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

class ooo(Codec):
	"""OpenOffice.org Color"""
	ext = ('soc',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag in ('{http://openoffice.org/2000/office}color-table','{http://openoffice.org/2004/office}color-table'):
			return True
		else:
			return False

	@staticmethod
	def read(book,file):
		xml = etree.parse(file).getroot()
		i = 0
		if xml.tag == '{http://openoffice.org/2000/office}color-table': # OOo 2
			draw = '{http://openoffice.org/2000/drawing}'
		elif xml.tag == '{http://openoffice.org/2004/office}color-table': # OOo 3
			draw = '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}'
		for elem in xml:
			if elem.tag == draw+'color':
				item = Color(book)
				id = 'col'+str(i+1)
				if draw+'name' in elem.attrib:
					item.info['name'] = {0: unicode(elem.attrib[draw+'name'])}
				if draw+'color' in elem.attrib:
					rgb = elem.attrib[draw+'color']
					item.values['RGB',False] = [int(rgb[1:3],16)/0xFF,int(rgb[3:5],16)/0xFF,int(rgb[5:],16)/0xFF]
				book.items[id] = item
				book.ids[id] = (item,book)
				i += 1

	@staticmethod
	def write(book):
		soc = '<?xml version="1.0" encoding="UTF-8"?>\n<ooo:color-table xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svg="http://www.w3.org/2000/svg" xmlns:ooo="http://openoffice.org/2004/office">'
		soc += ooo.writem(book.items)
		soc += '</ooo:color-table>'
		return soc.encode('utf-8')

	@staticmethod
	def writem(items,lang=0):
		soc = u''
		for item in items.values():
			if isinstance(item,Color):
				R,G,B = item.toRGB8()
				rgb = '#'+hex2(R)+hex2(G)+hex2(B)
				soc += '<draw:color draw:name="'
				if item.info['name']:
					soc += xmlescape(item.info['name'][lang])
				else:
					soc += rgb
				soc += '" draw:color="'+rgb+'"/>'
			elif isinstance(item,Group):
				soc += ooo.writem(item.items)
		return soc

