# encoding: utf-8
from tkstart import *

class _MetaGameObject(type):
    def __new__(mcs, classname, bases, dictionary):
        if not classname in ["GameObject","Enemy","Boss","Text"]:
            imageDir=os.curdir + os.sep + "images" + os.sep + str(classname).lower()
            filenames=[os.path.join(imageDir, f) for f in os.listdir(imageDir) if f.endswith(".gif")]
            filenames.sort()
            if "Enemy" in bases:
                dictionary["eliminatedImage"]=ImageTk.PhotoImage(image=Image.open(filenames.pop()))
            imgs=[Image.open(filename) for filename in filenames]
            if classname is "Background":
                imgs=[img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS) for img in imgs]
            dictionary["images"] = [ImageTk.PhotoImage(image=img) for img in imgs]
            
        return type.__new__(mcs, classname, bases, dictionary)

class GameObject:
    '''All object that show pictures on screen should inherit the GameObjectclass, they have to have a folder in the image folder namned <classname>.
    
    Use text=<text> to create a text object.
    
    Use callback=<callback> for mouse callback method bound to <Button-1>. Use Tkinter.CURRENT as tag/id for object currently under mouse pointer.
    '''
    __metaclass__=_MetaGameObject
    
    def __init__(self,game,x,y,anchor='nw',callback=None,text=None,color='black',imageNumber=0):
        self.game=game
        if text:
            self.objectId = self.game.create_text(x,y,anchor=anchor,text=text,fill=color)
        else:
            self.objectId = self.game.create_image(x,y,anchor=anchor,image=self.__class__.images[imageNumber])
        if callback:
            self.callback=callback
            self.game.tag_bind(self.objectId,'<Button-1>',callback)
    
    def __del__(self):
        self.game.tag_unbind('<Button-1>',self.objectId)
        self.game.delete(self.objectId)
        del self.objectId
        del self.game
        
    
    def getHeight(self):
        # Om man inte vill att något visst ska "hoppa" vid animering:
        #return self.__class__.images[0].height()
        bbox=self.game.bbox(self.objectId)
        return bbox[3]-bbox[1]
