#!/usr/bin/env python
# coding: utf-8
#
#       Copyright 2010 Olivier Berten <olivier.berten@gmail.com>
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

class caparol(WebSvc):
	"""Caparol"""
	
	content = ['swatchbook']

	about = u'These data come from Caparol\'s <a href="http://www.spectrum4.eu/desktopdefault.aspx?tabID=5960&lang=de">Spectrum</a> tool.<br /><br />© 1999-2009 Deutsche Amphibolin-Werke von Robert Murjahn Stiftung & Co KG. Alle Rechte vorbehalten.'

	nbLevels = 1
	url = "http://caparol2.active-online.de/spectrum/"
	locales = {'ba_ba':'bs','be_fr':'fr','cn_cn':'zh','cz_cz':'cs','de_de':'de','en_en':'en','es_es':'es','hr_hr':'hr','nl_nl':'nl','ro_ro':'ro','ru_ru':'ru','se_se':'sv'}
	locale = "de_de"
	lang = "de"
	wordlist = {}

	def level0(self):
		for l in self.locales:
			words = urlopen(self.url+l+"/get_language.php3").read()[14:]
			words = words.split(';')
			i = 0
			while i < len(words):
				word = words[i]
				if not word in self.wordlist:
					self.wordlist[word] = {}
				self.wordlist[word][self.locales[l]] = unquote_plus(words[i+1]).decode('utf8')
				i+=2
		collections = SortedDict()
		page = urlopen(self.url+self.locale+"/get_collection_data.php3").read()[19:]
		page = page.split('|')
		prods = SortedDict()
		for p in page:
			p = p.split(';')
			if p[2] in ('1','3'):
				if not p[0] in prods:
					prods[p[0]] = SortedDict()
				prods[p[0]][p[1]] = p[2:]
		for p in page:
			p = p.split(';')
			if p[2] == '2' and (p[0] in ("prod_%5BCaparol%5D","prod_%5BBASIC%5D") or (p[0] == "prod_%5BSynthesa%5D" and p[1] not in ("col_%5BSilverstyle_Syn%5D","col_%5BBuntsteinputz%5D")) or (p[0] == "prod_%5Bnora%5D" and p[1] == "col_%5Bnora%5D_%5Bnp+uni%5D")):
				if not p[0] in prods:
					prods[p[0]] = SortedDict()
				prods[p[0]][p[1]] = p[2:]
		for prod in prods:
			for col in prods[prod]:
				if not prod[8:-3] in collections:
					collections[prod[8:-3]] = SortedDict()
				collections[prod[8:-3]][str((prod,col,int(prods[prod][col][2]),int(prods[prod][col][3]),int(prods[prod][col][0])))] = self.wordlist[col][self.lang]
		return collections

	def read(self,swatchbook,coll):
		producer,collection,cols,rows,type = eval(coll)
		swatchbook.info.title = self.wordlist[collection][self.lang]
		for lang in self.wordlist[collection]:
			if self.wordlist[collection][lang] != swatchbook.info.title and (lang != 'en' and self.wordlist[collection][lang] != self.wordlist[collection]['en']):
				swatchbook.info.title_l10n[lang] = self.wordlist[collection][lang]
		swatchbook.book.display['columns'] = rows
		#swatchbook.book.display['rows'] = cols
		page = urlopen(self.url+self.locale+"/get_colorpicker_data2.php3?producer="+producer+"&collection="+collection).read()[20:]
		if page > '':
			page = page.split('|')
			groups = {}
			for p in page:
				dup = False
				p = p.split(';')
				id = unquote_plus(p[21]).decode('utf8')
				if type in (1,3) or int(p[6]) > 0:
					item = Color(swatchbook)
					item.values[('sRGB',False)] = [int(p[6])/0xFF,int(p[7])/0xFF,int(p[8])/0xFF]
					if p[9] > '':
						item.values[('LCH',False)] = [eval(p[9].replace('%2C','.')),eval(p[10].replace('%2C','.')),eval(p[11].replace('%2C','.'))]
					if id in swatchbook.materials:
						if item.values[('sRGB',False)] == swatchbook.materials[id].values[('sRGB',False)]:
							dup = True
						else:
							sys.stderr.write('duplicated id: '+id+'\n')
							id = id+str(item.toRGB8())
					item.usage.add('spot')
				else:
					item = Pattern(swatchbook)
					id = id+'.tif'
					if id in swatchbook.materials:
						dup = True
					else:
						if id.find('/') and not os.path.isdir(os.path.join(swatchbook.tmpdir,"patterns",id.rsplit('/',1)[0])):
							os.makedirs(os.path.join(swatchbook.tmpdir,"patterns",id.rsplit('/',1)[0]))
						urllib.urlretrieve(self.url+self.locale+"/picloader.php3?path=aoMappingTexturePath&imname="+quote_plus(id),os.path.join(swatchbook.tmpdir,"patterns",id))
				item.info.identifier = id
				item.info.title = unquote_plus(p[4]).decode('utf8')
				if p[13] > '':
					item.extra['LRV'] = p[13]
				if not dup:
					swatchbook.materials[id] = item
				if p[12] > '':
					if p[12] not in groups:
						group = Group(unquote_plus(p[12]).decode('utf8'))
						groups[p[12]] = group
						swatchbook.book.items.append(group)
					groups[p[12]].items.append(Swatch(id))
				else:
					swatchbook.book.items.append(Swatch(id))
