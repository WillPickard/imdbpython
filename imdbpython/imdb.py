from extractors.genre import GenreExtractor
from extractors.movie import MovieFeaturedExtractor
from extractors.movie import MoviePageExtractor 

from bs4 import BeautifulSoup as Soup 
import requests

DS = "/"
BASE_URL = "http://www.imdb.com"
GENRE_URL = BASE_URL + DS + "genre"
DEBUG = True

def debug(msg):
	if DEBUG:
		print(msg) 

def get_http_headers():
	return  {
		'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
		'Connection' : 'keep-alive',
		'Referer' : 'https://www.google.com',
		'Cache-Control' : 'max-age=0',
		'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding' : 'gzip, deflate, sdch',
		'Accept-Language' : 'en-US,en;q=0.8'
	}

def get_soup(url):
	debug("Getting soup: " + url)
	return Soup(requests.get(url, headers=get_http_headers()).text)

genre_extractor = GenreExtractor()

genre_soup = get_soup(GENRE_URL)


genres = genre_extractor.extract(get_soup(GENRE_URL))

genre = genres[0]

url = genre.url

featured_extractor = MovieFeaturedExtractor()
movie_extractor = MoviePageExtractor()

featured = featured_extractor.extract(get_soup(url))

featuredmovie = featured[0]

url = "http://imdb.com" + featuredmovie.href

movie = movie_extractor.extract(featuredmovie.imdb_id, get_soup(url))
print("movie:")
print(movie)