# encoding: utf-8
from gameobject import *

class Enemy(GameObject):
    '''Enemy base class
    
    Subclasses should have images numbered correct in a subfolder to images named <classname> in all lowercase characters. The folder should also contain a "dissabled image" that should be in alpabetically last order. These images will be avalible as ImageTk.PhotoImage objects in the variables 'images' and 'eliminatedImage' respectivly.'''
    
    speed=4
    hp=1
    eliminated = False
    
    
    def __init__(self,game):
        self.game=game
        callback=self.enemyOnClick
        x,y=game.width-50,randint(100,game.height-100)
        #GameObject.__init__(self,game,x,y)
        self.tag=hash(self)
        self.objectIds = itertools.cycle([self.game.create_image(x,y,anchor='sw',image=image,state='hidden',tags=(self.tag,"Enemy")) for image in self.getImages()])
        self.objectId=next(self.objectIds)
        self.game.itemconfig(self.tag,state='normal')
        self.game.tag_bind(self.tag,'<Button-1>',callback)
        
        game.after(1,self.walk)
        game.after(1,self.animate)
        
    
    def __del__(self):
        self.game.tag_unbind(self.tag,'<Button-1>')
        self.game.delete(self.tag)
        del self.objectId
        del self.game
        
    def delete(self):
        self.game.deleteEnemy(self)
        
    @classmethod
    def getImages(cls):
        return cls.images
    
    @classmethod
    def getSpeed(cls):
        return cls.speed
    
    def move(self,dx,dy):
        self.game.move(self.tag,dx,dy)
        
    def walk(self):
        if self.game.gamePaused:
            self.game.resumeQueue.append(self.walk)
        elif not self.eliminated:
            self.game.after(int(100/self.speed),self.walk)
            self.move(-2,0)
        
    def animate(self):
        if self.game.gamePaused:
            self.game.resumeQueue.append(self.animate)
        elif not self.eliminated:
            self.game.after(100,self.animate)
            self.nextPicture()
        
    def nextPicture(self):
        self.game.itemconfig(self.objectId,state='hidden')
        self.objectId = next(self.objectIds)
        self.game.itemconfig(self.objectId,state='normal')
			
    def enemyOnClick(self,event):
		self.game.score.currentScore = self.game.score.currentScore + 1
		self.game.itemconfig(self.game.score.scoreText,text="Score: " + str(self.game.score.currentScore))
    
class Boss(Enemy):
    '''Boss base class'''
	
    
def getEnemiesByLevel(self,level):
	if(level==1):
		return ["enemy2","enemy3","enemy4"]
	elif(level==2):
		return ["enemy5","enemy6","enemy7"]
	elif(level==3):
		return ["enemy8","enemy9","enemy10"]
