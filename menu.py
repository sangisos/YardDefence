# encoding: utf-8
from gameobject import *
from button import *

class Menu(GameObject):
    def __init__(self,game,buttonTextCallbackTuples,title=None):
        x,y=game.centerx,game.centery
        GameObject.__init__(self,game,x,y,'c')
        height=self.getHeight()
        if title:
            self.title=Text(game,x,y-height/3,text=title,color='white')
            y = y + self.title.getbboxHeight()/2
            
        # Place buttons
        buttonHeight=Button.getHeight()
        noOfButtons=len(buttonTextCallbackTuples)
        buttonAreaHeight=buttonHeight*noOfButtons*1.1
        ydiff=int(buttonAreaHeight/2)
        yjump=int(buttonAreaHeight/(len(buttonTextCallbackTuples)))
        ydeltas=range(-ydiff,ydiff,yjump-1)
        
        
        
        # Have to save one (and only one) ref to buttons, otherwise garbagecollected by python, if more than one, object will not be deleted
        self.buttons=[Button(game,x,y+ydelta,buttonText,callback=buttonCallback) for (buttonText,buttonCallback),ydelta in zip(buttonTextCallbackTuples,ydeltas)]
        
        
        
    def getButtonNumber(self,event):
        # HERE BE DRAGONS
        current = self.game.find_withtag(CURRENT)
        button = [self.buttons.index(button) for button in self.buttons if current[0] in [button.objectId, button.textObject.objectId]]
        return button[0] # Could fail if no object is found above, but the callback that triggers this method should only be called if the button or it's text is the 'current' object.
