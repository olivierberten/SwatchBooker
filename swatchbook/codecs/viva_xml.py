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

class viva_xml(Codec):
	"""VivaDesigner"""
	ext = ('xml',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag == 'VivaColors':
			return True
		else:
			return False

	@staticmethod
	def read(book,file):
		xml = etree.parse(file).getroot()
		if 'name' in xml.attrib:
			book.info['name'] = {0: unicode(xml.attrib['name'])}
		if len(list(xml.getiterator('copyright'))) > 0:
			book.info['copyright'] = {0: unicode(list(xml.getiterator('copyright'))[0].text)}
		if 'mask' in xml.attrib:
			prefix, suffix = unicode(xml.attrib['mask']).split('%1')
		else:
			prefix = suffix = ''
		if 'visiblerows' in xml.attrib:
			book.display['columns'] = eval(xml.attrib['visiblerows'])
		colors = xml.getiterator('color')
		i = 0
		for color in colors:
			item = Color(book)
			id = 'col'+str(i+1)
			name = unicode(color.attrib['name'])
			if name > u'':
				item.info['name'] = {0: prefix+name+suffix}
			if color.attrib['type'] == 'rgb':
				item.values[('RGB',False)] = [eval(color.find('red').text)/0xFF,\
											  eval(color.find('green').text)/0xFF,\
											  eval(color.find('blue').text)/0xFF]
			elif color.attrib['type'] == 'cmyk':
				item.values[('CMYK',False)] = [eval(color.find('cyan').text)/100,\
											   eval(color.find('magenta').text)/100,\
											   eval(color.find('yellow').text)/100,\
											   eval(color.find('key').text)/100]
			book.items[id] = item
			book.ids[id] = (item,book)
			i += 1


