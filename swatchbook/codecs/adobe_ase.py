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

class adobe_ase(Codec):
	"""Adobe Swatch Exchange"""
	ext = ('ase',)
	@staticmethod
	def test(file):
		file = open(file,'rb')
		data = file.read(4)
		file.close()
		if struct.unpack('4s', data)[0] == 'ASEF':
			return True
		else:
			return False

	@staticmethod
	def read(book,file):
		file = open(file,'rb')
		file.seek(4)
		version = struct.unpack('>2H',file.read(4))
		nbblocks = struct.unpack('>L',file.read(4))[0]
		group = False
		col_count = 0
		grp_count = 0
		parent = book
		for i in range(nbblocks):
			block_type,block_size = struct.unpack('>HL',file.read(6))
			if block_type == 0xc001:
				group = Group()
				grp_count += 1
				grpid = 'grp'+str(grp_count)
				parent = group
			elif block_type == 0xc002:
				parent = book
				parent.items[grpid] = group
				book.ids[grpid] = (item,parent)
			elif block_type == 0x0001:
				item = Color(book)
				col_count += 1
				id = 'col'+str(col_count)
			if block_size > 0:
				length = struct.unpack('>H',file.read(2))[0]
				if length > 0:
					name = unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be').split('\x00', 1)[0]
				if name > u'':
					if block_type == 0xc001:
						group.info['name'] = {0: name}
					elif block_type == 0x0001:
						item.info['name'] = {0: name}
				if block_type == 0x0001:
					model = struct.unpack('4s',file.read(4))[0]
					if model == "CMYK":
						item.values[('CMYK',False)] = list(struct.unpack('>4f',file.read(16)))
					elif model == "RGB ":
						item.values[('RGB',False)] = list(struct.unpack('>3f',file.read(12)))
					elif model == "LAB ":
						L,a,b = struct.unpack('>3f',file.read(12))
						item.values[('Lab',False)] = [L*100,a,b]
					elif model == "Gray":
						item.values[('GRAY',False)] = [1-struct.unpack('>f',file.read(4))[0],]
					type = struct.unpack('>H',file.read(2))[0]
					if type == 0:
						item.attr.append('global')
					elif type == 1:
						item.attr.append('spot')
					parent.items[id] = item
					book.ids[id] = (item,parent)
		file.close()

	@staticmethod
	def write(book,lang=0):
		ase = 'ASEF\x00\x01\x00\x00'
		nbblocks,content = adobe_ase.writem(book.items)
		ase += struct.pack('>L',nbblocks)+content
		return ase

	@staticmethod
	def writem(items,nbblocks=0,lang=0):
		ase_tmp = ''
		for item in items.values():
			if isinstance(item,Color) or isinstance(item,Group):
				block_size = 0
				name = ''
				if 'name' in item.info:
					block_size += 4+len(item.info['name'][lang])*2
					name = struct.pack('>H',len(item.info['name'][lang])+1)+item.info['name'][lang].encode('utf_16_be')+'\x00\x00'
				if isinstance(item,Color):
					nbblocks += 1
					block_size += 6
					if 'spot' in item.attr:
						spot = '\x00\x01'
					elif 'global' in item.attr:
						spot = '\x00\x00'
					else:
						spot = '\x00\x02'
					values = unicc(item.values)
					if 'Lab' in values:
						L,a,b = values['Lab']
						block_size += 12
						values = 'LAB '+struct.pack('>3f',L/100,a,b)
					elif 'CMYK' in values:
						C,M,Y,K = values['CMYK']
						block_size += 16
						values = 'CMYK'+struct.pack('>4f',C,M,Y,K)
					elif 'GRAY' in values:
						Gray = values['GRAY'][0]
						block_size += 4
						values = 'Gray'+struct.pack('>f',1-Gray)
					elif 'XYZ' in values:
						X,Y,Z = values['XYZ']
						L,a,b = XYZ2Lab(X,Y,Z)
						block_size += 12
						values = 'LAB '+struct.pack('>3f',L/100,a,b)
					elif item.toRGB():
						R,G,B = item.toRGB()
						block_size += 12
						values = 'RGB '+struct.pack('>3f',R,G,B)
					else:
						values = ''
					ase_tmp += '\x00\x01'+struct.pack('>L',block_size)+name+values+spot
				elif isinstance(item,Group):
					nbblocks += 2
					ase_tmp += '\xc0\x01'+struct.pack('>L',block_size)+name
					nbblocks,content_tmp = adobe_ase.writem(item.items,nbblocks)
					ase_tmp += content_tmp
					ase_tmp += '\xc0\x02'+'\x00\x00\x00\x00'
		return nbblocks,ase_tmp


