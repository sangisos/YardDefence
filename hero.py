# encoding: utf-8
from gameobject import *

class Hero(GameObject):
	def __init__(self,game):
		GameObject.__init__(self,game,110,game.height/2.5,'c')
