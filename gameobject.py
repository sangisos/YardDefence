# encoding: utf-8
from tkstart import *

class _MetaGameObject(type):
    def __new__(mcs, classname, bases, dictionary):
        if not classname in ["GameObject","Enemy","Boss","Text"]:
            imageDir=os.curdir + os.sep + "images" + os.sep + str(classname).lower()
            filenames=[os.path.join(imageDir, f) for f in os.listdir(imageDir) if f.endswith(".gif")]
            filenames.sort()
            
            if "Enemy" in str(bases) or "Boss" in str(bases):
                popedname=filenames.pop()
                print popedname
                dictionary["eliminatedImage"]=ImageTk.PhotoImage(image=Image.open(popedname))
                
            imgs=[Image.open(filename) for filename in filenames]
            
            if classname is "Background":
                imgs=[img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS) for img in imgs]
            
            dictionary["images"] = [ImageTk.PhotoImage(image=img) for img in imgs]
            
        return type.__new__(mcs, classname, bases, dictionary)

class GameObject:
    '''All object that show pictures on screen should inherit the GameObjectclass, they have to have a folder in the image folder namned <classname>.
    
    Make sure to always keep a reference to the object as long as it should be 'alive', otherwise the evil good natured Garbage Collector will come and eat your object!
    
    Use text=<text> to create a text object.
    
    Use callback=<callback> for mouse callback method bound to <Button-1>. Use Tkinter.CURRENT as tag/id for object currently under mouse pointer.
    '''
    __metaclass__=_MetaGameObject
    
    def __init__(self,game,x,y,anchor='nw',callback=None,text=None,color='black',imageNumber=0,font=None):
        self.game=game
        self.tag="gameObject"+str(hash(self))
        if text:
            if font is None:
                font=game.font
            self.objectId = self.game.create_text(x,y,anchor=anchor,text=text,fill=color,font=font,tags=self.tag)
        else:
            self.objectId = self.game.create_image(x,y,anchor=anchor,image=self.getImage(imageNumber),tags=self.tag)
        if callback:
            self.callback=callback
            self.game.tag_bind(self.objectId,'<Button-1>',callback)
    
    def __del__(self):
        self.game.tag_unbind('<Button-1>',self.objectId)
        self.game.delete(self.objectId)
        del self.objectId
        del self.game
        
    @classmethod
    def getImage(cls,number):
        return cls.images[number]
    
    @classmethod
    def getWidth(cls):
        return cls.images[0].width()
    
    @classmethod
    def getHeight(cls):
        return cls.images[0].height()
    
    def getbboxHeight(self):
        '''Om man inte vill att något visst ska "hoppa" vid animering, använd "return self.__class__.images[0].height()" (getHeight()), den tar bara höjden av första bilden. Den kan även användas utan att man har ett objekt av klassen'''
        bbox=self.game.bbox(self.objectId)
        return bbox[3]-bbox[1]
        
    
