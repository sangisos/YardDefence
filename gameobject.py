# encoding: utf-8
try:  # import as appropriate for 2.x vs. 3.x
    from tkinter import Canvas,CURRENT
except:
    from Tkinter import Canvas,CURRENT
from PIL import Image,ImageTk
import os
from random import randint

class MetaGameObject(type):
    def __new__(mcs, classname, bases, dictionary):
        if not classname in ["GameObject","Enemy","Text"]:
            imageDir=os.curdir + os.sep + "images" + os.sep + str(classname).lower()
            filenames=[os.path.join(imageDir, f) for f in os.listdir(imageDir) if f.endswith(".gif")]
            filenames.sort()
            if "Enemy" in bases:
                dictionary["eliminatedImage"]=ImageTk.PhotoImage(image=Image.open(filenames.pop()))
            dictionary["images"] = [ImageTk.PhotoImage(image=Image.open(filename)) for filename in filenames]
            
        return type.__new__(mcs, classname, bases, dictionary)

class GameObject:
    '''All object that show pictures on screen should inherit the GameObjectclass, they have to have a folder in the image folder namned <classname>.
    
    Use text=<text> to create a text object.
    
    Use callback=<callback> for mouse callback method bound to <Button-1>. Use Tkinter.CURRENT as tag/id for object currently under mouse pointer.
    '''
    __metaclass__=MetaGameObject
    
    '''The base mouse callback method bound to <Button-1>. Overwrite to implement your own callback, use Tkinter.CURRENT as tag/id for object currently under mouse pointer'''
        
    def __init__(self,canvas,x,y,anchor='nw',callback=None,text=None):
        self.canvas=canvas
        if text:
            self.objectId = self.canvas.create_text(x,y,anchor=anchor,image=self.__class__.images[0])
        else:
            self.objectId = self.canvas.create_image(x,y,anchor=anchor,image=self.__class__.images[0])
        if callback:
            self.canvas.tag_bind(self.objectId,'<Button-1>',callback)
