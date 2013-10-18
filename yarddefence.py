# encoding: utf-8
try:  # import as appropriate for 2.x vs. 3.x
    from tkinter import Tk,Canvas,Toplevel
except:
    from Tkinter import Tk,Canvas,Toplevel
root=Tk()
from PIL import Image,ImageTk
import os
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
        
        
        
        self.level=1
        
        
        self.menu() 
        
        
        
        
    def menu(self):
		Menu(self)


    def initGame(self):
		self.background=Background(self)
		self.activeEnemys=[]
		self.deadEnemys=[]
		self.after(0,self.doOneFrame)
		self.after(0,self.createEnemy)
        
    def createEnemy(self):
        self.activeEnemys.append(enemy2(self))
        self.after(randint(100,3000)/(self.level*self.difficulty),self.createEnemy)
        
    
    def doOneFrame(self):
        # Commented for debug. Uncomment to loop: 
        self.after(30,self.doOneFrame)
        ### Skriv kod efter här för att visa en frame
        
        
        
        
        
        root.update()
        
    
class Enemy(GameObject):
    '''Subclasses should have images numbered correct in a subfolder to images named <classname> in all lowercase characters. The folder should also contain a "dissabled image" that should be in alpabetically last order. These images will be avalible as ImageTk.PhotoImage objects in the variables 'images' and 'eliminatedImage' respectivly.'''
    def __init__(self,canvas):
        
        GameObject.__init__(self,canvas,canvas.width-50,randint(100,canvas.height-100))
        
class enemy2(Enemy):
    '''en fiende'''

class Background(ImageTk.PhotoImage):
    def __init__(self, canvas):
        self.canvas=canvas
        filename = "images/background" + str(canvas.level) + ".gif"
        image = Image.open(filename)
        rezisedImageObj = image.resize((canvas.width, canvas.height), Image.ANTIALIAS)
        ImageTk.PhotoImage.__init__(self,image=rezisedImageObj)
        self.imageID = canvas.create_image(0,0,anchor="nw",image=self)
        canvas.tag_lower(self)
		
class Menu(GameObject):
	def __init__(self,game):
            self.game=game
            game.difficulty=1
            x,y = game.width/2,game.height/2
            GameObject.__init__(self,game,x,y,'c')
            button=Button(game,x,y-50,"Play",callback=self.playClicked)
        
        def playClicked(self, event):
            self.game.initGame()
        
class Button(GameObject):
    def __init__(self,canvas,x,y,text,callback):
        GameObject.__init__(self,canvas,x,y,'c',callback)
        self.textId=canvas.create_text(x,y,text=text,anchor='c',fill='white')
        self.canvas.tag_bind(self.textId,'<Button-1>',callback)

class StoryTeller(GameObject):
	def __init__(self,canvas):
		x,y = canvas.width/2,canvas.height/2
		GameObject.__init__(self,canvas,x,y,'c')
		canvas.create_text(x,y,text="Shoot the wild animals before they eats your carrots! Click to start hunting.",anchor='c',fill='black', font='Purisa')

def main():
    game=GameWindow()
    root.mainloop()

if __name__ == "__main__":
	main()
