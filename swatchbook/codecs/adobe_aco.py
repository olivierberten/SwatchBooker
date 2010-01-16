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

class adobe_aco(Codec):
	"""Adobe Color Swatch"""
	ext = ('aco',)
	@staticmethod
	def test(file):
		file = open(file,'rb')
		data = file.read(2)
		file.close()
		if struct.unpack('>h', data)[0] in (1,2):
			return True
		else:
			return False

	@staticmethod
	def read(book,file):
		filesize = os.path.getsize(file)
		file = open(file,'rb')
		version, nbcolors = struct.unpack('>2H',file.read(4))
		if version == 1 and filesize > 4+nbcolors*10:
			file.seek(4+nbcolors*10)
			version, nbcolors = struct.unpack('>2H',file.read(4))
		for i in range(nbcolors):
			item = Color(book)
			id = 'col'+str(i+1)
			model = struct.unpack('>H',file.read(2))[0]
			if model == 2:
				C,M,Y,K = struct.unpack('>4H',file.read(8))
				item.values[('CMYK',False)] = [1-C/0xFFFF,1-M/0xFFFF,1-Y/0xFFFF,1-K/0xFFFF]
			elif model == 9:
				C,M,Y,K = struct.unpack('>4H',file.read(8))
				item.values[('CMYK',False)] = [C/10000,M/10000,Y/10000,K/10000]
			elif model == 0:
				R,G,B = struct.unpack('>3H',file.read(6))
				item.values[('RGB',False)] = [R/0xFFFF,G/0xFFFF,B/0xFFFF]
				file.seek(2, 1)
			elif model == 1:
				H,S,V = struct.unpack('>3H',file.read(6))
				item.values[('HSV',False)] = [H/0xFFFF,S/0xFFFF,V/0xFFFF]
				file.seek(2, 1)
			elif model == 7:
				L,a,b = struct.unpack('>H 2h',file.read(6))
				item.values[('Lab',False)] = [L/100,a/100,b/100]
				file.seek(2, 1)
			elif model == 8:
				K = struct.unpack('>H',file.read(2))[0]
				item.values[('GRAY',False)] = [K/10000,]
				file.seek(6, 1)
			else:
				file.seek(8, 1)
				sys.stderr.write('unknown color model ['+str(model)+']\n')
			if version == 2:
				length = struct.unpack('>L',file.read(4))[0]
				if length > 0:
					item.info['name'] = {0: unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be').split('\x00', 1)[0]}
			book.items[id] = item
			book.ids[id] = (item,book)
		file.close()

