from PIL import ImageTk, Image
from gameobject import GameObject

class HeroLife(GameObject):
	def __init__(self,canvas,x):
		GameObject.__init__(self,canvas,x,32,'c')
		
	#def __del__(self):
		#self.window.delete(self.imageId)
		#ImageTk.PhotoImage.__del__(self)
		#HeroLife.lifes=HeroLife.lifes-1