# encoding: utf-8
from gameobject import *
from button import *

class Menu(GameObject):
    def __init__(self,game,buttonTextCallbackTuples,title=None):
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
