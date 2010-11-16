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

class alpina(WebSvc):
	"""Alpina"""
	
	content = ['swatchbook']

	about = u'These data come from Alpina\'s <a href="http://www.alpina-farben.de/colordesigner/">COLORdesigner</a> tool.<br /><br />© 2008 Alpina'

	nbLevels = 1
	
	url = "http://www.alpina-farben.de/colordesigner/"
	
	collections = {}

	def level0(self):
		collections = SortedDict()
		collections['Farben'] = SortedDict()
		collections['Farben']['ColorStick'] = 'ColorStick'
		collections['Farben']['ColorStudio'] = 'ColorStudio'
		collections['Lacke'] = SortedDict()
		collections['Lacke']['2in1'] = '2 in 1'
		collections['Lacke']['Kunstharz'] = 'Kunstharz'
		collections['LivingStyle'] = SortedDict()
		collections['LivingStyle']['LivingStyle Accent'] = 'Accent'
		collections['LivingStyle']['LivingStyle Atelier'] = 'Atelier'
		collections['LivingStyle']['LivingStyle Structur'] = 'Structur'
		collections['LivingWhite'] = SortedDict()
		collections['LivingWhite']['LivingWhite Glance'] = 'Glance'
		collections['LivingWhite']['LivingWhite Silhouette'] = 'Silhouette'
		collections['LivingWhite']['LivingWhite Silhouette GS'] = 'Silhouette Gold / Silver'
		return collections

	def read(self,swatchbook,coll):
		cols = {}
		cols['ColorStick'] = (3,1)
		cols['ColorStudio'] = (6,3)
		cols['2in1'] = (4,3)
		cols['Kunstharz'] = (4,3)
		cols['LivingStyle Accent'] = (2,3)
		cols['LivingStyle Atelier'] = (2,3)
		cols['LivingStyle Structur'] = (3,3)
		cols['LivingWhite Glance'] = (2,1)
		cols['LivingWhite Silhouette'] = (2,1)
		cols['LivingWhite Silhouette GS'] = (2,1)
		swatchbook.info.title = coll
		swatchbook.book.display['columns'] = cols[coll][0]
		file = urlopen(self.url+"xml/colorlist.xml")
		xml = etree.parse(file).getroot()
		file.close()
		alpina = {}
		for elem in xml:
			colors = []
			for subelem in elem:
				if subelem.tag == "NAME":
					name = subelem.text
				elif subelem.tag == "ARTCOLOR":
					color = {}
					for subsubelem in subelem:
						color[subsubelem.tag] = subsubelem.text
					colors.append(color)
			alpina[name] = colors
		for col in alpina[coll]:
			if col['COLNAME'] == "weiss" or (not col['COLNAME'] and col['COLRGB'] == "FFFFFF"):
				swatchbook.book.items.append(Spacer())
				continue
			elif 'COLGR' in col and col['COLGR']:
				item = Pattern(swatchbook)
				item.info.title = col['COLNAME'] or ''
				id = col['COLGR'].rsplit('/',1)[1]
				if not os.path.isdir(os.path.join(swatchbook.tmpdir,"patterns")):
					os.mkdir(os.path.join(swatchbook.tmpdir,"patterns"))
				urlretrieve(self.url+col['COLGR'],os.path.join(swatchbook.tmpdir,"patterns",id))
			elif col['COLRGB']:
				item = Color(swatchbook)
				item.values[('sRGB',False)] = [int(col['COLRGB'][0:2],16)/0xFF,int(col['COLRGB'][2:4],16)/0xFF,int(col['COLRGB'][4:],16)/0xFF]
				item.usage.add('spot')
				id = col['COLNAME'] or ''
			if id in swatchbook.materials:
				if item.values[item.values.keys()[0]] == swatchbook.materials[id].values[swatchbook.materials[id].values.keys()[0]]:
					swatchbook.book.items.append(Swatch(id))
					continue
				else:
					sys.stderr.write('duplicated id: '+id+'\n')
					if item.info.title == '':
						item.info.title = id
					id = id+idfromvals(item.values[item.values.keys()[0]])
			item.info.identifier = id
			swatchbook.materials[id] = item
			swatchbook.book.items.append(Swatch(id))
				
