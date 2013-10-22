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
        self.hero=Hero(self)
        
        self.level=0
        self.difficulty=1
        self.menuObject=None
        self.gamePaused=False
        self.bossJustDied=False
        
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
        self.storyteller=StoryTeller(self)
        
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
        try:
            del self.menuObject
        except:
            pass
        self.score = CurrentScore(self)
        self.hero.show()
        
        self.resumeQueue = []
        self.lifeList = []
        lifePositionX = self.width/2-165
        for x in range(3):
            self.lifeList.append(HeroLife(self,lifePositionX))
            lifePositionX = lifePositionX + 30
            
        self.activeEnemies=[]
        self.deadEnemies=[]
        self.after(0,self.doOneFrame)
        self.after(0,self.createEnemy)
            
    def createEnemy(self):
        enemy=eval(random.choice(getEnemiesByLevel(self,self.level)))(self)
        self.activeEnemies.append(enemy)
        if self.bossJustDied:
            self.after(5000,self.tellStory)
            self.bossJustDied=False
        else:
            self.after(randint(400,4000)/(self.difficulty),self.createEnemy)
        
    def killEnemy(self,enemy):
        try:
            self.activeEnemies.remove(enemy)
            self.deadEnemies.append(enemy)
        except:
            pass
        
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
        
    def gameOver(self):
        self.gameOverText = self.create_text(self.width/2,self.height/2,text="Game Over",anchor='c',fill='black',font=(self.font,36,"bold"))
        
        root.update()
        
    def tellStory(self,event=None):
        self.storyteller=StoryTeller(self)
            
class CurrentScore():
    def __init__(self,game):
        self.game=game
        self.currentScore = 0
        self.scoreText = game.create_text(game.width/2,40,text="Score: 0",anchor='c',fill='black',font=(game.font,20,"bold"))
        
    def addPoint(self):
        self.currentScore = self.currentScore + 1
        self.game.itemconfig(self.game.score.scoreText,text="Score: " + str(self.game.score.currentScore))
        if(self.currentScore == self.game.level*10):
            if self.game.level == 1:
                self.game.boss=boss1(self.game)
            elif self.game.level == 2:
                self.game.boss=boss2(self.game)
            elif self.game.level == 3:
                self.game.boss=boss3(self.game)


def main():
    game=GameWindow()
    root.mainloop()

if __name__ == "__main__":
	main()
