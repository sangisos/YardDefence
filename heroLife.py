from PIL import ImageTk, Image
from gameobject import GameObject

class HeroLife(GameObject):
	lifes=0
	def __init__(self,x,y):
		#imageobj = Image.open("images/lifeIcon.gif")
		#image = ImageTk.PhotoImage.__init__(imageobj)
		HeroLife.lifes=heroLife.lifes+1
		self.life=heroLife.lifes
		#self.window = window
		#self.imageId = window.create_image(HeroLife.positionX + self.life*30,40,HeroLife.image)
		
	#def __del__(self):
		#self.window.delete(self.imageId)
		#ImageTk.PhotoImage.__del__(self)
		#HeroLife.lifes=HeroLife.lifes-1