# encoding: utf-8
try:  # import as appropriate for 2.x vs. 3.x
    from tkinter import Tk,Canvas,Event,CURRENT
except:
    from Tkinter import Tk,Canvas,Event,CURRENT
root=Tk()
from PIL import Image,ImageTk
import os
import time
from random import randint
from gameobject import GameObject
import heroLife

class GameWindow(Canvas):
    '''Spelfönstrets klass, håller koll!'''
    def __init__(self):
        
        # Runs in fullscreen
        root.attributes('-fullscreen', True)
        
        
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        Canvas.__init__(self, root, width=self.width, height=self.height,bg="#009900")
        self.pack()
        
        root.update()
        
        
        self.font=('Helvetica 11 bold')
        self.level=1
        self.difficulty=1
        self.menuObject=None
        
        self.startMenu()
        
        
        
        
    def startMenu(self,event=None):
        self.menuObject=Menu(self,[("Play",self.difficultyMenu),("Exit",self.exit)])
    
    def difficultyMenu(self,event=None):
        self.menuObject=Menu(self,[("Easy",self.startWithDifficultyCallback),("Medium",self.startWithDifficultyCallback),("Hard",self.startWithDifficultyCallback),('Back',self.startMenu)])
        
    def startWithDifficultyCallback(self,event):
        buttonNumber = self.menuObject.getButtonNumber(event)
        self.difficulty = buttonNumber + 1
        self.initGame()
        
    def exit(self,event=None):
        root.quit()

    def initGame(self):
        del self.menuObject
        self.background=Background(self)
        Hero(self)
        CurrentScore(self)
        
        lifeList = []
        lifePositionX = self.width/2.5
        for x in range(3):
            lifeList.append(heroLife.HeroLife(self,lifePositionX))
            lifePositionX = lifePositionX + 30
            
        self.activeEnemies=[]
        self.deadEnemies=[]
        self.storyteller=StoryTeller(self)
        self.after(0,self.doOneFrame)
        self.after(0,self.createEnemy)
            
    def createEnemy(self):
        enemy=enemy2(self)
        self.activeEnemies.append(enemy)
        self.after(randint(100,3000)/(self.level*self.difficulty),self.createEnemy)
        self.after(2000,enemy.delete)
        
    def deleteEnemy(self,enemy):
        self.activeEnemies.remove(enemy)
        
    def doOneFrame(self):
        # Commented for debug. Uncomment to loop: 
        self.after(30,self.doOneFrame)
        ### Skriv kod efter här för att visa en frame
        
        root.update()
        
    

class Enemy(GameObject):
    '''Subclasses should have images numbered correct in a subfolder to images named <classname> in all lowercase characters. The folder should also contain a "dissabled image" that should be in alpabetically last order. These images will be avalible as ImageTk.PhotoImage objects in the variables 'images' and 'eliminatedImage' respectivly.'''
    def __init__(self,game):
        
        GameObject.__init__(self,game,game.width-50,randint(100,game.height-100))
    def delete(self):
        self.game.deleteEnemy(self)
        
class enemy2(Enemy):
    '''en fiende'''

class Background(ImageTk.PhotoImage):
    def __init__(self, game):
        self.game=game
        filename = "images/background" + str(game.level) + ".gif"
        image = Image.open(filename)
        rezisedImageObj = image.resize((game.width, game.height), Image.ANTIALIAS)
        ImageTk.PhotoImage.__init__(self,image=rezisedImageObj)
        self.imageID = game.create_image(0,0,anchor="nw",image=self)
        game.tag_lower(self)

class Menu(GameObject):
    def __init__(self,game,buttonTextCallbackTuples,back=None):
        x,y = game.width/2,game.height/2
        GameObject.__init__(self,game,x,y,'c')
        
        # Place buttons
        heightForButtonPlacement=self.getHeight()/2 
        ydiff=heightForButtonPlacement/2
        yjump=heightForButtonPlacement/len(buttonTextCallbackTuples)
        ydeltas=range(-ydiff,ydiff,yjump)
        # Have to save one (and only one) ref to buttons, otherwise garbagecollected by python, if more than one, object will not be deleted
        self.buttons=[Button(game,x,y+ydelta,buttonText,callback=buttonCallback) for (buttonText,buttonCallback),ydelta in zip(buttonTextCallbackTuples,ydeltas)]
    def getButtonNumber(self,event):
        # HERE BE DRAGONS
        current = self.game.find_withtag(CURRENT)
        button = [self.buttons.index(button) for button in self.buttons if current[0] in [button.objectId, button.textObject.objectId]]
        return button[0] # Could fail if no object is found above, but the callback that triggers this method should only be called if the button or it's text is the 'current' object.

class Button(GameObject):
    def __init__(self,game,x,y,text,callback):
        GameObject.__init__(self,game,x,y,'c',callback)
        self.textObject=Text(game,x,y,text,'white',callback)

class Text(GameObject):
    def __init__(self,game,x,y,text,color='black',callback=None):
        GameObject.__init__(self,game,x,y,'c',callback,text,color)

class StoryTeller(GameObject):
	def __init__(self,game):
		x,y = game.width/2,game.height/2
		GameObject.__init__(self,game,x,y,'c')
		game.create_text(x,y,text="Dear Neighbour, \nYesterday my whole farm was attacked by a massive mob of \nWILD ANIMALS, they have eaten all my harvest. \nI am afraid that they are on their way to your farm right now. \nI hope you are prepared to protect your land! \n\nThey are freakin' CrAaaAaazzZyy!! \n\nRegards,\nLennart",anchor='c',fill='black',font=game.font)

class CurrentScore():
	def __init__(self,game):
		currentScore = 0
		game.create_text(50,50,text="Score: " + str(currentScore),anchor='c')
		
class Hero(GameObject):
	def __init__(self,game):
		GameObject.__init__(self,game,110,game.height/2.5,'c')

def main():
    game=GameWindow()
    root.mainloop()

if __name__ == "__main__":
	main()
