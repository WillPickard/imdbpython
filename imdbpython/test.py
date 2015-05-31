from bs4 import BeautifulSoup as Soup 
import requests

url = "http://www.imdb.com/title/tt0133093/?ref_=fn_al_tt_1"
soup = Soup(requests.get(url).text)
names = []
for prop in soup.find_all("span", class_="itemprop"):
	if prop.has_attr("itemprop") and prop.attrs["itemprop"] == "name":
		names.append((prop.attrs["itemprop"], prop.get_text()))

print(names)