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

class alcro(WebSvc):
	"""Alcro"""

	content = ['swatchbook']

	about = u'These data come from the <a href="http://alcro.colordream.com/">Alcro Designer</a> tool.<br /><br />© Alcro / MRM Starsky'

	nbLevels = 1
	url = "http://alcro.colordream.com/sv/palette/palettes/data/"

	collections = ['NCS',u'Färgsätt inomhus',u'Färgsätt utomhus']

	def level0(self):
		list0 = SortedDict()
		for i in range(len(self.collections)):
			list0[str(i)] = self.collections[i]
		return list0

	def read(self,swatchbook,coll):
		coll = int(coll)
		swatchbook.info.title = self.collections[coll]
		palettes = eval(urlopen(self.url).read().replace("true","True").replace("false","False"))
		if coll == 0:
			for groups in palettes["0"][0]['colors']:
				group = Group(groups['name'])
				for colors in groups['sc'][0]['colors']:
					color = Color(swatchbook)
					color.usage.add('spot')
					id = str(colors['k'])
					color.info.identifier = id
					color.info.title = colors['name']
					color.values[('sRGB',False)] = (colors['r']/0xFF,colors['g']/0xFF,colors['b']/0xFF)
					group.items.append(Swatch(id))
					swatchbook.materials[id] = color
				swatchbook.book.items.append(group)
		else:
			for groups in palettes[str(coll)]:
				group = Group(unicode(groups['name'],'utf-8'))
				for colors in groups['colors']:
					color = Color(swatchbook)
					color.usage.add('spot')
					id = str(colors['k'])
					color.info.identifier = id
					color.info.title = unicode(colors['name'],'utf-8')
					color.values[('sRGB',False)] = (colors['r']/0xFF,colors['g']/0xFF,colors['b']/0xFF)
					group.items.append(Swatch(id))
					swatchbook.materials[id] = color
				swatchbook.book.items.append(group)
				
		