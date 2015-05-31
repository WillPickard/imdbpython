
import string

class Extractor(object):

	def __init__(self):
		self.models_props = []
		self.entity_access_path = []
		self.model_prop_access_paths = {}
		return

	def extract(self, soup):
#		print("model props: " , self.models_props)
#		print("entity_access_path: ", self.entity_access_path)
#		print("model prop access paths: ", self.model_prop_access_paths)
		entities = []
#		soup_entities = self.follow_path(self.entity_access_path, soup)
#		print(soup_entities)
		for soup_entity in self.follow_path(self.entity_access_path, soup):
			#print(soup_entity)
#			print("entity:")
#			print(soup_entity)
			entity = {}
			for prop, path in self.model_prop_access_paths.items():
				# just get the text

				if path == "text":
					entity[prop] = soup_entity.get_text()
					continue

				# if it's a list then we need to treat it like a path

				elif type(path) is list:
					# print(prop, " :")
					# print(self.follow_path(path, soup_entity))
					target = self.follow_path(path, soup_entity)
					
					# print(target)
					# if its a list then multiple values found, trust that the 1st element is correct
					while (type (target) is list and len(target) > 0) or target.__class__.__name__ == "ResultSet":
						target = target[0]
					# print(type(target))
					# print(target)
					# print("--")
					# print(prop , " : " , target)
					entity[prop] = target

				# otherwise we have the entity we want to extract the values from

				else:	
					s = Selector(path)

					value = self.resolve_selector(s, soup_entity)

					if value:
						entity[prop] = value

			entities.append(entity)
			# print("-")

#		print(entities)
		return entities

	def follow_path(self, path=[], soup=None):
#		print("following path: " , path)

		# if spaces are present in the path then split them 
		t = []
		for s in path:
			splt = s.split()
			t += splt
		path = t

		results = [soup]
		for s in path:
			for soup in results:
				temp = []
			#	soup = results.pop()

				soup_class = soup.__class__.__name__

			#	print(soup_class)

				selector = Selector(s)

				if soup_class == "ResultSet":
					for result in soup:
						r = self.resolve_selector(selector, result)
			#			print("r: " , r)
						if r is not None:
							r_class = r.__class__.__name__

							if r_class == "ResultSet":
								temp += r 
							else:
								temp.append(r)
				
				#elif soup_class == "BeautifulSoup":
				elif hasattr(soup, "find") or hasattr(soup, "find_all"):
			#		print("+")
					soup = self.resolve_selector(selector, soup)

					# if soup.__class__.__name__ == "ResultSet":
					# 	temp += soup
					# else:
					# 	temp.append(soup)
					temp.append(soup)

			#	else:
			#		print("?")

				results = temp

		return results

	def resolve_selector(self, selector, soup):
		s = selector.s()
		# print("resolving selector: " , s)
		if selector.is_id():
		#	print("ID! ", s, " - ", selector.get_id())
			i = selector.get_id()
			return soup.find(id=i)

		if selector.is_text():
			return soup.get_text()

		if selector.is_tag():
			tagname = selector.get_tag_name()
#			print("TAG! ", s, " - ", tagname)
			if selector.is_class():
				classname = selector.get_class_name()
#				print("\tAND CLASS! ",  s, " - ", classname)
				soup = soup.find_all(tagname, class_=classname)

				return soup
			return soup.find_all(tagname)

		if selector.is_class():
			classname = selector.get_class_name()
			# how can we get the classnames with a tagname?
			return soup.find_all("div", class_=classname)

		if selector.is_attr():
			attr = selector.get_attr_name()
#			print("attr name: ", attr)
			if hasattr(soup, "has_attr") and soup.has_attr(attr):
				return soup.get(attr)



# helper class
class Selector:
	def __init__(self, selector=""):
		self.selector = selector

	# For typing reasons
	def s(self):
		return self.selector

	def is_text(self):
		return self.selector == "text"

	def is_id(self):
		s = self.selector
		if len(s) > 0:
			return s[0] == "#"
		else:
			return False

	def get_id(self):
		s = self.s()
		ii = s.find("#")
		name = ""

		if ii >= 0:
			s = s[ii + 1:]
			for c in s:
				if c == "[" or c == "]" or c == ".":
					break
				name += c
		return name


	def is_class(self):
		s = self.s()
		return s.find(".") >= 0

	def get_class_name(self):
		s = self.s()
		name = ""
		pi = s.find(".")

		if pi >= 0:
			s = s[pi + 1:]

			for c in s:
				if c == "[" or c == "]" or c == ".":
					break
				name += c
		return name.strip()


	def is_attr(self):
		return len(self.get_attr_name()) > 0

	def is_tag(self):
		s = self.selector
	
		if len(s) > 0:
			alph = string.ascii_lowercase
			s = s[0].lower()
			return alph.find(s) >= 0

		else:
			return False

	def get_attr_name(self):
		s = self.selector
		if len(s) > 1:
			# attrs are of form [attr_name]
			i1 = s.find("[")
			i2 = s.find("]")
			if i1 >= 0 and i2 >= 0:
				return s[i1+1:i2]
		
		return ""

	def get_tag_name(self):
		s = self.s()
		name = ""
		if len(s) > 0:
			for c in s:
				if c == "[" or c == "]" or c == "." or c == "#":
					break
				name += c

		return name.strip()