# encoding: utf-8
from gameobject import *
from background import *
from text import *

class StoryTeller(GameObject):
	def __init__(self,game):
            game.level=game.level+1
            self.level1Text = "Dear Neighbour, \nYesterday my whole farm was attacked by a massive mob of \nWILD ANIMALS, they have eaten all my harvest. \nI am afraid that they are on their way to your farm right now. \nI hope you are prepared to protect your land! \n\nRegards,\nLennart"
            self.level2Text = "Oh my good, these animals are CRAZY! \nI have an idea, lets dig a river through our lands, \nmaybe that will keep the animals away. \n\nRegards, \nLennart"
            self.level3Text = "Looks like the river is to small for theese even \ncrazier animals. \nBut hey, I have an even CRAZIER idea. \nI have some dynamites in my basement, lets use them \nto blow up some more land. \nIm sure that will stop the animals from destroying our farms. \nGood luck! \n\nRegards, \nLennart"
            self.victoryText = "If you read this I assume that you are still alive \nand have defeated the CRAZY big boat of wild animals. \nI saw them, they loaded the boat with all the remainings \nof their army. Our farms are safe now. \nCongratulations! \n\nGreetings, \nLennart"
            self.storyTexts = [self.level1Text,self.level2Text,self.level3Text,self.victoryText]
            game.background=Background(game)
            x,y = game.width/2,game.height/2
            GameObject.__init__(self,game,x,y,'c',self.storyTellerOnClick)
            self.textObject=Text(game,x,y,text=self.storyTexts[game.level-1],callback=self.storyTellerOnClick,color='black',font=game.storyFont)
            
        def storyTellerOnClick(self,event):
            self.game.delete(self.objectId)
            del self.textObject
            self.game.initGame()
            
