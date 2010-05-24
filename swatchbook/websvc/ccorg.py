#!/usr/bin/env python
# coding: utf-8
#
#       Copyright 2008 Olivier Berten <olivier.berten@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#

from __future__ import division
from swatchbook.websvc import *
from cgi import parse_qs
from sgmllib import SGMLParser

class MyParser(SGMLParser):
	"A simple parser class."

	def parse(self, s):
		"Parse the given string 's'."
		self.feed(s)
		self.close()

	def __init__(self, verbose=0):
		"Initialise an object, passing 'verbose' to the superclass."

		SGMLParser.__init__(self, verbose)
		self.hyperlinks = []
		self.descriptions = []
		self.inside_a_element = 0
		self.starting_description = 0

	def start_a(self, attributes):
		"Process a hyperlink and its 'attributes'."

		for name, value in attributes:
			if name == "href":
				self.hyperlinks.append(value)
				self.inside_a_element = 1
				self.starting_description = 1

	def end_a(self):
		"Record the end of a hyperlink."

		self.inside_a_element = 0

	def handle_data(self, data):
		"Handle the textual 'data'."

		if self.inside_a_element:
			if self.starting_description:
				self.descriptions.append(data)
				self.starting_description = 0
			else:
				self.descriptions[-1] += data

	def get_hyperlinks(self):
		"Return the list of hyperlinks."

		return self.hyperlinks

	def get_descriptions(self):
		"Return a list of descriptions."

		return self.descriptions

