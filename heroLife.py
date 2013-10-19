from PIL import ImageTk, Image
from gameobject import GameObject

class HeroLife(GameObject):
	def __init__(self,canvas,x):
		GameObject.__init__(self,canvas,x,32,'c')
