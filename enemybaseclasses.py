# encoding: utf-8
from gameobject import *
import inspect,sys,gc
class Enemy(GameObject):
    '''Enemy base class
    
    Subclasses should have images numbered correct in a subfolder to images named <classname> in all lowercase characters. The folder should also contain a "dissabled image" that should be in alpabetically last order. These images will be avalible as ImageTk.PhotoImage objects in the variables 'images' and 'eliminatedImage' respectivly.'''
    
    speed=9 # Never above MAX_SPEED (CraAAaaAAaaZy fast)
    MAX_SPEED=9
    hp=1
    movePixels=-1
    eliminated=True # if not an instance.
    activeEnemies=[]
    deadEnemies=[]
    stepsTaken=0
    stepSize=100
    animationRunning=False
    
    def __init__(self,game):
        self.eliminated = False
        self.game=game
        self.positionOfTailX=game.winfo_width()+self.getWidth()
        self.endStep=self.stepsTaken+game.winfo_width()+self.getWidth()
        margintopbottom=game.winfo_height()/7
        x,y=game.winfo_width()-50,randint(margintopbottom,margintopbottom*6)
        self.tag="enemy"+str(hash(self))
        self.objectIds=[self.game.create_image(x,y,anchor='sw',image=image,state='hidden',tags=(self.tag,self.classTag,"Enemy")) for image in self.getImages()]
        self.eliminatedId=self.game.create_image(x,y,anchor='sw',image=self.eliminatedImage,state='hidden',tags=(self.tag,self.classTag,"Enemy","Dead"))
        self.objectIdsCycle = itertools.cycle(self.objectIds)
        
        self.objectId=next(self.objectIdsCycle)
        self.game.itemconfig(self.objectId,state='normal')
        
        self.callback=self.enemyOnClick
        self.callback2=game.hero.heroShoot
        
        self.game.tag_bind(self.tag,'<Button-1>',self.callback)
        self.game.tag_bind(self.tag,'<Button-1>',self.callback2,'+')
        
        self.activeEnemies.append(self)
        
        #game.after(1,self.walk)
        #game.after(1,self.animate)
        
    def __del__(self):
        print "enemy deleted i enemybaseclass.__del__("+str(self)+")"
        
    def delete(self):
        self.game.tag_unbind(self.objectId,'<Button-1>')
        self.game.tag_unbind(self.tag,'<Button-1>')
        if not self.eliminated:
            self.activeEnemies.remove(self)
            self.eliminated=True
            del self.objectIdsCycle
            del self.objectIds
        else:
            self.deadEnemies.remove(self)
            
        self.game.delete(self.tag)
        self.game.delete(self.objectId)
        del self.callback
        del self.objectId
        del self.eliminatedId
        del self.callback2
        del self.game
        print "referrers: ",
        print gc.get_referrers(self)
        print "referents: ",
        print gc.get_referents(self)
    
    def eliminate(self):
        x,y = self.game.coords(self.tag)
        self.eliminated=True
        self.activeEnemies.remove(self)
        self.deadEnemies.append(self)
        try:
            self.game.tag_unbind(self.tag,'<Button-1>')
            self.game.delete(self.tag)
        except:
            print "fel i ebc.eliminate"
        del self.objectIdsCycle
        del self.objectIds
        self.objectId=self.game.create_image(x,y,anchor='sw',image=self.eliminatedImage,tags=("Dead"))
        self.game.tag_bind(self.objectId,'<Button-1>',self.callback2)
        self.game.itemconfig(self.objectId,state='normal')
        self.game.after(5000,self.delete)
        
        
    @classmethod
    def getImages(cls):
        return cls.images
    
    def move(self,dx,dy):
        self.game.move(self.tag,dx,dy)
        
    @classmethod
    def moveAll(cls,game,tics):
        maxSpeed=Enemy.MAX_SPEED+3-game.difficulty
        for enemycls in getEnemyClasses(game.level):
            if tics%(maxSpeed-enemycls.speed)==0:
                game.move(enemycls.classTag,-enemycls.stepSize,0)
                enemycls.stepsTaken=enemycls.stepsTaken+enemycls.stepSize
        
    @classmethod
    def missedEnemy(cls,game):
        print "activeEmemies: " + str(cls.activeEnemies) ##############DEBUG#############
        for enemy in Enemy.activeEnemies:
            if enemy.endStep<enemy.stepsTaken:
                if game.lifeList:
                    del game.lifeList[-1]
                if not game.lifeList:
                    game.gameOver()
                enemy.delete()
        
    
    @classmethod
    def animateAll(cls):
        cls.animationRunning=True
        
    def animate(self):
        try:
            if self.game.gamePaused:
                self.game.resumeQueue.append(self.animate)
            elif not self.eliminated:
                if self.positionOfTailX>0:
                    self.game.after(100,self.animate)
                    self.nextPicture()
        except:
            print "fel i animate"
        
    def walk(self):
        if self.game.gamePaused:
            self.game.resumeQueue.append(self.walk)
        elif not self.eliminated:
            if self.positionOfTailX>0:
                self.game.after(int(100/self.speed),self.walk)
                self.move(self.movePixels,0)
                self.positionOfTailX=self.positionOfTailX+self.movePixels
            else:
                if self.game.lifeList:
                    del self.game.lifeList[-1]
                    if not self.game.lifeList:
                        self.game.gameOver()
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

class EnemyHandler:
    def __init__(self,game):
        self.game=game

def getEnemyClasses(level):
    '''gives all enemies at level=<level> as a list of classes'''
    return [enemyClass[1] for enemyClass in inspect.getmembers(sys.modules["enemyclasses"], lambda member: inspect.isclass(member) and member.__module__ == "enemyclasses") if not issubclass(enemyClass[1],Boss) and enemyClass[1].level == level]
