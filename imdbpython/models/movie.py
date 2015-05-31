from models.base import Base as BaseModel

class FeaturedMovie(BaseModel):
	def __init__(self, title="", href="", imdb_id=""):
		self.title = title
		self.href = href
		self.imdb_id = imdb_id



class Movie(BaseModel):
	def __init__(self, imdb_id="", title="", url="", rating="", duration="", genres=[], 
				release_date="", imdb_rating=0, meta_rating=0, review_links={}, directors=[], writers=[], 
				actors=[], storyline="", keywords=[], taglines=[], budget=0):
			self.imdb_id = imdb_id
			self.title = title
			self.url = url
			self.rating = rating
			self.duration = duration
			self.genres = genres
			self.release_date = release_date
			self.imdb_rating = imdb_rating
			self.meta_rating = meta_rating
			self.directors = directors
			self.writers = writers
			self.actors = actors
			self.storyline = storyline
			self.keywords = keywords
			self.taglines = taglines 
			self.budget = budget
			self.review_links = review_links

			self.accessor_map = {
				"imdb_id" : "",
				"title" : "",
				"url" : "",
				"rating" : "",
				"duration" : "",
				"genres" : "",
				"release_date" : "",
				"imdb_rating" : "",
				"meta_rating" : "",
				"directors": "",
				"writers" : "writers", 
				"actors" : "",
				"storyline" : "",
				"keywords" : "",
				"taglines" : "",
				"budget" : ""
			}
