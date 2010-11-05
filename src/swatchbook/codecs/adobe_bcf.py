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

class adobe_bcf(SBCodec):
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
	def read(swatchbook,file):
		file = open(file,'rb')
		version = struct.unpack('8s',file.read(8))[0].split('\x00', 1)[0]
		swatchbook.info.title = unicode(struct.unpack('32s',file.read(32))[0].split('\x00', 1)[0],'macroman')
		swatchbook.info.version = unicode(struct.unpack('8s',file.read(8))[0].split('\x00', 1)[0],'macroman')
		swatchbook.info.rights = unicode(struct.unpack('32s',file.read(32))[0].split('\x00', 1)[0],'macroman')
		swatchbook.info.description = unicode(struct.unpack('512s',file.read(512))[0].split('\x00', 1)[0],'macroman')
		name_format, swatchbook.book.display['columns'], swatchbook.book.display['rows'], nbcolors =  struct.unpack('>4H',file.read(8))
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
				swatchbook.info.description = swatchbook.info.description+unicode(description2,'macroman')
			inks,nbinks,Lab = struct.unpack('>3H',file.read(6))
			file.seek(24, 1)
			if inks  == 1:
				swatchbook.inks = []
				for i in range(nbinks):
					swatchbook.inks.append(struct.unpack('>10s 10s H 32s',file.read(54)))
		for i in range(nbcolors):
			item = Color(swatchbook)
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
				nCLR = ("%X" % col_nbinks)+'CLR'
				if col_nbinks > 0:
					val_tmp_d = {}
					for j in range(col_nbinks):
						hifi = struct.unpack('>2H',file.read(4))
						val_tmp_d[hifi[0]] = hifi[1]/0xFFFF
					val_tmp_l = []
					for j in range(col_nbinks):
						val_tmp_l.append(val_tmp_d[j])
					item.values[(nCLR,False)] = tuple(val_tmp_l)
				file.seek((8-col_nbinks)*4, 1)
			col_type = struct.unpack('>H',file.read(2))[0]
			if col_type == 1:
				item.usage.append('spot')
			if version in ('ACF 2.1','BCF 2.0') and type in (8,16):
				preferredmodel = bcf_model[struct.unpack('>H',file.read(2))[0]]
			if preferredmodel == 'hifi':
				preferredmodel = nCLR
			if preferredmodel != '0CLR':
				item.values.insert(0,(preferredmodel,False),item.values.pop((preferredmodel,False)))
			id = unicode(struct.unpack('32s',file.read(32))[0].split('\x00', 1)[0],'macroman').strip()
			if id == '':
				if sum(item.values[item.values.keys()[0]]) == 0:
					swatchbook.book.items.append(Spacer())
					continue
				else:
					id = str(item.toRGB8())
			else:
				id = prefix+id+suffix
			if id in swatchbook.materials:
				if item.values[item.values.keys()[0]] == swatchbook.materials[id].values[swatchbook.materials[id].values.keys()[0]]:
					swatchbook.book.items.append(Swatch(id))
					continue
				else:
					sys.stderr.write('duplicated id: '+id+'\n')
					item.info.title = id
					id = id+idfromvals(item.values[item.values.keys()[0]])
			item.info.identifier = id
			swatchbook.materials[id] = item
			swatchbook.book.items.append(Swatch(id))
		file.close()

