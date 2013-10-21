# encoding: utf-8
from gameobject import *

class Background(GameObject):
    def __init__(self, game):
        GameObject.__init__(self,game,0,0,imageNumber=game.level,callback=game.hero.heroShoot)
        game.tag_lower(self.objectId)
