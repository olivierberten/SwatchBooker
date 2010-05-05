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

class riff_pal(SBCodec):
	"""RIFF Palette"""
	ext = ('pal',)
	@staticmethod
	def test(file):
		file = open(file,'rb')
		data = file.read(12)
		RIFF, size, PAL = struct.unpack('<4s L 4s', data)
		file.close()
		if  RIFF == 'RIFF' and PAL == 'PAL ':
			return True
		else:
			return False

	@staticmethod
	def read(swatchbook,file):
		file = open(file,'rb')
		file.seek(12, 0)
		chunk = struct.unpack('<4s L', file.read(8))
		while chunk[0] != 'data':
			file.seek(chunk[1], 1)
			chunk = struct.unpack('<4s L', file.read(8))
		version, nbcolors = struct.unpack('<2H',file.read(4))
		for i in range(nbcolors):
			item = Color(swatchbook)
			R,G,B = struct.unpack('3B',file.read(3))
			item.values[('RGB',False)] = [R/0xFF,G/0xFF,B/0xFF]
			file.seek(1, 1)
			id = str((R,G,B))
			if id in swatchbook.swatches:
				swatchbook.book.items.append(Swatch(id))
			else:
				item.info.identifier = id
				swatchbook.swatches[id] = item
				swatchbook.book.items.append(Swatch(id))
		file.close()

