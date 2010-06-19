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
from swatchbook.codecs import *

class autocad_acb(SBCodec):
	"""AutoCAD Color Book"""
	ext = ('acb',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag == 'colorBook':
			return True
		else:
			return False

	@staticmethod
	def read(swatchbook,file):
		xml = etree.parse(file).getroot()
		swatchbook.info.title = unicode(list(xml.getiterator('bookName'))[0].text)
		if len(list(xml.getiterator('majorVersion'))) > 0:
			swatchbook.info.version = list(xml.getiterator('majorVersion'))[0].text+'.'+list(xml.getiterator('minorVersion'))[0].text
		nbcolors = len(list(xml.getiterator('colorEntry')))
		for colorPage in xml.getiterator('colorPage'):
			swatchbook.book.display['columns'] = max(swatchbook.book.display['columns'],len(list(colorPage.getiterator('colorEntry'))))
		encrypted = False
		i = 0
		for colorPage in xml.getiterator('colorPage'):
			for colorEntry in colorPage.getiterator('colorEntry'):
				item = Color(swatchbook)
				if colorEntry.find('RGB8Encrypt'):
					encrypted = True
				elif colorEntry.find('RGB8'):
					item.values[('RGB',False)] = [eval(colorEntry.find('RGB8').find('red').text)/0xFF,eval(colorEntry.find('RGB8').find('green').text)/0xFF,eval(colorEntry.find('RGB8').find('blue').text)/0xFF]
				item.usage.append('spot')
				id = unicode(colorEntry.find('colorName').text)
				if id in swatchbook.materials:
					if len(item.values) > 0 and item.values[item.values.keys()[0]] == swatchbook.materials[id].values[swatchbook.materials[id].values.keys()[0]]:
						swatchbook.book.items.append(Swatch(id))
						i += 1
						continue
					else:
						sys.stderr.write('duplicated id: '+id+'\n')
						item.info.title = id
						id = str(item.toRGB8())
				item.info.identifier = id
				swatchbook.materials[id] = item
				swatchbook.book.items.append(Swatch(id))
				i += 1
			if len(list(colorPage.getiterator('colorEntry'))) < swatchbook.book.display['columns'] and i<nbcolors:
				swatchbook.book.items.append(Break())
		if encrypted:
			sys.stderr.write(file+": this script can't decode encrypted RGB values\n")

