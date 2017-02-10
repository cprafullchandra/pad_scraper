from error import ErrorHandler
from lxml import html
from lxml.etree import tostring
import requests
import re
import sys
from monster import Monster

class Scraper:
    """ Scraper class for parsing data from padx """
    pad_url = None
    monster_urls = None
    last = 0
    backup = None

    # XPath Macros
    # !! TODO - Bring macros here: requires add self. to all calls to them

    # !! TODO - Check for "dump.txt" on boot, pass to parse
    @ErrorHandler
    def __init__(self, index=0, url="http://www.puzzledragonx.com/en/",
                    page="http://www.puzzledragonx.com/en/monsterbook.asp",
                    backup="dump.txt"):
        """ Initializes class variables and starts the parsing process """
        print("Retrieving monsters from padx")
        self.backup = backup
        self.pad_url = url
        page = requests.get(page)
        tree = html.fromstring(page.content)
        hrefs = tree.xpath('//td[@class="index"]/div[@class="indexframe"]/a')

        monster_urls = {}
        for href in hrefs:
            monster_id = int(re.search('[0-9]+', href.attrib['href']).group(0))
            monster_urls[monster_id] = self.pad_url + href.attrib['href']

        self.monster_urls = monster_urls
        self.parse()

    @ErrorHandler
    def parse_url(self, mon_id):
        """ Parses the page of a specific monster entry """
        page = requests.get(self.monster_urls[mon_id])
        tree = html.fromstring(page.content)

        monster = Monster()

        ### Temp Location for macros
        avatar_d = 'div[@class="avatar"]'
        chart_d = 'div[@id="comparechart"]'
        content_d = 'div[@id="content"]'
        monster_d = 'div[@id="monster"]'
        name_d = 'div[@class="name"]'
        profile_d = 'div[@id="compareprofile"]'
        stars_d = 'div[@class="stars"]'
        evolve = 'span[@id="evolve"]'
        mpoint  = 'span[@title="Monster Point"]'

        tablestat = 'table[@id="tablestat"]'
        data    = 'td[@class="data"]'
        data_jp = 'td[@class="data jap"]'
        attack = 'td[text()="ATK"]'
        level = 'td[text()="Level"]'
        health = 'td[text()="HP"]'
        rcv = 'td[text()="RCV"]'

        img = 'img'
        sibling = 'following-sibling::td/'
        text = 'text()'

        ### Get monster information from tables
        monster.id = mon_id
        monster.image = self.pad_url + tree.xpath('//'+monster_d+'/a')[0].attrib['href']
        monster.avatar = self.pad_url + tree.xpath('//'+content_d+'/'+avatar_d+'/'+img)[0].attrib['src']

        ### Table 1 info
        monster.en_name = tree.xpath('//'+content_d+'/'+name_d+'//'+text)[0]
        monster.jp_name = tree.xpath('//'+content_d+'//'+data_jp+'/'+text)
        monster.type = tree.xpath('//'+content_d+'//td[@class="ptitle" and text()="Type:"]/../'+data+'/a/'+text)
        monster.element = tree.xpath('//'+content_d+'//td[@class="ptitle" and text()="Element:"]/../'+data+'/a/'+text)
        monster.rarity = int(tree.xpath('count(//'+content_d+'/'+stars_d+'/'+img+')'))
        monster.cost = int(tree.xpath('//'+content_d+'//td[@class="ptitle" and text()="Cost:"]/../'+data+'/a/'+text)[0])
        monster.monsterpoints = int(tree.xpath('//'+content_d+'//'+mpoint+'/../../'+data+'/'+text)[0])
        monster.expcurve = int(tree.xpath('//'+profile_d+'/'+tablestat+'//td[contains(.,"Growth Curve")]/a/'+text)[0].replace(',',''))
        monster.maxexp = int(re.search('[0-9]+',tree.xpath('//'+profile_d+'/'+tablestat+'//td[contains(.,"Exp to max")]/'+text)[0].replace(',','')).group(0))

        ### Table 3 info
        monster.minlvl = int(tree.xpath('//'+chart_d+'//'+level+'/'+sibling+text)[0])
        monster.maxlvl = int(tree.xpath('//'+chart_d+'//'+level+'/'+sibling+sibling+text)[0])
        monster.basehp = int(tree.xpath('//'+chart_d+'//'+health+'/'+sibling+text)[0])
        monster.maxhp = int(tree.xpath('//'+chart_d+'//'+health+'/'+sibling+sibling+text)[0])
        monster.baseatk = int(tree.xpath('//'+chart_d+'//'+attack+'/'+sibling+text)[0])
        monster.maxatk = int(tree.xpath('//'+chart_d+'//'+attack+'/'+sibling+sibling+text)[0])
        monster.basercv = int(tree.xpath('//'+chart_d+'//'+rcv+'/'+sibling+text)[0])
        monster.maxrcv = int(tree.xpath('//'+chart_d+'//'+rcv+'/'+sibling+sibling+text)[0])
        ### Weighted stats are HP/10 + ATK/5 + RCV/3
        # !! TODO - Are these always integer results or do we want decimals?
        monster.minweighted = monster.basehp/10 + monster.baseatk/5 + monster.basercv/3
        monster.maxweighted = monster.maxhp/10 + monster.maxatk/5 + monster.maxrcv/3

        ### Table 4 info
        monster.active_skill = tree.xpath('//'+content_d+'//td[@class="title value-normal nowrap" and text()="Active Skill:"]/'+sibling+'a/span/'+text)[0]
        monster.active_skill_description = tree.xpath('//'+content_d+'//td[@class="title" and text()="Effects:"]/'+sibling+text)[0]
        monster.active_skill_cooldown = tree.xpath('//'+content_d+'//td[@class="title" and text()="Cool Down:"]/'+sibling+text)[0]
        monster.same_active_skill = [re.search('[0-9]+', x.attrib['href']).group(0) for x in tree.xpath('//'+content_d+'//td[@class="title" and text()="Same Skill:"]/'+sibling+'a')]
        monster.leader_skill = tree.xpath('//'+content_d+'//td[@class="title value-normal nowrap" and text()="Leader Skill:"]/'+sibling+'a/span/'+text)[0]
        monster.leader_skill_description = tree.xpath('//'+content_d+'//td[@class="title" and text()="Effects:"]/'+sibling+text)[1]
        monster.awakenings = [re.search('^(.*?)(?=\r\n)', x.attrib['title']).group(0) for x in tree.xpath('//'+content_d+'//td[@class="awoken1"]/a/'+img)]

        ### Grab evolutions
        ### Grab the evolution and material rows
        evolution_rows = tree.xpath('//'+evolve+'/following-sibling::table//td[@class="evolve" or @class="awokenevolve"]/..')
        material_rows = tree.xpath('//'+evolve+'/following-sibling::table//td[@class="require" or @class="finalevolve nowrap" or @class="finalawokenevolve nowrap"]/..')

        ### Work through the first row to determine the base form for all subsequent evolution rows
        evo_row = evolution_rows[0]
        mat_row = material_rows[0]
        evolutions = evo_row.xpath('./td[@class="evolve" or @class="awokenevolve"]/div/div/text()')
        materials = [[re.search('[0-9]+', y.attrib['href']).group(0) for y in x.xpath('./a')] for x in mat_row.xpath('./td[@class="require" or @class="finalevolve nowrap" or @class="finalawokenevolve nowrap"]')]

        ### Create tuples for each evolution pair in the first row and save the last evolution to be used as the base for the subsequent rows
        evolution_tuples = []
        base = ""
        for i in range(len(evolutions)):
            if i == len(evolutions) - 1:
                base = evolutions[i]
            else:
                evolution_tuples.append((evolutions[i], materials[i], evolutions[i+1]))

        ### Work through all subsequent rows using the previously determined base form for the first evolution pair in each row
        for evo_row, mat_row in zip(evolution_rows[1:], material_rows[1:]):
            evolutions = evo_row.xpath('./td[@class="evolve" or @class="awokenevolve"]/div/div/text()')
            materials = [[re.search('[0-9]+', y.attrib['href']).group(0) for y in x.xpath('./a')] for x in mat_row.xpath('./td[@class="require" or @class="finalevolve nowrap" or @class="finalawokenevolve nowrap"]')]

            for i in range(len(evolutions)):
                if i == 0 and len(evolutions) == 1:
                    evolution_tuples.append((base, materials[i], evolutions[i]))
                elif i == 0 and len(evolutions) > 1:
                    evolution_tuples.append((base, materials[i], evolutions[i]))
                    evolution_tuples.append((evolutions[i], materials[i+1], evolutions[i+1]))
                elif i == len(evolutions) - 1:
                    evolution_tuples.append((evolutions[i], [], ""))
                else:
                    evolution_tuples.append((evolutions[i], materials[i], evolutions[i+1]))

        print(str(evolution_tuples))

        # id of last monster processed
        self.last = mon_id
        #monster.info()

        # !! TODO - should this return something for parse to store?

    @ErrorHandler
    def parse(self):
        """ Parses every monster link for information """
        print("Parsing monster information")

        # !! TODO - what are these used for?
        monster_image_urls = []
        max_val = 1
        monsters = []

        for mon_id in range(126,127):
            self.parse_url(mon_id)

    @ErrorHandler
    def __del__(self):
        with open(self.backup, 'w+') as f:
            f.write(str(self.last))

@ErrorHandler
def main(args):
    """ Instantiates the scraper which runs to completion """
    print(args)
    count = len(args)
    if count == 1:
        scraper = Scraper()
    elif count == 5:
        scraper = Scraper(index=args[1], url=args[2], page=args[3], backup=args[4])
    else:
        print("Invalid arguments.")
        sys.exit(1)

    print("Completed successfully. Last Entry: " + str(scraper.last))

if __name__ == '__main__':
    main(sys.argv)
