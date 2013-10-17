# encoding: utf-8
try:  # import as appropriate for 2.x vs. 3.x
    from tkinter import Tk,Canvas,Toplevel,CURRENT
except:
    from Tkinter import Tk,Canvas,Toplevel,CURRENT
from PIL import Image,ImageTk
import os
from random import randint

class MetaGameObject(type):
    def __new__(mcs, classname, bases, dictionary):
        if not classname in ["GameObject", "Enemy"]:
            imageDir=os.curdir + os.sep + "images" + os.sep + str(classname).lower()
            filenames=[os.path.join(imageDir, f) for f in os.listdir(imageDir) if f.endswith(".gif")]
            filenames.sort()
            if "Enemy" in bases:
                dictionary["eliminatedImage"]=ImageTk.PhotoImage(image=Image.open(filenames.pop()))
            dictionary["images"] = [ImageTk.PhotoImage(image=Image.open(filename)) for filename in filenames]
            
        return type.__new__(mcs, classname, bases, dictionary)

class GameObject:
    '''All object that show pictures on screen should inherit the GameObjectclass, they have to have a folder in the image folder namnet <classname>'''
    __metaclass__=MetaGameObject
    def mouseCallback(self,event):
        print CURRENT
        self.canvas.delete(CURRENT)
        
    def __init__(self,canvas,x,y,anchor='nw'):
        self.canvas=canvas
        self.imageID = self.canvas.create_image(x,y,anchor=anchor,image=self.__class__.images[0])
        self.canvas.tag_bind(self.imageID,'<Button-1>',self.mouseCallback)
