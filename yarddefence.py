# encoding: utf-8
try:  # import as appropriate for 2.x vs. 3.x
    from tkinter import Tk,Canvas,Toplevel
except:
    from Tkinter import Tk,Canvas,Toplevel
from PIL import Image,ImageTk
import os
from random import randint



root=Tk()

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
    
class MetaGameObject(type):
    def __new__(mcs, classname, bases, dictionary):
        try:
            imageDir=os.curdir + os.sep + "images" + os.sep + str(classname)
            filenames=[os.path.join(imageDir, f) for f in os.listdir(imageDir) if f.endswith(".gif")]
            filenames.sort()
            dictionary["eliminatedImage"]=ImageTk.PhotoImage(image=Image.open(filenames.pop()))
            dictionary["enemyimg"] = [ImageTk.PhotoImage(image=Image.open(filename)) for filename in filenames]
        except:
            pass
        return type.__new__(mcs, classname, bases, dictionary)

class GameObject:
    '''All object that show pictures on screen should inherit the GameObjectclass'''
    __metaclass__=MetaGameObject
    
    def __init__(self, canvas):
        self.canvas=canvas
        self.imageID = canvas.create_image(canvas.width-50,randint(100,canvas.height-100),anchor="c",image=self.__class__.enemyimg[0])
        

class enemy2(GameObject):
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

def main():
	game=GameWindow()
	root.mainloop()

if __name__ == "__main__":
	main()
