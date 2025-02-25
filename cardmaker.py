
import requests, re, random

from bs4 import BeautifulSoup

# damage calculation
# https://bulbapedia.bulbagarden.net/wiki/Damage#Damage_calculation

HEALTH_COEFFICENT = 0.0001499027361861746
SPEED_COEFFICENT = 21680.725
ATTACK_COEFFICENT = 17557.15

class Card :
	def __init__(self, wiki_url: str) -> None:
		if not wiki_url.startswith("https://en.wikipedia.org/wiki/") :
			raise ValueError(f"Url '{wiki_url}' is not a wikipedia url!")

		page = requests.get(wiki_url)

		if not page.ok :
			raise ConnectionError(f"GET request failed with code {page.status_code}")

		soup = BeautifulSoup(page.text, "html.parser")

		title = str(soup.find("title"))
		self.name: str = title[7:-20]

		categories = [
			re.search("title=\".*\"", str(x)).group()[16:-1] for x in
			soup.find("div", attrs={
				"id": "mw-normal-catlinks"
			}).find("ul").find_all("li")
		]

		tags = re.findall("<.*>", page.text)
		tags = [x[1:x.find(" ")] for x in tags if not "/" in x]
		tags = [x for x in tags if not "<" in x and not "." in x]
		counter = {
			x: tags.count(x) for x in tags
		}

		counter = {
			x[0]: x[1] for x in
			sorted(counter.items(), key = lambda x: -x[1])
		}

		random.seed(wiki_url)

		# Type
		if len(categories) > 0 :
			self.type: str = categories.pop(random.randrange(0, len(categories)))
		else :
			self.type: str = "Normal"

		# Strengths
		if len(categories) > 0 :
			self.strength: str = categories.pop(random.randrange(0, len(categories)))
		else :
			self.strength: str = ""

		# Health
		self.health: int = round(len(page.text) * HEALTH_COEFFICENT)

		# Speed
		self.speed: int = round(len(page.text) / SPEED_COEFFICENT)

		sections = [
			re.search("<span>.*</span>", str(x)).group()[6:-7] for x in
			soup.find("ul", attrs={
				"id": "mw-panel-toc-list"
			}).find_all("li")[1:]
		]
		sections = [x for x in sections if x.lower() != "other" and len(x) <= 25]

		# Attacks
		base_atk = len(page.text) / ATTACK_COEFFICENT

		self.moves = []
		if len(sections) >= 4 :
			for i in range(4) :
				self.moves.append(
					(
						sections.pop(random.randrange(0, len(sections))),
						int(round(base_atk * random.randrange(70, 130) / 100 * 2, -1) / 2)
					)
				)
		elif len(sections) > 0 :
			self.moves.extend([
				(
					x,
					int(round(base_atk * random.randrange(70, 130) / 100 * 2, -1) / 2)
				)
				for x in sections
			])
		else :
			self.moves.append(("Struggle", 0))

		# Defence
		self.defence: int = counter["a"] if "a" in counter else 0

	def __str__(self) -> str:
		return f"""- {self.name} -
 Type: {self.type}
 Strength: {self.strength}

 Hp: {self.health}
 Def: {self.defence}

 Moves:
  {"\n  ".join([x[0] + " - " + str(x[1]) for x in self.moves])}"""
