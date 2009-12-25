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

class colorschemer(Codec):
	"""ColorSchemer"""
	ext = ('cs',)
	@staticmethod
	def test(file):
		file = open(file,'rb')
		data = file.read(2)
		file.close()
		if struct.unpack('<H', data)[0] == 3:
			return True
		else:
			return False

	@staticmethod
	def read(book,file):
		file = open(file,'rb')
		version, nbcolors = struct.unpack('<2H',file.read(4))
		file.seek(4, 1)
		for i in range(nbcolors):
			item = Color(book)
			id = 'col'+str(i+1)
			R,G,B = struct.unpack('3B',file.read(3))
			item.values[('RGB',False)] = [R/0xFF,G/0xFF,B/0xFF]
			file.seek(1, 1)
			length = struct.unpack('<L',file.read(4))[0]
			if length > 0:
				item.info['name'] =  {0: unicode(struct.unpack(str(length)+'s',file.read(length))[0],'latin1')}
			file.seek(11, 1)
			book.items[item] = item
			book.ids[id] = (item,book)
		file.close()

