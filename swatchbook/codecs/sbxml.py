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

class sbxml(Codec):
	"""SwatchBook XML (deprecated)"""
	ext = ('sb',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag == 'SwatchBook' and etree.parse(file).getroot().attrib['version'] == '0.1':
			return True
		else:
			return False

	@staticmethod
	def read(book,file):
		xml = etree.parse(file).getroot()
		for elem in xml:
			if elem.tag in ('group','color','spacer','break'):
				sbxml.readitem(book,elem)
			elif elem.tag in ('name','description','copyright','license'):
				if elem.tag not in book.info:
					book.info[elem.tag] = {}
				if 'lang' in elem.attrib:
					book.info[elem.tag][elem.attrib['lang']] = elem.text
				else:
					book.info[elem.tag][0] = elem.text
			elif elem.tag in ('version'):
				book.info['version'] = elem.text
			elif elem.tag in ('columns','rows'):
				book.display[elem.tag] = int(elem.text)
			elif elem.tag in ('colorspace'):
				book.profiles[elem.attrib['id']] = ICCprofile(elem.attrib['href'])

	@staticmethod
	def readitem(parent,item):
		if item.tag == 'group':
			bitem = Group()
			if 'id' in item.attrib:
				bitem.id = item.attrib['id']
			for elem in item:
				if elem.tag in ('group','color','spacer','break'):
					sbxml.readitem(bitem,elem)
				elif elem.tag in ('name','description'):
					if elem.tag not in bitem.info:
						bitem.info[elem.tag] = {}
					if 'lang' in elem.attrib:
						bitem.info[elem.tag][elem.attrib['lang']] = elem.text
					else:
						bitem.info[elem.tag][0] = elem.text
		elif item.tag == 'color':
			bitem = Color()
			if 'spot' in item.attrib and item.attrib['spot'] == '1':
				bitem.attr.append('spot')
			if 'id' in item.attrib:
				bitem.id = item.attrib['id']
			for elem in item:
				if elem.tag in ('RGB','CMYK','Lab','Gray','CMY','XYZ','YIQ','HSL','HSV','CMYKOG'):
					values = map(eval,elem.text.split())
					if 'space' in elem.attrib:
						bitem.values[(elem.tag,elem.attrib['space'])] = values
					else:
						bitem.values[elem.tag] = values
				elif elem.tag in ('name','description','copyright'):
					if elem.tag not in bitem.info:
						bitem.info[elem.tag] = {}
					if 'lang' in elem.attrib:
						bitem.info[elem.tag][elem.attrib['lang']] = elem.text
					else:
						bitem.info[elem.tag][0] = elem.text
		elif item.tag == 'spacer':
			bitem = Spacer()
		elif item.tag == 'break':
			bitem = Break()
		if isinstance(bitem,Spacer) or isinstance(bitem,Break):
			parent.items[str(bitem)] = bitem
		else:
			parent.items[bitem.id] = bitem

