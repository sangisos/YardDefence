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
    def __init__(self, **kwargs):
        
        # Runs in fullscreen
        root.attributes('-fullscreen', True)
        
        
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        Canvas.__init__(self, root, width=self.width, height=self.height, **kwargs)
        self.pack()
        
        root.update()
        
        self.menu() 
        
        
        
        
    def menu(self):
		self.level=1
		menu = Menu(self)
		self.initGame()


    def initGame(self):
		self.background=Background(self)
		self.activeEnemys=[]
		self.deadEnemys=[]
		self.after(0,self.doOneFrame)
		self.after(0,self.createEnemy)
        
    def createEnemy(self):
        self.activeEnemys.append(enemy2(self))
        self.after(randint(500/self.level,3000/self.level),self.createEnemy)
        
    
    def doOneFrame(self):
        # Commented for debug. Uncomment to loop: 
        self.after(30,self.doOneFrame)
        
        ### Skriv kod efter här för att visa en frame
        #Darth.enemyimg=["images/lifeIcon.gif"]
        
        
        
        
        
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
	def __init__(self,canvas):
		GameObject.__init__(self,canvas,500,500)
		
class StoryTeller(GameObject):
	def __init__(self,canvas):
		GameObject.__init__(self,canvas,500,500)
		

def main():
    game=GameWindow()
    root.mainloop()

if __name__ == "__main__":
	main()
