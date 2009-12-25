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

from swatchbook.codecs import *

class autocad_acb(Codec):
	"""AutoCAD Color Book"""
	ext = ('acb',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag == 'colorBook':
			return True
		else:
			return False

	@staticmethod
	def read(book,file):
		xml = etree.parse(file).getroot()
		book.info['name'] = {0: unicode(list(xml.getiterator('bookName'))[0].text)}
		if len(list(xml.getiterator('majorVersion'))) > 0:
			book.info['version'] = list(xml.getiterator('majorVersion'))[0].text+'.'+list(xml.getiterator('minorVersion'))[0].text
		nbcolors = len(list(xml.getiterator('colorEntry')))
		book.display['columns'] = 0
		i = 0
		for colorPage in xml.getiterator('colorPage'):
			book.display['columns'] = max(book.display['columns'],len(list(colorPage.getiterator('colorEntry'))))
		encrypted = False
		for colorPage in xml.getiterator('colorPage'):
			for colorEntry in colorPage.getiterator('colorEntry'):
				item = Color(book)
				id = 'col'+str(i+1)
				item.info['name'] = {0: unicode(colorEntry.find('colorName').text)}
				if colorEntry.find('RGB8Encrypt'):
					encrypted = True
				elif colorEntry.find('RGB8'):
					item.values[('RGB',False)] = [eval(colorEntry.find('RGB8').find('red').text)/0xFF,eval(colorEntry.find('RGB8').find('green').text)/0xFF,eval(colorEntry.find('RGB8').find('blue').text)/0xFF]
				item.attr.append('spot')
				book.items[id] = item
				book.ids[id] = (item,book)
				i += 1
			if len(list(colorPage.getiterator('colorEntry'))) < book.display['columns'] and i<nbcolors:
				book.items['break'+str(i)] = Break()
		if encrypted:
			sys.stderr.write(file+": this script can't decode encrypted RGB values\n")

