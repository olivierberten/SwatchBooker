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

class adobe_act(SBCodec):
	"""Adobe Color Table"""
	ext = ('act',)
	@staticmethod
	def test(file):
		filesize = os.path.getsize(file)
		file = open(file)
		data = file.read()
		file.close()
		if '\x00' in data and (filesize == 772 or filesize%3 == 0) and filesize < 2048: #that limit is arbitrary as Fireworks has virtually no limit but I've never seen files bigger than 2 KB 
			return True
		else:
			return False

	@staticmethod
	def read(swatchbook,file):
		filesize = os.path.getsize(file)
		if filesize == 772: # CS2
			file = open(file,'rb')
			file.seek(768, 0)
			nbcolors = struct.unpack('>H',file.read(2))[0]
			file.seek(0, 0)
		else:
			nbcolors = int(filesize/3)
			file = open(file,'rb')
		for i in range(nbcolors):
			item = Color(swatchbook)
			id = 'col'+str(i+1)
			R,G,B = struct.unpack('3B',file.read(3))
			id = str((R,G,B))
			item.values[('RGB',False)] = [R/0xFF,G/0xFF,B/0xFF]
			if id in swatchbook.materials:
				swatchbook.book.items.append(Swatch(id))
			else:
				item.info.identifier = id
				swatchbook.materials[id] = item
				swatchbook.book.items.append(Swatch(id))
		file.close()

