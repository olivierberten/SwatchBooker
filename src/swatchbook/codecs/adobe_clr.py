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

class adobe_clr(SBCodec):
	"""Flash Color Set"""
	ext = ('clr',)
	@staticmethod
	def test(file):
		file = open(file,'rb')
		data = file.read(4)
		file.close()
		if data == '\xff\xff\x00\x00':
			return True
		else:
			return False

	@staticmethod
	def read(swatchbook,file):
		file = open(file,'rb')
		file.seek(16, 1)
		nbcolors = struct.unpack('<H',file.read(2))[0]
		file.seek(15, 1)
		swatchbook.book.display['columns'] = 21
		for i in range(nbcolors):
			item = Color(swatchbook)
			file.seek(1, 1)
			R,G,B,a = struct.unpack('4B',file.read(4))
			item.values[('RGB',False)] = [R/0xFF,G/0xFF,B/0xFF]
			id = item.values[('RGB',False)]
			if a < 0xFF:
				item.extra['alpha'] = str(a/0xFF)
				id.append(a)
			id = idfromvals(id)
			file.seek(2, 1)
			H,S,L = struct.unpack('<3H',file.read(6))
			item.values[('HLS',False)] = [H/240,L/240,S/240]
			file.seek(2, 1)
			if id in swatchbook.materials:
				swatchbook.book.items.append(Swatch(id))
			else:
				item.info.identifier = id
				swatchbook.materials[id] = item
				swatchbook.book.items.append(Swatch(id))
		file.seek(1, 1)
		nbgradients = struct.unpack('<H',file.read(2))[0]
		for i in range(nbgradients):
			item = Gradient()
			id = "Gradient "+str(i+1)
			file.seek(2, 1)
			v = struct.unpack('B',file.read(1))[0]
			file.seek(30, 1)
			nbstops = struct.unpack('B',file.read(1))[0]
			if v == 4:
				file.seek(8, 1)
			opstops = []
			transparency = False
			for j in range(nbstops):
				stop = ColorStop()
				color = Color(swatchbook)
				offset,R,G,B,opacity = struct.unpack('5B',file.read(5))
				stop.position = offset/0xFF
				color.values[('RGB',False)] = [R/0xFF, G/0xFF, B/0xFF]
				colorid = idfromvals(color.values[('RGB',False)])
				if not colorid in swatchbook.materials:
					color.info.identifier = colorid
					swatchbook.materials[colorid] = color
				stop.color = colorid
				item.stops.append(stop)
				if opacity != 0xFF:
					transparency = True
				opstops.append((offset,opacity))
			if transparency:
				for opstop in opstops:
					stop = OpacityStop()
					stop.position = opstop[0]/0xFF
					stop.opacity = opstop[1]/0xFF
					item.opacitystops.append(stop)
			item.info.identifier = id
			swatchbook.materials[id] = item
			swatchbook.book.items.append(Swatch(id))
			file.seek(6, 1)
		file.close()

