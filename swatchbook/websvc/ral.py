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

	type = 'list'
	nbLevels = 1
	url = 'http://www.ral-farben.de/uebersicht-ral-classic-farben.html'

	def level0(self):
		return {'0': u'RAL CLASSIC'}

	def read(self,swatchbook,palette):
		webpage = urllib.urlopen(self.url).read()
		data = webpage.split('<tbody>')[1].split('</tbody>')[0]
		data = data.split('<tr')[1:]
		swatchbook.info.title = u'RAL CLASSIC'

		swatch = []
		i = 0
		for line in data:
			item = Color(swatchbook)
			if line.find(' style="background: rgb(') >= 0:
				line = line.split(' style="background: rgb(')[1]
				R,G,B = eval("["+line.split(') none repeat scroll 0% 0%; -moz-background-clip: border; -moz-background-origin: padding; -moz-background-inline-policy: continuous;')[0]+"]")
				item.values[('sRGB',False)] = [R/0xFF,G/0xFF,B/0xFF]
				line = line.split(';"')[1]
			line = line.replace('                         <br />                         ','')
			line = line.split('>                     <td><p>                         ',1)[1].split('                     </p></td>                 </tr>             ')[0]
			code,de,en,fr,es,it,nl = line.split('                     </p></td>                     <td><p>                         ')
			item.info.identifier = unicode(code)
			item.info.title = unicode(de,'UTF-8')
			item.info.title_l10n = {'de': unicode(de,'UTF-8'),'en': unicode(en,'UTF-8'),'fr': unicode(fr,'UTF-8'),'es': unicode(es,'UTF-8'),'it': unicode(it,'UTF-8'),'nl': unicode(nl,'UTF-8')}
			swatchbook.swatches[code] = item
			swatchbook.book.items.append(Swatch(code))
			i += 1			
