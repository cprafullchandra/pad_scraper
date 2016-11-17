from lxml import html
import requests

page = requests.get("http://www.puzzledragonx.com/en/monsterbook.asp")
tree = html.fromstring(page.content)

hrefs = tree.xpath('//td[@class="index"]/div[@class="indexframe"]/a')
#monsters = monsters[-1]

monsterlinks = []
for href in hrefs:
	monsterlinks.append("http://www.puzzledragonx.com/en/" + href.attrib['href'])

print monsterlinks