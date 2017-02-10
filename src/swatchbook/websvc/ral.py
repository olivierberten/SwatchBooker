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

	about = u'These data come from the <a href="http://www.ral-farben.de/uebersicht-ral-classic-farben.html?&L=1">RAL CLASSIC colour names</a> listed at RAL\'s website.<br /><br />RAL CLASSIC is registered trademarks of RAL gGmbH, 53757 Sankt Augustin.'

	nbLevels = 1
	url = 'http://web.archive.org/web/20120208005345/https://www.ral-farben.de/uebersicht-ral-classic-farben.html'

	def level0(self):
		return {'0': u'RAL CLASSIC'}

	def read(self,swatchbook,palette):
		webpage = urllib.urlopen(self.url).read()
		data = webpage.split('<!-- END WAYBACK TOOLBAR INSERT -->')[1].split('<tbody>')[1].split('</tbody>')[0]
		data = data.split('<tr')[1:]
		swatchbook.info.title = u'RAL CLASSIC'

		i = 0
		for line in data:
			item = Color(swatchbook)
			item.usage.append('spot')
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
