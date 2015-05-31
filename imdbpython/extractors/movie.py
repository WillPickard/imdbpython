from extractors.base import Extractor as BaseExtractor
from models.movie import Movie 
from models.movie import FeaturedMovie

def debug(msg=""):
	print("MovieExtractor ... " , msg)

# Class to extract movies from pages with > 1
class MovieFeaturedExtractor(BaseExtractor):
	def __init__(self):
		BaseExtractor.__init__(self)

		self.models_props = [
			"imdb_id",
			"title",
			"href"
		] 

		self.entity_access_path = [
			"#main",
			"table.results",
			"td.title"
		]

		self.model_prop_access_paths = {
			"imdb_id" : [
				"span",
				"[data-tconst]"
			],
			"title" : [
				"a",
				"text"
			],
			"href" : [
				"a",
				"[href]"
			],
		}

	def extract(self, soup):
		data = BaseExtractor.extract(self, soup)

		data = list(map(lambda a: 
			FeaturedMovie(href=a["href"], title=a["title"],  imdb_id=a["imdb_id"]
		), data))
		return data 


# Class to extract movies from dedicated movie pages
class MoviePageExtractor(BaseExtractor):
	
	def __init__(self):
		BaseExtractor.__init__(self)
		self.models_props = [
			"imdb_id",
			"title",
			"rating",
			"duration",
			"genres",
			"release_date",
			"imdb_rating",
			"meta_rating",
			"directors",
			"actors",
			"writes",
			"storyline",
			"keywords",
			"taglines",
			"budget"
		]

		self.entity_access_path = [
			"#pagecontent"
		]

		self.model_prop_access_paths = {
			"title" : [
				"#overview-top",
				"h1.header",
				"span.itemprop",
				"text"
			],
			"rating" : [
				"#overview-top",
				"div.infobar",
				"meta",
				"text"
			],
			"duration" : [
				"#overview-top",
				"div.infobar",
				"time",
				"[datetime]"
			],
			"genres" : [
				"#overview-top",
				"div.infobar",
				"a"
			],
			"release_date" : [
				"#overview-top",
				"div.infobar",
				"span.nobr",
				"a",
				"meta",
				"[content]"
			],
			"imdb_rating" : [
				"#overview-top",
				"div.star-box-giga-star",
				"text",
			],	
		#	"meta_rating",
			"directors" : [
				"#overview-top",
				"div.text-block",
			],
			"actors",
			"writes",
			"storyline",
			"keywords",
			"taglines",
			"budget"
		}

		return

	# we will need to do it purselves
	def extract(self, imdb_id, soup):
		url = "http://www.imdb.com/title/" + imdb_id

		movie = Movie(imdb_id=imdb_id, url=url)

		overview = soup.find(id="#overview-top")

		title = overview.find_all("h1", class_="header")
		infobar = overview.find_all("div", class_="infobar")
		starbox = overview.find_all("div", class_="star-box")

		if len(title) > 0:
			spans = title.find_all("span")
			if len(spans) == 2:
				movie.title = spans[0].get_text()

		if len(infobar) > 0:
			infobar = infobar[0]
			metas = infobar.find_all("meta")
			spans = infobar.find_all("span")
			times = inforbar.find_all("time")

			for meta in metas:
				if meta.has_attr("itemprop"):
					itemprop = meta.get("itemprop")

					if itemprop == "contentRating":
						movie.rating = meta.get("content")

					elif itemprop == "datePublished":
						movie.release_date = meta.get("content")

			for span in spans:
				if span.has_attr("itemprop"):
					itemprop = span.get("itemprop")

					if itemprop == "genre":
						movie.genres.append(meta.span.get_text())

			for time in times:
				if time.has_attr("itemprop"):
					itemprop = time.get("itemprop")

					if itemprop == "duration":
						movie.duration = time.get("datetime")

		if len(starbox) > 0:
			starbox = starbox[0]

			gigastar = starbox.find_all("div", class_="star-box-giga-star")

			if len(gigastar) > 0:
				movie.imdb_rating = gigastar[0].get_text()

			movie.review_links["imdb"] = url + "/" + "reviews"
			movie.review_links["external"] = url + "/" + "externalreviews"
			movie.review_links["critic"] = url + "/criticreviews"

		

			
		return movie


