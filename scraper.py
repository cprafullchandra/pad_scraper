from lxml import html
import requests
import re
import sys
from monster import Monster

print("Retrieving monsters from padx")
pad_url = "http://www.puzzledragonx.com/en/"
page = requests.get("http://www.puzzledragonx.com/en/monsterbook.asp")
tree = html.fromstring(page.content)

hrefs = tree.xpath('//td[@class="index"]/div[@class="indexframe"]/a')

monster_urls = {}
for href in hrefs:
	monster_id = int(re.search('[0-9]+', href.attrib['href']).group(0))
	monster_urls[monster_id] = pad_url + href.attrib['href']

### loop over every monster link
print("Parsing monster information")

monster_image_urls = []
max = 1
monsters = []
for mon_id in range(2972,2973):
	page = requests.get(monster_urls[mon_id])
	tree = html.fromstring(page.content)

	monster = Monster()
	# get monster image url
	monster.id = mon_id
	monster.image = pad_url + tree.xpath('//div[@id="monster"]/a')[0].attrib['href']
	monster.avatar = pad_url + tree.xpath('//div[@id="content"]/div[@class="avatar"]/img')[0].attrib['src']
	monster.name = tree.xpath('//div[@id="content"]/div[@class="name"]//text()')[0]
	monster.rarity = int(tree.xpath('count(//div[@id="content"]/div[@class="stars"]/img)'))
	monster.type = tree.xpath('//div[@id="content"]//td[@class="ptitle" and text()="Type:"]/../td[@class="data"]/a/text()')

	# Only care about tables 1, 3, and 4
	monster.info()
