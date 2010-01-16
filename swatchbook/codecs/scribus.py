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

class scribus(Codec):
	"""Scribus Swatch"""
	ext = ('xml',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag == 'SCRIBUSCOLORS':
			return True
		else:
			return False

	@staticmethod
	def read(book,file):
		xml = etree.parse(file).getroot()
		if 'Name' in xml.attrib:
			book.info['name'] = {0: unicode(xml.attrib['Name'])}
		colors = xml.getiterator('COLOR')
		i = 0
		for color in colors:
			item = Color(book)
			id = 'col'+str(i+1)
			name = unicode(color.attrib['NAME'])
			if name > u'':
				item.info['name'] = {0: name}
			if "RGB" in color.attrib:
				rgb = color.attrib['RGB']
				item.values[('RGB',False)] = [int(rgb[1:3],16)/0xFF,int(rgb[3:5],16)/0xFF,int(rgb[5:],16)/0xFF]
			if "CMYK" in color.attrib:
				cmyk = color.attrib['CMYK']
				item.values[('CMYK',False)] = [int(cmyk[1:3],16)/0xFF,int(cmyk[3:5],16)/0xFF,int(cmyk[5:7],16)/0xFF,int(cmyk[7:],16)/0xFF]
			if "Spot" in color.attrib and color.attrib['Spot'] == 1:
				item.attr.append('spot')
			book.items[id] = item
			book.ids[id] = (item,book)
			i += 1

	@staticmethod
	def write(book,lang=0):
		scsw = '<?xml version="1.0" encoding="UTF-8"?>\n<SCRIBUSCOLORS Name="'+book.info['name'][lang]+'">\n'
		scsw += scribus.writem(book.items)
		scsw += '</SCRIBUSCOLORS>'
		return scsw.encode('utf-8')

	@staticmethod
	def writem(items,lang=0):
		scsw_tmp = u''
		for item in items.values():
			if isinstance(item,Color):
				values = unicc(item.values)
				scsw_tmp += ' <COLOR '
				if 'CMYK' in values:
					C,M,Y,K = values['CMYK']
					scsw_tmp += 'CMYK="#'+hex2(C*0xFF)+hex2(M*0xFF)+hex2(Y*0xFF)+hex2(K*0xFF)+'"'
				elif 'GRAY' in values:
					K = values['GRAY'][0]
					scsw_tmp += 'CMYK="#000000'+hex2(K*0xFF)+'"'
				else:
					if item.toRGB8():
						R,G,B = item.toRGB8()
						scsw_tmp += 'RGB="#'+hex2(R)+hex2(G)+hex2(B)+'"'
				if 'name' in item.info:
					scsw_tmp += ' NAME="'+xmlescape(item.info['name'][lang])+'"'
				if 'spot' in item.attr:
					scsw_tmp += ' Spot="1"'
				scsw_tmp += ' />\n'
			elif isinstance(item,Group):
				scsw_tmp += scribus.writem(item.items)
		return scsw_tmp


