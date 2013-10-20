# encoding: utf-8
from gameobject import *

class Enemy(GameObject):
    '''Enemy base class
    
    Subclasses should have images numbered correct in a subfolder to images named <classname> in all lowercase characters. The folder should also contain a "dissabled image" that should be in alpabetically last order. These images will be avalible as ImageTk.PhotoImage objects in the variables 'images' and 'eliminatedImage' respectivly.'''
    
    speed=8
    hp=1
    movePixels=-1
    eliminated=True
    def __init__(self,game):
        self.eliminated = False
        self.game=game
        self.hp=self.getStartHp()
        self.positionOfTailX=game.width+self.getWidth()
        
        x,y=game.width-50,randint(100,game.height-100)
        
        self.tag=hash(self)
        self.objectIds=[self.game.create_image(x,y,anchor='sw',image=image,state='hidden',tags=(self.tag,"Enemy")) for image in self.getImages()]
        self.objectIdsCycle = itertools.cycle(self.objectIds)
        
        self.objectId=next(self.objectIdsCycle)
        self.game.itemconfig(self.tag,state='normal')
        
        self.callback=self.enemyOnClick
        self.game.tag_bind(self.tag,'<Button-1>',self.callback)
        
        self.eliminated = False
        
        game.after(1,self.walk)
        game.after(1,self.animate)
        
    def __del__(self):
        print "enemy deleted"
        
    def delete(self):
        try:
            self.game.deleteEnemy(self)
            if not self.eliminated:
                self.eliminated=True
                self.game.tag_unbind(self.tag,'<Button-1>')
                del self.objectIdsCycle
                del self.objectIds
            
            self.game.delete(self.tag)
            self.game.delete(self.objectId)
            del self.callback
            del self.walk
            del self.tag
            del self.hp
            del self.objectId
            del self.eliminated
        except:
            print "fel i eliminate"
        #self.__del__()
    
            
    def eliminate(self):
        x,y = self.game.coords(self.tag)
        self.eliminated=True
        self.game.killEnemy(self)
        try:
            self.game.tag_unbind(self.tag,'<Button-1>')
            self.game.delete(self.tag)
        except:
            print "fel i eliminate"
        del self.objectIdsCycle
        del self.objectIds
        self.objectId=self.game.create_image(x,y,anchor='sw',image=self.eliminatedImage,tags=("Dead"))
        
        
    @classmethod
    def getImages(cls):
        return cls.images
    
    @classmethod
    def getStartHp(cls):
        return cls.hp
    
    @classmethod
    def getSpeed(cls):
        return cls.speed
    
    def move(self,dx,dy):
        self.game.move(self.tag,dx,dy)
        
    def animate(self):
        if self.game.gamePaused:
            self.game.resumeQueue.append(self.animate)
        elif not self.eliminated:
            if self.positionOfTailX>0:
                self.game.after(100,self.animate)
            self.nextPicture()
        
    def walk(self):
        if self.game.gamePaused:
            self.game.resumeQueue.append(self.walk)
        elif not self.eliminated:
            if self.positionOfTailX>0:
                self.game.after(int(100/self.speed),self.walk)
                self.move(self.movePixels,0)
                self.positionOfTailX=self.positionOfTailX+self.movePixels
            else:
                self.delete()
        
    def nextPicture(self):
        self.game.itemconfig(self.objectId,state='hidden')
        self.objectId = next(self.objectIdsCycle)
        self.game.itemconfig(self.objectId,state='normal')
			
    def enemyOnClick(self,event):
		self.game.score.currentScore = self.game.score.currentScore + 1
		self.game.itemconfig(self.game.score.scoreText,text="Score: " + str(self.game.score.currentScore))
                self.hp=self.hp-1
                if self.hp<=0:
                    self.eliminate()
                
    
class Boss(Enemy):
    '''Boss base class'''
	
    
def getEnemiesByLevel(self,level):
	if(level==1):
		return ["enemy2","enemy3","enemy4"]
	elif(level==2):
		return ["enemy5","enemy6","enemy7"]
	elif(level==3):
		return ["enemy8","enemy9","enemy10"]
