# encoding: utf-8
from gameobject import *

class Hero(GameObject):
	def __init__(self,game):
		GameObject.__init__(self,game,125,game.height/2.5,'c',callback=self.heroShoot)
		self.game.itemconfig(self.tag,state='hidden')
	
	def heroShoot(self,event):
		print "Shooooting"
		
	def show(self):
		self.game.itemconfig(self.tag,state='normal')
	def hide(self):
		self.game.itemconfig(self.tag,state='hidden')
