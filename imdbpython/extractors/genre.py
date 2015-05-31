from extractors.base import Extractor as BaseExtractor
from models.genre import Genre 

def debug(msg=""):
	print("GenreExtractor ... " , msg)
class GenreExtractor(BaseExtractor):
	
	def __init__(self):
		BaseExtractor.__init__(self)
		self.models_props = ["name", "url"]

		self.entity_access_path = [
			"#main", 
			"table.splash",
			"a"
		]

		self.model_prop_access_paths = {
			"name" : "text",
			"url" : "[href]"
		}

		return

	def extract(self, soup):
		data = BaseExtractor.extract(self, soup)
	#	debug("returned from BaseExtractor: " + str(data))

		genres = []

		for entity in data:
			name = entity["name"] if "name" in entity else ""
			url = entity["url"] if "url" in entity else ""

			# format url to fully qualified

			url = url.replace("http://imdb.com/", "")
			if url[0] == "/":
				url = url[1:]
			url = "http://imdb.com/" + url

			genres.append(Genre(name=name, url=url))

			
		return genres


