# encoding: utf-8
from gameobject import *

class Enemy(GameObject):
    '''Enemy base class
    
    Subclasses should have images numbered correct in a subfolder to images named <classname> in all lowercase characters. The folder should also contain a "dissabled image" that should be in alpabetically last order. These images will be avalible as ImageTk.PhotoImage objects in the variables 'images' and 'eliminatedImage' respectivly.'''
    def __init__(self,game):
        
        GameObject.__init__(self,game,game.width-50,randint(100,game.height-100))
    def delete(self):
        self.game.deleteEnemy(self)
        
class Boss(Enemy):
    '''Boss base class'''
