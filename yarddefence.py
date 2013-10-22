# encoding: utf-8
from gameimports import *

class GameWindow(Canvas):
    '''Spelfönstrets klass, håller koll!'''
    def __init__(self):
        
        # Runs in fullscreen
        root.attributes('-fullscreen', True)
        
        self.gameTicker=0
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
        self.enemy=EnemyHandler(self)
        
        self.resumeQueue = []
        
        self.level=0
        self.difficulty=1
        self.menuObject=None
        self.gamePaused=False
        self.gameRunning=False
        
        
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
        while self.resumeQueue:
            self.after(0,self.resumeQueue.pop())
    
    def initGame(self):
        del self.menuObject
        self.gameRunning=True
        self.score = CurrentScore(self)
        self.hero.show()
        self.enemy.mainloop()
        
        self.lifeList = []
        lifePositionX = self.width/2-165
        for x in range(3):
            self.lifeList.append(HeroLife(self,lifePositionX))
            lifePositionX = lifePositionX + 30
            
        self.after(0,self.doOneFrame)
        self.after(0,self.createEnemy)
        self.after(2000,self.createEnemy)
        self.after(4000,self.createEnemy)
        self.after(6000,self.createEnemy)
            
    def createEnemy(self):
        random.choice(getEnemyClasses(self.level))(self)
        #enemy=eval(random.choice(getEnemiesByLevel(self,self.level)))(self)
        #self.after(randint(100,3000)/(self.level*self.difficulty),self.createEnemy)
        
    def doOneFrame(self):
        # Commented for debug. Uncomment to loop: 
        if self.gameRunning:
            self.after(5,self.doOneFrame)  ######### DEBUG ########## should be 2 to 30
            root.update()
        elif self.gamePaused:
            self.resumeQueue.append(self.doOneFrame)
            root.update()
        else:
            self.gameTicker=self.gameTicker+1
            ### Skriv kod efter här för att visa en frame
            #self.activeEnemies[0].walk(self,1)
            self.enemy.createRandom()
            self.enemy.moveAll()
            self.enemy.missedEnemy()
            
            root.update()
    
    def gameOver(self):
        self.gameOverText = self.create_text(self.width/2,self.height/2,text="Game Over",anchor='c',fill='black',font=(self.font,36,"bold"))

class StoryTeller(GameObject):
	def __init__(self,game):
            #self.tag="storyTeller" + str(hash(self))
            game.background=Background(game)
            x,y = game.width/2,game.height/2
            GameObject.__init__(self,game,x,y,'c',self.storyTellerOnClick)
            self.textObject=Text(game,x,y,text="Dear Neighbour, \nYesterday my whole farm was attacked by a massive mob of \nWILD ANIMALS, they have eaten all my harvest. \nI am afraid that they are on their way to your farm right now. \nI hope you are prepared to protect your land! \n\nRegards,\nLennart",callback=self.storyTellerOnClick,color='black',font=game.storyFont)
            #Oh my good, these animals are CRAZY! \nI have an idea, lets dig a river through our lands, \nmaybe that will keep the animals away. \n\nRegards, \nLennart"
            #Looks like the river is to small for theese even crazier animals. \nBut hey, I have an even CRAZIER idea. \nI have some old dynamites in my basement, lets use them to blow up some more land. \Im sure that will stop the animals from destroying our farms. \nGood luck! \n\nRegards, \nLennart
            #If you read this I assume that you are still alive \nand have defeated the CRAZY big boat of wild animals. \nI saw them, they loaded the boat with all the remainings \of their army. Our farms are now safe. \nCongratulations! \n\nGreetings, \nLennart \n\nScore: " + currentScore
        def storyTellerOnClick(self,event):
            #self.game.delete(self.tag)
            self.game.delete(self.objectId)
            del self.textObject
            self.game.initGame()
            
class CurrentScore():
    def __init__(self,game):
        self.game=game
        self.currentScore = 0
        self.scoreText = game.create_text(game.width/2,40,text="Score: 0",anchor='c',fill='black',font=(game.font,20,"bold"))
        
    def addPoint(self):
        self.currentScore = self.game.score.currentScore + 1
        self.game.itemconfig(self.game.score.scoreText,text="Score: " + str(self.game.score.currentScore))



def main():
    game=GameWindow()
    root.mainloop()

if __name__ == "__main__":
	main()