class ccorg(WebSvc):
	"""ColorCharts.org"""
	
	content = ['swatchbook']

	about = u'Copyright 2000 - 2007 Colorcharts.org, All Rights Reserved'

	nbLevels = 3
	url = "http://www.colorcharts.org/ccorg/"

	@staticmethod
	def parse_deck(str):
		"""Parse the string into a dictionary"""
		str = parse_qs(str)
		rows = str['rows'][0]
		colours = str['c'][0]
		names = unicode(str['n'][0].split('^')[0],'utf8')
		cbn = str['n'][0].split('^')[6]
		stars = str['n'][0].split('^')[7][0]
		outofgamut =  str['n'][0].split('^')[8]
		return {'rows': rows, 'stars': stars, 'colours': colours, 'names': names, 'cbn': cbn, 'outofgamut': outofgamut}

	@staticmethod
	def merge_decks(deck1, deck2):
		"""Merge 2 decks into one"""
		return {'rows': deck1['rows'], 'stars': deck1['stars'], 'colours': deck1['colours']+'~'+deck2['colours'], 'names': deck1['names']+'~'+deck2['names'], 'cbn': deck1['cbn']+'~'+deck2['cbn'], 'outofgamut': deck1['outofgamut']+'~'+deck2['outofgamut']}

	def level0(self):
		categories = SortedDict()
		page = urllib.urlopen(self.url).read()

		cats = page.partition('<ul id="cats">')
		cats = cats[1]+cats[2]
		cats = cats.partition('</ul>')
		cats = cats[0]+cats[1]
		p = MyParser()
		p.parse(cats)
		for i in range(len(p.get_hyperlinks())):
			categoryid = p.get_hyperlinks()[i].split('categoryid=')[1]
			categories[categoryid] = xmlunescape(p.get_descriptions()[i])
		
		return categories

	def level1(self,cat):
		companies = SortedDict()
		page = urllib.urlopen(self.url+"resources/companies.aspx?categoryid="+cat).read()

		if page.find('ctl00_mainbody_DigCertList'):
			DigCertList = page.partition('<table id="ctl00_mainbody_DigCertList"')
			DigCertList = DigCertList[1]+DigCertList[2]
			DigCertList = DigCertList.partition('</table>')
			DigCertList = DigCertList[0]+DigCertList[1]
		else:
			DigCertList = ''

		if page.find('ctl00_mainbody_CompanyList'):
			CompanyList = page.partition('<table id="ctl00_mainbody_CompanyList"')
			CompanyList = CompanyList[1]+CompanyList[2]
			CompanyList = CompanyList.partition('</table>')
			CompanyList = CompanyList[0]+CompanyList[1]
		else:
			CompanyList = ''

		str = DigCertList+CompanyList
		
		p = MyParser()
		p.parse(str)
		for i in range(len(p.get_hyperlinks())):
			id = p.get_hyperlinks()[i].rsplit('=')[1]
			if id not in companies:
				companies[id] = xmlunescape(p.get_descriptions()[i])

		return companies

	def level2(self,companyid):
		collections = SortedDict()
		page = urllib.urlopen(self.url+"resources/colors.aspx?companyid="+companyid).read()

		dlProducts = page.partition('<table id="ctl00_mainbody_dlProducts"')
		dlProducts = dlProducts[1]+dlProducts[2]
		dlProducts = dlProducts.partition('</table>')
		dlProducts = dlProducts[0]+dlProducts[1]
		p = MyParser()
		p.parse(dlProducts)
		for i in range(len(p.get_hyperlinks())):
			companyid = p.get_hyperlinks()[i].split('companyid=')[1].split('&lineid=')[0]
			lineid = p.get_hyperlinks()[i].split('&lineid=')[1]
			collections[str((companyid,lineid))] = xmlunescape(p.get_descriptions()[i])

		return collections

	def read(self,swatchbook,coll):
		companyid,lineid = eval(coll)
		url = self.url+"resources/colors.aspx?companyid="+companyid+"&lineid="+lineid
		page = urllib.urlopen(url).read()
		data = page.split('ReceiveServerData("fandeck^&')[1].split('");</script>')[0]
		deck = ccorg.parse_deck(data)

		if 'Page: 1 of ' in page:
			pages = page.split('Page: 1 of ')[1].split('</td><td><input')[0]
			
			for i in range(1,int(pages)):
				viewstate = page.split('__VIEWSTATE" value="')[1].split('" />')[0]
				sock = urllib.urlopen(url +'&'+urllib.urlencode({'__VIEWSTATE': viewstate})+'&ctl00%24mainbody%24Pager1%24Next.x=7&ctl00%24mainbody%24Pager1%24Next.y=7')
				page = sock.read()
				sock.close()
				data = page.split('ReceiveServerData("fandeck^&')[1].split('");</script>')[0]
				deck = ccorg.merge_decks(deck, ccorg.parse_deck(data))

		deck['company'] = page.split('<h1>')[1].split('</h1>')[0]
		deck['collection'] = page.split('selected" value="')[1].split('">',1)[1].split('</option>')[0]
		deck['colours'] = deck['colours'].split('~')
		deck['names'] = deck['names'].split('~')
		deck['cbn'] = deck['cbn'].split('~')
		deck['outofgamut'] = deck['outofgamut'].split('~')
		cert = {'5': 'Product samples scanned on our UV/VIS Spectrophotometer',
				'4': 'Fandecks scanned on our UV/VIS Spectrophotometer',
				'3': 'Fandecks scanned on a X-Rite CFS-57 Spectrophotometer',
				'2': 'Samples based on RGB values as provided by manufacturer',
				'1': 'Samples determined from existing web display'}
		swatchbook.info.title = xmlunescape(deck['company']+" - "+deck['collection'])
		swatchbook.info.description = 'Colorcharts.org certification: '+'*'*int(deck['stars'][:1])+'\n'+cert[deck['stars'][:1]]
		swatchbook.book.display['columns'] = int(deck['rows'])
		
		for i in range(len(deck['colours'])):
			item = Color(swatchbook)
			item.usage.append('spot')
			rgb = deck['colours'][i]
			item.values[('sRGB',False)] = [int(rgb[0:2],16)/0xFF,int(rgb[2:4],16)/0xFF,int(rgb[4:],16)/0xFF]
			if deck['names'][i] not in swatchbook.swatches:
				id = deck['names'][i]
			else:
				if item.values[('sRGB',False)] == swatchbook.swatches[deck['names'][i]].values[('sRGB',False)]:
					swatchbook.book.items.append(Swatch(id))
					continue
				else:
					sys.stderr.write('duplicated id: '+deck['names'][i]+'\n')
					item.info.title = deck['names'][i]
					id = str(item.toRGB8())
			item.info.identifier = id
			item.extra['CBN'] = deck['cbn'][i]
			item.extra['outofgamut'] =  str(abs(int(deck['outofgamut'][i])))
			swatchbook.swatches[id] = item
			swatchbook.book.items.append(Swatch(id))
