from PIL import ImageTk, Image

class HeroLife(ImageTk.PhotoImage):
	imageobj = Image.open("images/lifeIcon")
	image = ImageTk.PhotoImage.__init__(imageobj)
	lifes=0
	positionX = window.width/2
	def __init__(self,window):
		HeroLife.lifes=heroLife.lifes+1
		self.life=heroLife.lifes
		self.window = window
		self.imageId = window.create_image(HeroLife.positionX + self.life*30,40,HeroLife.image)
		
	def __del__(self):
		self.window.delete(self.imageId)
		ImageTk.PhotoImage.__del__(self)
		HeroLife.lifes=HeroLife.lifes-1