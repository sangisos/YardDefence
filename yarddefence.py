# encoding: utf-8
try:  # import as appropriate for 2.x vs. 3.x
    from tkinter import Tk,Canvas,Toplevel
except:
    from Tkinter import Tk,Canvas,Toplevel
from PIL import Image,ImageTk
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
        self.setBackground()
        
    
    def setBackground(self):
        filename = "images/background" + str(self.level) + ".gif"
        
        self.bgImageObj = Image.open(filename)
        
        rezisedImageObj = self.bgImageObj.resize((self.width, self.height), Image.ANTIALIAS)
        
        self.bgImage = ImageTk.PhotoImage(rezisedImageObj)
        
        self.bgImageID = self.create_image(0,0,anchor="nw",image=self.bgImage)
        self.tag_lower(self.bgImageID)
        
        root.update()
    
    '''	
    def resizeBackground(self):
        print "resizeBg "+str(self.getWidth()) + " " + str(time.clock())
        self.delete(self.bgImageID)
        
        rezisedImageObj = self.bgImageObj.resize((self.getWidth(), self.getHeight()), Image.ANTIALIAS)
        
        self.bgImage = ImageTk.PhotoImage(rezisedImageObj)
        
        self.bgImageID = self.create_image(0,0,anchor="nw",image=self.bgImage)
        self.tag_lower(self.bgImageID)
        '''
    
    def removeBackground(self):
        self.delete(self.bgImageID)
        del self.bgImageID
        del self.bgImage
	




def main():
	game=GameWindow()
	root.mainloop()

if __name__ == "__main__":
	main()
