# encoding: utf-8
from gameobject import *

class Text(GameObject):
    def __init__(self,game,x,y,text,color='black',callback=None,font=None):
        GameObject.__init__(self,game,x,y,'c',callback,text,color,font)
