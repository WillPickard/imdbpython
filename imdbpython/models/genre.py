from models.base import Base as BaseModel

class Genre(BaseModel):
	def __init__(self, name="", url=""):
		self.name = name
		self.url = url
		return
