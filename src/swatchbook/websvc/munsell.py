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

class munsell(WebSvc):
	"""Munsell"""

	content = ['swatchbook']

	about = u'These data come from Munsell Color Science Laboratory\'s <a href="https://www.rit.edu/cos/colorscience/rc_munsell_renotation.php">Munsell Renotation Data</a>. None of these data should be confused with actual measurements from a Munsell Book of Color!<br /><br />Copyright 2010 RIT Munsell Color Science Laboratory. All rights reserved.'

	nbLevels = 1
	url = 'http://www.rit-mcsl.org/MunsellRenotation/'

	palettes = SortedDict()
	palettes['1929'] = '1929 Book of Colors'
	palettes['real'] = 'Visible range'
	palettes['all'] = 'Full range'
	
	def level0(self):
		return self.palettes

	def read(self,swatchbook,palette):
		file = urlopen(self.url+palette+'.dat').readlines()[1:]
		swatchbook.info.title = "Munsell - "+self.palettes[palette]
		cp = False
		cols = 0
		for line in file:
			swatchbook.book.display['columns'] = max(swatchbook.book.display['columns']or 0,cols) 
			c = line.split()
			if cp and (c[0] != cp[0] or c[1] != cp[1]):
				swatchbook.book.items.append(Break())
				cols = 0
			item = Color(swatchbook)
			id = c[0]+' '+c[1]+'/'+c[2]
			item.values[('xyY',False)] = (eval(c[3]),eval(c[4]),eval(c[5]))
			item.usage.add('spot')
			item.info.identifier = id
			swatchbook.materials[id] = item
			swatchbook.book.items.append(Swatch(id))
			cp = c
			cols += 1
