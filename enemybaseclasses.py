# encoding: utf-8
from gameobject import *

class Enemy(GameObject):
    '''Enemy base class
    
    Subclasses should have images numbered correct in a subfolder to images named <classname> in all lowercase characters. The folder should also contain a "dissabled image" that should be in alpabetically last order. These images will be avalible as ImageTk.PhotoImage objects in the variables 'images' and 'eliminatedImage' respectivly.'''
    
    speed=5
    hp=1
    eliminated = False
    
    
    def __init__(self,game):
        
        GameObject.__init__(self,game,game.width-50,randint(100,game.height-100),callback=self.enemyOnClick)
        game.after(0,self.walk)
        
    
    def delete(self):
        self.game.deleteEnemy(self)
        
    @classmethod
    def getSpeed(cls):
        pass
    
    def walk(self):
		if(self.eliminated == False):
			self.game.after(int(100/self.speed),self.walk)
			self.move(-1,0)
		else:
			pass
			
    def enemyOnClick(self,event):
        #del self
		print "jdksdkj"
		#self.game.currentScore = self.game.currentScore + 1
		#print self.game.currentScore
    
class Boss(Enemy):
    '''Boss base class'''
	
    
def getEnemiesByLevel(self,level):
	if(level==1):
		return ["enemy2","enemy3","enemy4"]
	elif(level==2):
		return ["enemy5","enemy6","enemy7"]
	elif(level==3):
		return ["enemy8","enemy9","enemy10"]
