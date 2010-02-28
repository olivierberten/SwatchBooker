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
from swatchbook.websvc import *

class pantone(WebSvc):
	"""Pantone"""

	type = 'list'
	nbLevels = 1
	url = 'http://www.pantone-france.com/pages/paint/paintselector.aspx'

	def dec(self,str):
		if len(str)>0:
			return chr(ord(str[0])+7)+chr(ord(str[1])-47)+chr(ord(str[2])-23)+chr(ord(str[3])-17)+chr(ord(str[4])+5)+chr(ord(str[5])-19)
		else:
			return "FFFFFF"

	def level0(self):
		list0 = SortedDict()
		list0['0'] = u'PANTONE MATCHING SYSTEM® coated'
		list0['1'] = u'PANTONE® PAINTS+INTERIORS'
		return list0

	def read(self,book,palette):
		webpage = urllib.urlopen(self.url).read()
		data = webpage.split('\'\',\'\',\'\',\'\',\'\',')[1].split(',\r\n\t\t\r\n\t\t0);')[0]
		data = data.replace('\t\t','')
		data = data.replace('&#174;','®')
		data = data.split(',\r\n')

		swatch = []

		for line in data:
			exec 'swatch.append(['+line+'])'

		if palette == '1':
			book.info['name'] = {0: u'PANTONE® PAINTS+INTERIORS'}
			book.display['columns'] = 7
			for i in range(0,1925):
				R = int(self.dec(swatch[i][2])[0:2],16)
				G = int(self.dec(swatch[i][2])[2:4],16)
				B = int(self.dec(swatch[i][2])[4:6],16)
				item = Color(book)
				id = 'col'+str(i)
				item.values[('RGB',False)] = [R/0xFF,G/0xFF,B/0xFF]
				item.info['name'] =  {0: unicode("PANTONE "+swatch[i][0]+" TPX")}
				item.info['description'] =  {0: unicode(swatch[i][1])}
				book.items[id] = item
				book.ids[id] = (item,book)
		else:
			book.info['name'] = {0: u'PANTONE MATCHING SYSTEM® coated'}
			book.display['columns'] = 7
			for i in range(1925,3073):
				if swatch[i][0] == 'blank':
					item = Spacer()
					id = 'sp'+str(i)
				else:
					R = int(self.dec(swatch[i][2])[0:2],16)
					G = int(self.dec(swatch[i][2])[2:4],16)
					B = int(self.dec(swatch[i][2])[4:6],16)
					item = Color(book)
					id = 'col'+str(i)
					item.values[('RGB',False)] = [R/0xFF,G/0xFF,B/0xFF]
					item.info['name'] =  {0: unicode("PANTONE "+swatch[i][0],'utf-8')}
				book.items[id] = item
				book.ids[id] = (item,book)
