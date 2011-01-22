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

class ral(WebSvc):
	"""RAL"""

	content = ['swatchbook']

	about = u'These data come from the <a href="http://www.ral-farben.de/uebersicht-ral-classic-farben.html?&L=1">RAL CLASSIC</a> and <a href="http://www.ral-farben.de/uebersicht-ral-p1-farben.html?&L=1">RAL PLASTICS</a> colour names listed at RAL\'s website.<br /><br />RAL CLASSIC and RAL PLASTICS are registered trademarks of RAL gGmbH, 53757 Sankt Augustin.'

	nbLevels = 1
	urls = [('RAL CLASSIC','http://www.ral-farben.de/uebersicht-ral-classic-farben.html'),('RAL PLASTICS','http://www.ral-farben.de/uebersicht-ral-p1-farben.html')]

	def level0(self):
		palettes = SortedDict()
		palettes['0'] = self.urls[0][0]
		palettes['1'] = self.urls[1][0]
		return palettes 

	def read(self,swatchbook,palette):
		palette = eval(palette)
		webpage = urlopen(self.urls[palette][1]).read()
		data = webpage.split('<tbody>')[1].split('</tbody>')[0]
		data = data.split('<tr')[1:]
		swatchbook.info.title = self.urls[palette][0]

		i = 0
		for line in data:
			item = Color(swatchbook)
			item.usage.add('spot')
			if line.find(' style="BACKGROUND: rgb(') >= 0:
				line = line.split(' style="BACKGROUND: rgb(')[1]
				R,G,B = eval("["+line.split(');',1)[0]+"]")
				item.values[('sRGB',False)] = [R/0xFF,G/0xFF,B/0xFF]
				line = line.split('"')[1]
			line = line.replace(' <br />','')
			line = line.replace('&nbsp;',' ')
			line = line.split('><td><p>',1)[1].split('</p></td></tr>')[0]
			code,de,en,fr,es,it,nl = map(strip,line.split('</p></td><td><p>'))
			item.info.identifier = unicode(code)
			item.info.title = unicode(de,'UTF-8')
			item.info.title_l10n = {'de': unicode(de,'UTF-8'),'en': unicode(en,'UTF-8'),'fr': unicode(fr,'UTF-8'),'es': unicode(es,'UTF-8'),'it': unicode(it,'UTF-8'),'nl': unicode(nl,'UTF-8')}
			swatchbook.materials[code] = item
			swatchbook.book.items.append(Swatch(code))
			i += 1
