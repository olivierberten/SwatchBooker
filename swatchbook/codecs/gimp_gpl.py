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

class gimp_gpl(Codec):
	"""Gimp Palette"""
	ext = ('gpl',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(12)
		file.close()
		if struct.unpack('12s', data)[0] == 'GIMP Palette':
			return True
		else:
			return False

	@staticmethod
	def read(book,file):
		file = open(file, 'U').readlines()[1:]
		if file[0][:5] == 'Name:':
			name = unicode(file[1].partition('Name: ')[2].strip(),'utf-8')
			if name > u'':
				book.info['name'] = {0: name}
			file = file[1:]
		if file[0][:8] == 'Columns:':
			cols = int(file[0].partition('Columns: ')[2].strip()) # max 64 in Gimp 2.6
			if cols > 0:
				book.display['columns'] = cols
			file = file[1:]
		i = 0
		for line in file:
			if line[0] == '#':
				continue
			else:
				entry = line.split(None,3)
				if entry[0].isdigit() and entry[1].isdigit() and entry[2].isdigit():
					item = Color(book)
					id = 'col'+str(i+1)
					item.values[('RGB',False)] = [int(entry[0])/0xFF,int(entry[1])/0xFF,int(entry[2])/0xFF]
					if len(entry) > 3 and entry[3].strip() not in ('Untitled','Sans titre'): # other languages to be added
						item.info['name'] =  {0: unicode(entry[3].strip(),'utf-8')}
					book.items[id] = item
					book.ids[id] = (item,book)
					i += 1
				else:	
					sys.stderr.write('incorrect line: '+line.encode('utf-8'))
				
	@staticmethod
	def write(book,lang=0):
		gpl = 'GIMP Palette\n'
		if 'name' in book.info:
			gpl += 'Name: '+book.info['name'][lang]+'\n'
		if 'columns' in book.display and book.display['columns'] > 0:
			gpl += 'Columns: '+str(book.display['columns'])+'\n'
		gpl += '#'
		
		gpl += gimp_gpl.writem(book.items)
		
		return gpl.encode('utf-8')

	@staticmethod
	def writem(items,lang=0):
		gpl_tmp = u''
		for item in items.values():
			if isinstance(item,Color):
				R,G,B = item.toRGB8()
				gpl_tmp += '\n'+str(R).rjust(3)+' '+str(G).rjust(3)+' '+str(B).rjust(3)
				if item.info['name']:
					gpl_tmp += '\t'+item.info['name'][lang]
			elif isinstance(item,Group):
				gpl_tmp += '\n# '+item.info['name'][lang]
				gpl_tmp += gimp_gpl.writem(item.items)
			elif isinstance(item,Spacer):
				gpl_tmp += '\n  0   0   0'
		return gpl_tmp


