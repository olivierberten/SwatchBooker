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

class viva_xml(SBCodec):
	"""VivaDesigner"""
	ext = ('xml',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag == 'VivaColors':
			return True
		else:
			return False

	@staticmethod
	def read(swatchbook,file):
		xml = etree.parse(file).getroot()
		if 'name' in xml.attrib:
			swatchbook.info.title = xmlunescape(unicode(xml.attrib['name']))
		if len(list(xml.getiterator('copyright'))) > 0:
			swatchbook.info.rights = xmlunescape(unicode(list(xml.getiterator('copyright'))[0].text))
		if 'mask' in xml.attrib:
			prefix, suffix = xmlunescape(unicode(xml.attrib['mask'])).split('%1')
		else:
			prefix = suffix = ''
		if 'visiblerows' in xml.attrib:
			swatchbook.book.display['columns'] = eval(xml.attrib['visiblerows'])
		colors = xml.getiterator('color')
		for color in colors:
			item = Color(swatchbook)
			id_tmp = xmlunescape(unicode(color.attrib['name']))
			if color.attrib['type'] == 'rgb':
				item.values[('RGB',False)] = [eval(color.find('red').text)/0xFF,\
											  eval(color.find('green').text)/0xFF,\
											  eval(color.find('blue').text)/0xFF]
			elif color.attrib['type'] == 'cmyk':
				item.values[('CMYK',False)] = [eval(color.find('cyan').text)/100,\
											   eval(color.find('magenta').text)/100,\
											   eval(color.find('yellow').text)/100,\
											   eval(color.find('key').text)/100]
			if not id_tmp or id_tmp == '':
				id = str(item.values[item.values.keys()[0]])
			else:
				id = prefix+id_tmp+suffix
			if id in swatchbook.materials:
				if item.values[item.values.keys()[0]] == swatchbook.materials[id].values[swatchbook.materials[id].values.keys()[0]]:
					swatchbook.book.items.append(Swatch(id))
					continue
				else:
					sys.stderr.write('duplicated id: '+id+'\n')
					item.info.title = id
					id = id+str(item.values[item.values.keys()[0]])
			item.info.identifier = id
			swatchbook.materials[id] = item
			swatchbook.book.items.append(Swatch(id))


