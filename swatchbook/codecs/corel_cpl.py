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

class corel_cpl(Codec):
	"""Corel Palette"""
	ext = ('cpl',)
	@staticmethod
	def test(file):
		file = open(file,'rb')
		data = file.read(2)
		file.close()
		if data in ('\xcc\xbc','\xcc\xdc','\xcd\xbc','\xcd\xdc','\xdd\xdc','\xdc\xdc','\xcd\xdd'):
			return True
		else:
			return False

	@staticmethod
	def read(book,file):
		spot=False
		file = open(file,'rb')
		version = file.read(2)
		if version == '\xdc\xdc': #custom palettes
			length = struct.unpack('B',file.read(1))[0]
			if length > 0:
				book.info['name'] =  {0: unicode(struct.unpack(str(length)+'s',file.read(length))[0],'latin1')}
			nbcolors = struct.unpack('<H',file.read(2))[0]
		elif version in ('\xcc\xbc','\xcc\xdc'):
			nbcolors = struct.unpack('<H',file.read(2))[0]
		else:
			nbheaders = struct.unpack('<L',file.read(4))[0]
			headers = {}
			for i in range(nbheaders):
				id,offset = struct.unpack('<2L',file.read(8))
				headers[id] = offset
			# Header 0: Name
			file.seek(headers[0], 0)
			length = struct.unpack('B',file.read(1))[0]
			if length > 0:
				if version == '\xcd\xdc':
					book.info['name'] =  {0: unicode(struct.unpack(str(length)+'s',file.read(length))[0],'latin1')}
				else:
					book.info['name'] =  {0: unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_le')}
			# Header 1: Palette Type
			file.seek(headers[1], 0)
			type = struct.unpack('<H',file.read(2))[0]
			# Header 2: Number of colors
			file.seek(headers[2], 0)
			nbcolors = struct.unpack('<H',file.read(2))[0]
			# Header 3: Custom inks
			if 3 in headers:
				file.seek(headers[3], 0)
				nbinks = struct.unpack('<H',file.read(2))[0]
				book.inks = struct.unpack('<'+str(nbinks)+'H',file.read(nbinks*2))
			# Header 5: UI informations
			if 5 in headers:
				file.seek(headers[5], 0)
				book.display['columns'],book.display['rows'] = struct.unpack('<2H',file.read(4))
			file.seek(headers[2]+2, 0)
			if 'columns' not in book.display:
				if type in (38,):
					book.display['columns'] = 9
					book.display['rows'] = 8
				elif type in (23,26,27,28,29,30,32,32,35,36,37,39):
					book.display['columns'] = 7
					book.display['rows'] = 6
				elif type in (12,24,33,34):
					book.display['columns'] = 7
					book.display['rows'] = 7
			if type in (3,8,9,10,11,16,17,18,20,21,22,23,26,27,28,29,30,31,32,35,36,37):
				spot = True
		if version in ('\xcd\xbc','\xcd\xdc','\xcd\xdd') and type < 38 and type not in(5,16):
			long = True
		else:
			long = False
		row = {}
		col = {}
		for i in range(nbcolors):
			item = Color(book)
			if long:
				id = str(struct.unpack('<L',file.read(4))[0])
			else:
				id = 'col'+str(i+1)
			model =  struct.unpack('<H',file.read(2))[0]
			file.seek(2, 1)
			if model == 2:
				file.seek(4, 1)
				C,M,Y,K =  struct.unpack('4B',file.read(4))
				item.values[('CMYK',False)] = [C/100,M/100,Y/100,K/100]
			elif model in (3,17):
				file.seek(4, 1)
				C,M,Y,K =  struct.unpack('4B',file.read(4))
				item.values[('CMYK',False)] = [C/0xFF,M/0xFF,Y/0xFF,K/0xFF]
			elif model == 4:
				file.seek(4, 1)
				C,M,Y =  struct.unpack('3B',file.read(3))
				item.values[('CMY',False)] = [C/0xFF,M/0xFF,Y/0xFF]
				file.seek(1, 1)
			elif model in (5,21):
				file.seek(4, 1)
				B,G,R = struct.unpack('3B',file.read(3))
				item.values[('RGB',False)] = [R/0xFF,G/0xFF,B/0xFF]
				file.seek(1, 1)
			elif model == 6:
				file.seek(4, 1)
				H,S,V = struct.unpack('<H2B',file.read(4))
				item.values[('HSV',False)] = [H/360,S/0xFF,V/0xFF]
			elif model == 7:
				file.seek(4, 1)
				H,L,S = struct.unpack('<H2B',file.read(4))
				item.values[('HLS',False)] = [H/360,L/0xFF,S/0xFF]
			elif model == 9:
				file.seek(4, 1)
				K =  struct.unpack('B',file.read(1))[0]
				item.values[('GRAY',False)] = [1-K/0xFF,]
				file.seek(3, 1)
			elif model == 11:
				file.seek(4, 1)
				Y,I,Q =  struct.unpack('3B',file.read(3))
				item.values[('YIQ',False)] = [Y/0xFF,(I-100)/0x80,(Q-100)/0x80]
				file.seek(1, 1)
			elif model == 12:
				file.seek(4, 1)
				L,a,b =  struct.unpack('B 2b',file.read(3))
				item.values[('Lab',False)] = [L*100/0xFF,a,b]
				file.seek(1, 1)
			elif model == 15:
				file.seek(2, 1)
				Y,O,M,C,G,K =  struct.unpack('6B',file.read(6))
				item.values[('6CLR',False)] = [Y/100,O/100,M/100,C/100,G/100,K/100]
			elif model == 18:
				file.seek(4, 1)
				L,a,b =  struct.unpack('3B',file.read(3))
				item.values[('Lab',False)] = [L*100/0xFF,a-0x80,b-0x80]
				file.seek(1, 1)
			else:
				file.seek(8, 1)
				sys.stderr.write('unknown color model ['+str(model)+']\n')
			if long:
				model2 =  struct.unpack('<H',file.read(2))[0]
				file.seek(2, 1)
				if model2 == model:
					file.seek(8, 1)
				else:
					if model2 == 2:
						file.seek(4, 1)
						C,M,Y,K =  struct.unpack('4B',file.read(4))
						item.values[('CMYK',False)] = [C/100,M/100,Y/100,K/100]
					elif model2 in (3,17):
						file.seek(4, 1)
						C,M,Y,K =  struct.unpack('4B',file.read(4))
						item.values[('CMYK',False)] = [C/0xFF,M/0xFF,Y/0xFF,K/0xFF]
					elif model2 == 4:
						file.seek(4, 1)
						C,M,Y =  struct.unpack('3B',file.read(3))
						item.values[('CMY',False)] = [C/0xFF,M/0xFF,Y/0xFF]
						file.seek(1, 1)
					elif model2 in (5,21):
						file.seek(4, 1)
						B,G,R = struct.unpack('3B',file.read(3))
						item.values[('RGB',False)] = [R/0xFF,G/0xFF,B/0xFF]
						file.seek(1, 1)
					elif model2 == 6:
						file.seek(4, 1)
						H,S,V = struct.unpack('<H2B',file.read(4))
						item.values[('HSV',False)] = [H/360,S/0xFF,V/0xFF]
					elif model2 == 7:
						file.seek(4, 1)
						H,L,S = struct.unpack('<H2B',file.read(4))
						item.values[('HLS',False)] = [H/360,L/0xFF,S/0xFF]
					elif model2 == 9:
						file.seek(4, 1)
						K =  struct.unpack('B',file.read(1))[0]
						item.values[('GRAY',False)] = [1-K/0xFF,]
						file.seek(3, 1)
					elif model2 == 11:
						file.seek(4, 1)
						Y,I,Q =  struct.unpack('3B',file.read(3))
						item.values[('YIQ',False)] = [Y/0xFF,(I-100)/0x80,(Q-100)/0x80]
						file.seek(1, 1)
					elif model2 == 12:
						file.seek(4, 1)
						L,a,b =  struct.unpack('B 2b',file.read(3))
						item.values[('Lab',False)] = [L*100/0xFF,a,b]
						file.seek(1, 1)
					elif model2 == 15:
						file.seek(2, 1)
						Y,O,M,C,G,K =  struct.unpack('6B',file.read(6))
						item.values[('6CLR',False)] = [Y/100,O/100,M/100,C/100,G/100,K/100]
					elif model2 == 18:
						file.seek(4, 1)
						L,a,b =  struct.unpack('3B',file.read(3))
						item.values[('Lab',False)] = [L*100/0xFF,a-0x80,b-0x80]
						file.seek(1, 1)
					else:
						file.seek(8, 1)
						sys.stderr.write('unknown color model ['+str(model2)+']\n')
			length = struct.unpack('B',file.read(1))[0]
			if length > 0:
				if version in ('\xdc\xdc','\xcc\xdc') or (version == '\xcd\xdc' and type not in (16,)):
					item.info['name'] =  {0: unicode(struct.unpack(str(length)+'s',file.read(length))[0],'latin1')}
				else:
					item.info['name'] =  {0: unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_le')}
			if version == '\xcd\xdd':
				row[i], col[i] = struct.unpack('<2L',file.read(8))
				file.seek(4, 1)
			if spot:
				item.attr.append('spot')
			if 'name' in item.info and (find(item.info['name'][0],'NONASSIGNED') >= 0 or find(item.info['name'][0],'UNASSIGNED') >= 0):
				item = Spacer()
			if id in book.ids:
				#sys.stderr.write('duplicate id ['+id+']\n')
				id = id+str(item)
			if 'row' in vars() and i in row and row[i] > 0 and col[i] == 0 and col[i-1] < book.display['columns']-1:
				bbreak = Break()
				bid = 'break'+str(i)
				book.items[bid] = bbreak
				book.ids[bid] = (bbreak,book)
			book.items[id] = item
			book.ids[id] = (item,book)
			
		file.close()

