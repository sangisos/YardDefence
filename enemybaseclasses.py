# encoding: utf-8
from gameobject import *
import inspect,sys,gc
class Enemy(GameObject):
    '''Enemy base class
    
    Subclasses should have images numbered correct in a subfolder to images named <classname> in all lowercase characters. The folder should also contain a "dissabled image" that should be in alpabetically last order. These images will be avalible as ImageTk.PhotoImage objects in the variables 'images' and 'eliminatedImage' respectivly.'''
    
    speed=0.1 # Never above MAX_SPEED (CraAAaaAAaaZy fast). well... should be at least.....   FIXME DEBUG
    MAX_SPEED=1.0
    hp=1
    movePixels=-1
    eliminated=True # if not an instance.
    activeEnemies=[]
    deadEnemies=[]
    currentTics=0.
    stepsTaken=0
    stepSize=4 ######## Pixels moved per iteration, a value of 1 to 5 is ok ########  FIXME DEBUG
    animationRunning=False
    
    def __init__(self,game):
        self.eliminated = False
        self.game=game
        self.positionOfTailX=game.winfo_width()+self.getWidth()
        self.endStep=self.stepsTaken+game.winfo_width()+self.getWidth()
        margintopbottom=game.winfo_height()/7
        x,y=game.winfo_width()-50,randint(margintopbottom,margintopbottom*6)
        self.tag="enemy"+str(hash(self))
        self.tagDead="dead"+str(hash(self))
        self.objectIds=[self.game.create_image(x,y,anchor='sw',image=image,state='hidden',tags=(self.tag,self.classTag,"Enemy")) for image in self.getImages()]
        self.eliminatedId=self.game.create_image(x,y,anchor='sw',image=self.eliminatedImage,state='hidden',tags=(self.tagDead,self.classTag,"Dead"))
        self.objectIdsCycle = itertools.cycle(self.objectIds)
        
        self.objectId=next(self.objectIdsCycle)
        self.game.itemconfig(self.objectId,state='normal')
        
        self.callback=self.enemyOnClick
        
        self.funcId=self.game.tag_bind(self.tag,'<Button-1>',self.callback)
        
        self.activeEnemies.append(self)
        
        #game.after(1,self.walk)
        #game.after(1,self.animate)
        
    def __del__(self):
        print "enemy deleted i enemybaseclass.__del__("+str(self)+")"
        
    def delete(self):
        if not self.eliminated:
            self.game.tag_unbind(self.tag,'<Button-1>',self.funcId)
            self.activeEnemies.remove(self)
            self.eliminated=True
            del self.objectIdsCycle
            del self.objectIds
        else:
            self.game.tag_unbind(self.tagDead,'<Button-1>')
            self.deadEnemies.remove(self)
            
        self.game.delete(self.tag)
        self.game.delete(self.objectId)
        del self.callback
        del self.objectId
        del self.eliminatedId
        del self.game
        #print "referrers: ",
        #print gc.get_referrers(self)
        #print "referents: ",
        #print gc.get_referents(self)
    
    def eliminate(self):
        x,y = self.game.coords(self.objectId)
        self.eliminated=True
        
        self.activeEnemies.remove(self)
        self.deadEnemies.append(self)
        self.game.tag_unbind(self.tag,'<Button-1>',self.funcId)
        self.game.delete(self.tag)
        self.objectId=self.eliminatedId
        self.game.dtag(self.objectId,self.classTag)
        self.game.tag_bind(self.objectId,'<Button-1>',self.game.hero.heroShoot)
        self.game.itemconfig(self.objectId,image=self.eliminatedImage,state='normal')
        
        del self.objectIdsCycle
        del self.objectIds
        
        
    @classmethod
    def getImages(cls):
        return cls.images
    
    def move(self,dx,dy):
        self.game.move(self.tag,dx,dy)
        
    @classmethod
    def moveAll(cls,game,tics):
        maxSpeed=Enemy.MAX_SPEED-game.difficulty/6.0
        #print getEnemyClasses(game.level)
        for enemycls in getEnemyClasses(game.level):
            enemycls.currentTics=enemycls.currentTics+tics
            #print enemycls
            #print enemycls.currentTics
            #print maxSpeed
            if enemycls.currentTics>maxSpeed-enemycls.speed/2.0:
                enemycls.currentTics=0
                game.move(enemycls.classTag,-enemycls.stepSize,0)
                game.itemconfig(enemycls.classTag,image=next(enemycls.imageCycle))
                enemycls.stepsTaken=enemycls.stepsTaken+enemycls.stepSize
    @classmethod
    def missedEnemy(cls,game):
        #print "activeEmemies: " + str(cls.activeEnemies) ##############DEBUG#############
        for enemy in Enemy.activeEnemies:
            if enemy.endStep<enemy.stepsTaken:
                if game.lifeList:
                    del game.lifeList[-1]
                if not game.lifeList:
                    game.gameOver()
                enemy.delete()
        
    
    @classmethod
    def animateAll(cls):
        pass
        
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
        self.game.hero.heroShoot()
        self.game.score.addPoint()
        self.hp=self.hp-1
        if self.hp<=0:
            self.eliminate()
                
    
class Boss(Enemy):
    '''Boss base class'''
	
class EnemyHandler:
    def __init__(self,game):
        self.game=game
        self.enemyTicker=0
        self.timeForEnemy=0
    def mainloop(self):
        if self.game.gameRunning:
            self.game.after(30,self.mainloop)
            self.enemyTicker=self.enemyTicker+0.1
            ####### Enemy main loop ##########
            Enemy.moveAll(self.game,self.enemyTicker)
            Enemy.missedEnemy(self.game)
            self.createEnemy()
            ####### Enemy main loop end ##########
            self.game.update()
        elif self.game.gamePaused:
            self.game.resumeQueue.append(self.mainloop)
        else:
            print "EnemyHandler mainloop ended" ######## DEBUG ######
            
    def createEnemy(self):
        self.
        if >timeForEnemy
        random.choice(getEnemyClasses(self.level))(self)






def getEnemyClasses(level):
    '''gives all enemies at level=<level> as a list of classes'''
    return [enemyClass[1] for enemyClass in inspect.getmembers(sys.modules["enemyclasses"], lambda member: inspect.isclass(member) and member.__module__ == "enemyclasses") if not issubclass(enemyClass[1],Boss) and enemyClass[1].level == level]
