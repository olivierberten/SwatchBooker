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

def unserialize(string):
	s = [string]
	def parse():
		type,s[0] = s[0].split(':',1)
		if type == 'O':
			return parse_object()
		elif type == 'N':
			s[0] = s[0].split(';',1)[1]
			return None
		elif type == 'i':
			return parse_integer()
		elif type == 'd':
			return parse_double()
		elif type == 'b':
			return parse_bool()
		elif type == 's':
			return parse_string()
		elif type == 'a':
			return parse_array()

	def parse_object():
		className = parse_string()
		attributes = parse_array()
		cl = type(className, (object,), {})
		obj = cl()
		for attr in attributes:
			setattr(obj,attr,attributes[attr])
		return obj

	def parse_integer():
		i,s[0] = s[0].split(';',1)
		return int(i)

	def parse_double():
		d,s[0] = s[0].split(';',1)
		return float(d)

	def parse_bool():
		b,s[0] = s[0].split(';',1)
		return bool(int(b))

	def parse_string():
		length,s[0] = s[0].split(':"',1)
		l = int(length)
		st = s[0][:l]
		s[0] = s[0][l+2:]
		return st

	def parse_array():
		nb,s[0] = s[0].split(':{',1)
		nbElements = int(nb)
		array = SortedDict()
		for e in range(nbElements):
			key = parse()
			value = parse()
			array[key] = value
		sep,s[0] = s[0].split('}',1)
		if nbElements > 0 and len(array) == nbElements and array.keys()[-1] == nbElements-1:
			new_array = []
			for i in range(nbElements):
				new_array.append(array[i])
			array = new_array
		return array

	return parse()

class baumit(WebSvc):
	"""Baumit"""

	content = ['swatchbook']

	about = u'These data come from the <a href="http://vmw06-01.ebau.at/Contenido-Baumit/designer/?spr=en">Baumit ColourDesigner</a> tool.<br /><br />© Baumit GmbH'

	nbLevels = 1
	url = 'http://vmw06-01.ebau.at/Contenido-Baumit/designer/PHPobject/Gateway.php'

	palettes = SortedDict()
	palettes['0000000001'] = 'Colors of More Emotion'
	palettes['0000000002'] = 'Art Line'
	
	def level0(self):
		return self.palettes

	def read(self,swatchbook,palette):
		data = 'O%3A8%3A%22stdClass%22%3A5%3A%7Bs%3A7%3A%22%255Fdata%22%3Ba%3A6%3A%7Bs%3A1%3A%228%22%3Ba%3A3%3A%7Bs%3A1%3A%222%22%3Bs%3A6%3A%22bd1008%22%3Bs%3A1%3A%221%22%3Bs%3A8%3A%22designer%22%3Bs%3A1%3A%220%22%3Bs%3A9%3A%22localhost%22%3B%7Ds%3A1%3A%224%22%3Bs%3A9%3A%223348466ed%22%3Bs%3A1%3A%223%22%3Ba%3A1%3A%7Bs%3A1%3A%220%22%3Ba%3A1%3A%7Bs%3A1%3A%220%22%3Bs%3A10%3A%22'+palette+'%22%3B%7D%7Ds%3A1%3A%222%22%3Ba%3A1%3A%7Bs%3A1%3A%220%22%3Bs%3A9%3A%22getColors%22%3B%7Ds%3A1%3A%221%22%3Bs%3A5%3A%22DBcon%22%3Bs%3A1%3A%220%22%3Bi%3A1%3B%7Ds%3A9%3A%22db%255Fname%22%3Bs%3A8%3A%22designer%22%3Bs%3A9%3A%22db%255Fpass%22%3Bs%3A6%3A%22bd1008%22%3Bs%3A9%3A%22db%255Fuser%22%3Bs%3A8%3A%22designer%22%3Bs%3A9%3A%22db%255Fhost%22%3Bs%3A9%3A%22localhost%22%3B%7D'
		headers = {'Content-type' : 'text/plain'}
		req = Request(self.url, data, headers)
		response = urlopen(req).read()
		u = unserialize(unquote_plus(response[1:]))

		swatchbook.info.title = self.palettes[palette]
		if palette == '0000000001':
			swatchbook.book.display['columns'] = 5
		elif palette == '0000000002':
			swatchbook.book.display['columns'] = 8

		l = u._loader.serverResult
		for c in l:
			item = Color(swatchbook)
			item.usage.add('spot')
			id = c['col_name']
			item.info.identifier = id
			item.values[('sRGB',False)] = [int(c['col_R'])/0xFF,int(c['col_G'])/0xFF,int(c['col_B'])/0xFF]
			swatchbook.materials[id] = item
			swatchbook.book.items.append(Swatch(id))
			