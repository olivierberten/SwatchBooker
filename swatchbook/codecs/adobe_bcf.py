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

bcf_model = {1: 'RGB', 2: 'CMYK',8: 'hifi', 16: 'Mixed'}

class adobe_bcf(Codec):
	"""Binary Color Format"""
	ext = ('bcf',)
	@staticmethod
	def test(file):
		file = open(file,'rb')
		data = file.read(7)
		file.close()
		if struct.unpack('7s', data)[0] in ('ACF 1.0','ACF 2.1','BCF 2.0'):
			return True
		else:
			return False

	@staticmethod
	def read(book,file):
		file = open(file,'rb')
		version = struct.unpack('8s',file.read(8))[0].split('\x00', 1)[0]
		name = struct.unpack('32s',file.read(32))[0].split('\x00', 1)[0]
		if name > '':
			book.info['name'] = {0: unicode(name,'macroman')}
		book.info['version'] = unicode(struct.unpack('8s',file.read(8))[0].split('\x00', 1)[0],'macroman')
		copyright = struct.unpack('32s',file.read(32))[0].split('\x00', 1)[0]
		if copyright > '':
			book.info['copyright'] = {0: unicode(copyright,'macroman')}
		description = struct.unpack('512s',file.read(512))[0].split('\x00', 1)[0]
		if description > '':
			book.info['description'] = {0: unicode(description,'macroman')}
		names, book.display['columns'], book.display['rows'], nbcolors =  struct.unpack('>4H',file.read(8))
		prefix =  struct.unpack('12s',file.read(12))[0].split('\x00', 1)[0]
		if prefix > '':
			prefix = unicode(prefix+' ','macroman')
		suffix = struct.unpack('4s',file.read(4))[0].split('\x00', 1)[0]
		if suffix > '':
			suffix = unicode(' '+suffix,'macroman')
		type, XYZ, CMYK, RGB, preferredmodel = struct.unpack('>5h',file.read(10))
		preferredmodel = bcf_model[preferredmodel]
		if version in ('ACF 2.1','BCF 2.0'):
			extender = struct.unpack('>H',file.read(2))[0]
			if extender  == 1:
				description2 = struct.unpack('100s',file.read(100))[0].split('\x00', 1)[0]
				book.info['description'][0] = book.info['description'][0]+unicode(description2,'macroman')
			inks,nbinks,Lab = struct.unpack('>3H',file.read(6))
			file.seek(24, 1)
			if inks  == 1:
				book.inks = []
				for i in range(nbinks):
					book.inks.append(struct.unpack('>10s 10s H 32s',file.read(54)))
		for i in range(nbcolors):
			item = Color(book)
			id = 'col'+str(i+1)
			if XYZ == 1:
				X,Y,Z  = struct.unpack('>3H',file.read(6))
				item.values[('XYZ',False)] = [X*100/0xFFFF,Y*100/0xFFFF,Z*100/0xFFFF]
			elif 'Lab' in vars() and Lab == 1:
				item.values[('Lab',False)] = list(struct.unpack('>3h',file.read(6)))
			else:
				file.seek(6, 1)
			if CMYK == 1:
				C,M,Y,K = struct.unpack('>4H',file.read(8))
				item.values[('CMYK',False)] = [C/0xFFFF,M/0xFFFF,Y/0xFFFF,K/0xFFFF]
			else:
				file.seek(8, 1)
			if RGB == 1:
				R,G,B = struct.unpack('>3H',file.read(6))
				item.values[('RGB',False)] = [R/0xFFFF,G/0xFFFF,B/0xFFFF]
			else:
				file.seek(6, 1)
			if version in ('ACF 2.1','BCF 2.0') and type in (8,16):
				col_nbinks = struct.unpack('>H',file.read(2))[0]
				if col_nbinks > 0:
					item.values[("%X" % col_nbinks)+'CLR',False] = {}
					for j in range(col_nbinks):
						hifi = struct.unpack('>2H',file.read(4))
						item.values[("%X" % col_nbinks)+'CLR',False][hifi[0]] = hifi[1]/0xFFFF
				file.seek((8-col_nbinks)*4, 1)
			col_type = struct.unpack('>H',file.read(2))[0]
			if col_type == 1:
				item.attr.append('spot')
			if version in ('ACF 2.1','BCF 2.0') and type in (8,16):
				col_preferredmodel = struct.unpack('>H',file.read(2))[0]
				item.preferredmodel = bcf_model[col_preferredmodel]
			else:
				item.preferredmodel = preferredmodel
			name = struct.unpack('32s',file.read(32))[0].split('\x00', 1)[0]
			if name > '':
				item.info['name'] = {0: prefix+unicode(name,'macroman')+suffix}
			elif sum(item.values[item.values.keys()[0]]) == 0:
				item = Spacer()
			book.items[id] = item
			book.ids[id] = (item,book)
		file.close()

