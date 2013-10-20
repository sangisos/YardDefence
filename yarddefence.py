# encoding: utf-8
from gameimports import *

class GameWindow(Canvas):
    '''Spelfönstrets klass, håller koll!'''
    def __init__(self):
        
        # Runs in fullscreen
        root.attributes('-fullscreen', True)
        
        
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        self.centerx = self.width/2
        self.centery = self.height/2
        Canvas.__init__(self, root, width=self.width, height=self.height,bg="#009900")
        
        self.pack()
        root.update()
        
        # Standard font, används i gameobject om inget anges
        self.font=('Helvetica 12 normal')
        self.storyFont=('Helvetica 11 bold')
        
        self.level=0
        self.difficulty=1
        self.menuObject=None
        self.gamePaused=False
        
        
        root.bind('<Escape>',self.confirmExit)
        
        self.startMenu()
        
        
        
        
    def startMenu(self,event=None):
        self.background=Background(self)
        self.menuObject=Menu(self,[("Play",self.difficultyMenu),("Exit",self.confirmExit)])
    
    def difficultyMenu(self,event=None):
        self.menuObject=Menu(self,[("Easy",self.startWithDifficultyCallback),("Medium",self.startWithDifficultyCallback),("Hard",self.startWithDifficultyCallback),('Back',self.startMenu)])
        
    def startWithDifficultyCallback(self,event):
        buttonNumber = self.menuObject.getButtonNumber(event)
        self.difficulty = buttonNumber + 1
        self.level=1
        self.initGame()
        
    def confirmExit(self,event=None):
        self.pauseGame()
        self.menuObject=Menu(self,[('Yes', self.exit), ('No', self.continueGame)],title="Exit game?")
        
    def exit(self,event=None):
        self.quit()
        
    def pauseGame(self,event=None):
        self.gamePaused=True
    
    def continueGame(self,event=None):
        self.gamePaused=False
    
    def initGame(self):
        del self.menuObject
        self.background=Background(self)
        self.hero=Hero(self)
        
        CurrentScore(self)
        self.score = CurrentScore(self)
        
        self.resumeQueue = []
        self.lifeList = []
        lifePositionX = self.width/2.5
        for x in range(3):
            self.lifeList.append(HeroLife(self,lifePositionX))
            lifePositionX = lifePositionX + 30
            
        self.activeEnemies=[]
        self.deadEnemies=[]
        self.storyteller=StoryTeller(self)
        self.after(0,self.doOneFrame)
        self.after(0,self.createEnemy)
            
    def createEnemy(self):
        enemy=eval(random.choice(getEnemiesByLevel(self,self.level)))(self)
        self.activeEnemies.append(enemy)
        self.after(randint(100,3000)/(self.level*self.difficulty),self.createEnemy)
        
    def killEnemy(self,enemy):
        self.activeEnemies.remove(enemy)
        self.deadEnemies.append(enemy)
        
    def deleteEnemy(self,enemy):
        print "trying to delete enemy: " + str(enemy) + " from active.",
        try:
            self.activeEnemies.remove(enemy)
            print " success"
        except:
            print "trying to delete enemy: " + str(enemy) + " from dead."
            try:
                self.deadEnemies.remove(enemy)
                print " success"
            except:
                print str(enemy) + " no reference here."
                
    def doOneFrame(self):
        # Commented for debug. Uncomment to loop: 
        self.after(30,self.doOneFrame)
        ### Skriv kod efter här för att visa en frame
        #self.activeEnemies[0].walk(self,1)
        
        root.update()
        

class StoryTeller(GameObject):
	def __init__(self,game):
		x,y = game.width/2,game.height/2
		GameObject.__init__(self,game,x,y,'c')
		game.create_text(x,y,text="Dear Neighbour, \nYesterday my whole farm was attacked by a massive mob of \nWILD ANIMALS, they have eaten all my harvest. \nI am afraid that they are on their way to your farm right now. \nI hope you are prepared to protect your land! \n\nRegards,\nLennart",anchor='c',fill='black',font=game.storyFont)

class CurrentScore():
	def __init__(self,game):
		self.currentScore = 0
		self.scoreText = game.create_text(game.width/2,40,text="Score: " + str(self.currentScore),anchor='c',fill='black',font=(game.font,20,"bold"))

def main():
    game=GameWindow()
    root.mainloop()

if __name__ == "__main__":
	main()
