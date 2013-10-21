# encoding: utf-8
from gameobject import *

class Text(GameObject):
    def __init__(self,game,x,y,text,anchor='c',color='black',callback=None,font=None):
        GameObject.__init__(self,game,x,y,anchor,callback=callback,text=text,color=color,font=font)
