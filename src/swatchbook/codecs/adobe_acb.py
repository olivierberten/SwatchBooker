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

class adobe_acb(SBCodec):
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
	def read(swatchbook,file):
		def decode_str(str):
			if str[0:4] == '$$$/':
				str = str.partition('=')[2]
			return str.replace('^C',u'©').replace('^R',u'®')
		file = open(file,'rb')
		file.seek(8, 1)
		length = struct.unpack('>L',file.read(4))[0]
		if length > 0:
			swatchbook.info.title = decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))
		length = struct.unpack('>L',file.read(4))[0]
		if length > 0:
			prefix = decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))
		else:
			prefix = ''
		length = struct.unpack('>L',file.read(4))[0]
		if length > 0:
			suffix = decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))
		else:
			suffix = ''
		length = struct.unpack('>L',file.read(4))[0]
		if length > 0:
			swatchbook.info.rights = decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))
		nbcolors = struct.unpack('>H',file.read(2))[0]
		swatchbook.book.display['columns'] = struct.unpack('>H',file.read(2))[0]
		file.seek(2, 1)
		model = struct.unpack('>H',file.read(2))[0]
		for i in range(nbcolors):
			item = Color(swatchbook)
			length = struct.unpack('>L',file.read(4))[0]
			if length > 0:
				item.info.title = prefix+decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))+suffix
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
			if item.info.title == '' and sum(item.values[item.values.keys()[0]]) == 0:
				swatchbook.book.items.append(Spacer())
				continue
			if id in swatchbook.materials:
				if item.values[item.values.keys()[0]] == swatchbook.materials[id].values[swatchbook.materials[id].values.keys()[0]]:
					swatchbook.book.items.append(Swatch(id))
					continue
				else:
					sys.stderr.write('duplicated id: '+id+'\n')
					id = id+idfromvals(item.values[item.values.keys()[0]])
			elif len(id) == 0:
				id = idfromvals(item.values[item.values.keys()[0]])
			item.info.identifier = id
			swatchbook.materials[id] = item
			swatchbook.book.items.append(Swatch(id))
		if file.read(4):
			if struct.unpack('>4s',file.read(4))[0] == 'spot':
				for id in swatchbook.materials:
					if isinstance(swatchbook.materials[id],Color):
						swatchbook.materials[id].usage.append('spot')
		file.close()

