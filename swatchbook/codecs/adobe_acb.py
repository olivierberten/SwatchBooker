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

class adobe_acb(Codec):
	"""Adobe Color Book"""
	ext = ('acb',)
	@staticmethod
	def test(file):
		file = open(file,'rb')
		data = file.read(4)
		file.close()
		if struct.unpack('4s', data)[0] == '8BCB':
			return True
		else:
			return False

	@staticmethod
	def read(book,file):
		def decode_str(str):
			if str[0:4] == '$$$/':
				str = str.partition('=')[2]
			return str.replace('^C',u'©').replace('^R',u'®')
		file = open(file,'rb')
		file.seek(8, 1)
		length = struct.unpack('>L',file.read(4))[0]
		if length > 0:
			name = decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))
		if name > u'':
			book.info['name'] = {0: name}
		length = struct.unpack('>L',file.read(4))[0]
		if length > 0:
			prefix = decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))
		else:
			prefix = u''
		length = struct.unpack('>L',file.read(4))[0]
		if length > 0:
			suffix = decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))
		else:
			suffix = u''
		length = struct.unpack('>L',file.read(4))[0]
		if length > 0:
			description = decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))
		if 'description' in vars() and description > u'':
			book.info['copyright'] = {0: description}
		nbcolors = struct.unpack('>H',file.read(2))[0]
		book.display['columns'] = struct.unpack('>H',file.read(2))[0]
		file.seek(2, 1)
		model = struct.unpack('>H',file.read(2))[0]
		for i in range(nbcolors):
			item = Color(book)
			length = struct.unpack('>L',file.read(4))[0]
			if length > 0:
				item.info['name'] = {0: prefix+decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))+suffix}
			id = struct.unpack('>6s',file.read(6))[0].strip()
			if model == 0:
				R,G,B = struct.unpack('>3B',file.read(3))
				item.values[('RGB',False)] = [R/0xFF,G/0xFF,B/0xFF]
			elif model == 2:
				C,M,Y,K = struct.unpack('>4B',file.read(4))
				item.values[('CMYK',False)] = [1-C/0xFF,1-M/0xFF,1-Y/0xFF,1-K/0xFF]
			elif model == 7:
				L,a,b = struct.unpack('>3B',file.read(3))
				item.values[('Lab',False)] = [L*100/0xFF,a-0x80,b-0x80]
			else:
				sys.stderr.write('unknown color model ['+str(model)+']\n')
			if 'name' not in item.info and sum(item.values[item.values.keys()[0]]) == 0:
				id = 'sp'+str(i)
				item = Spacer()
			if id in book.ids or len(id) == 0:
				#sys.stderr.write('duplicate id ['+str(id)+']\n')
				id = id+str(item)
			book.items[id] = item
			book.ids[id] = (item,book)
		if file.read(4):
			if struct.unpack('>4s',file.read(4))[0] == 'spot':
				for id in book.items:
					if isinstance(book.items[id],Color):
						book.items[id].attr.append('spot')
		file.close()

