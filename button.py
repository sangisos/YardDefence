# encoding: utf-8
from gameobject import *
from text import *

class Button(GameObject):
    def __init__(self,game,x,y,text,callback):
        GameObject.__init__(self,game,x,y,'c',callback)
        self.textObject=Text(game,x,y,text,color='white',callback=callback)
    
