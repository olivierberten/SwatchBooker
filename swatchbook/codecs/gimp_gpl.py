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

class gimp_gpl(SBCodec):
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
	def read(swatchbook,file):
		file = open(file, 'U').readlines()[1:]
		if file[0][:5] == 'Name:':
			swatchbook.info.title = unicode(file[1].partition('Name: ')[2].strip(),'utf-8')
			file = file[1:]
		if file[0][:8] == 'Columns:':
			cols = int(file[0].partition('Columns: ')[2].strip()) # max 64 in Gimp 2.6
			if cols > 0:
				swatchbook.book.display['columns'] = cols
			file = file[1:]
		for line in file:
			id = False
			if line[0] == '#':
				continue
			else:
				entry = line.split(None,3)
				if entry[0].isdigit() and entry[1].isdigit() and entry[2].isdigit():
					item = Color(swatchbook)
					item.values[('RGB',False)] = [int(entry[0])/0xFF,int(entry[1])/0xFF,int(entry[2])/0xFF]
					if len(entry) > 3 and entry[3].strip() not in ('Untitled','Sans titre'): # other languages to be added
						id = unicode(entry[3].strip(),'utf-8')
					if not id or id == '':
						id = str(item.toRGB8())
					if id in swatchbook.materials:
						if item.values[('RGB',False)] == swatchbook.materials[id].values[('RGB',False)]:
							swatchbook.book.items.append(Swatch(id))
							continue
						else:
							sys.stderr.write('duplicated id: '+id+'\n')
							item.info.title = id
							id = id+str(item.toRGB8())
					item.info.identifier = id
					swatchbook.materials[id] = item
					swatchbook.book.items.append(Swatch(id))
				else:	
					sys.stderr.write('incorrect line: '+line.encode('utf-8'))
				
	@staticmethod
	def write(swatchbook):
		gpl = 'GIMP Palette\n'
		if swatchbook.info.title > '':
			gpl += 'Name: '+swatchbook.info.title+'\n'
		if swatchbook.book.display['columns']:
			gpl += 'Columns: '+str(swatchbook.book.display['columns'])+'\n'
		gpl += '#'
		
		gpl += gimp_gpl.writem(swatchbook,swatchbook.book.items)
		
		return gpl.encode('utf-8')

	@staticmethod
	def writem(swatchbook,items):
		gpl_tmp = u''
		for item in items:
			if isinstance(item,Swatch):
				item = swatchbook.materials[item.material]
				if isinstance(item,Color):
					R,G,B = item.toRGB8()
					gpl_tmp += '\n'+str(R).rjust(3)+' '+str(G).rjust(3)+' '+str(B).rjust(3)
					if item.info.title > '':
						name_txt = item.info.title
					else:
						name_txt = item.info.identifier
					gpl_tmp += '\t'+name_txt
			elif isinstance(item,Group):
				gpl_tmp += '\n# '+item.info.title
				gpl_tmp += gimp_gpl.writem(swatchbook,item.items)
			elif isinstance(item,Spacer):
				gpl_tmp += '\n  0   0   0'
		return gpl_tmp


