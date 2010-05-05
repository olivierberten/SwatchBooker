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

class adobe_acf(SBCodec):
	"""ASCII Color Format"""
	ext = ('acf',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(7)
		file.close()
		if struct.unpack('7s', data)[0] in ('ACF 1.0','ACF 2.1'):
			return True
		else:
			return False

	@staticmethod
	def read(swatchbook,file):
		spot=False
		file = open(file, 'U').readlines()
		version = file[0].strip()
		swatchbook.info.title = unicode(file[1].strip(),'macroman')
		swatchbook.info.version = unicode(file[2].partition('LibraryVersion: ')[2].strip(),'macroman')
		swatchbook.info.rights = unicode(file[3].partition('Copyright: ')[2].strip(),'macroman')
		swatchbook.info.description = unicode(file[4].partition('AboutMessage: ')[2].strip(),'macroman')
		name_format = file[5].partition('Names: ')[2].strip().lower() # Full Partial
		swatchbook.book.display['columns'] = eval(file[6].partition('Rows: ')[2].strip())
		swatchbook.book.display['rows'] = eval(file[7].partition('Columns: ')[2].strip())
		nbcolors = eval(file[8].partition('Entries: ')[2].strip())
		prefix = file[9].partition('Prefix: ')[2].strip()
		if prefix > '':
			prefix = unicode(prefix+' ','macroman')
		suffix = file[10].partition('Suffix: ')[2].strip()
		if suffix > '':
			suffix = unicode(' '+suffix,'macroman')
		type = file[11].partition('Type: ')[2].strip() # hifi Process Spot Mixed
		if type == 'Spot':
			spot = True
		models = file[12].partition('Models: ')[2].strip().split() # hifi Lab RGB CMYK
		preferredmodel = file[13].partition('PreferredModel: ')[2].strip()
		pos = 14
		if version == 'ACF 2.1':
			nbinks = int(file[pos].partition('Inks: ')[2].strip())
			pos = pos+1
			swatchbook.inks = []
			for i in range(nbinks):
				swatchbook.inks.append(file[pos].strip())
				pos = pos+1
		pos = pos+1
		for i in range(nbcolors):
			item = Color(swatchbook)
			for model in models:
				colors = file[pos].strip().split()
				for k in range(len(colors)):
					if model == 'RGB':
						colors[k] = eval(colors[k])/0xFFFF
					else:
						colors[k] = eval(colors[k])
				if model == "hifi" and len(colors) > 0:
					nCLR = ("%X" % len(colors))+'CLR'
					item.values[(nCLR,False)] = colors
					if preferredmodel == 'hifi':
						preferredmodel = nCLR
				else:
					item.values[(model,False)] = colors
				pos = pos+1
			item.values.insert(0,(preferredmodel,False),item.values.pop((preferredmodel,False)))
			if type == 'Mixed':
				col_type = file[pos].strip()
				if col_type == 'Spot' or spot:
					item.usage.append('spot')
				pos = pos+1
			id = unicode(file[pos].strip(),'macroman')
			if prefix > '' or suffix > '':
				item.info.title = prefix+id+suffix
			pos = pos+1
			if id in swatchbook.swatches:
				if item.values[item.values.keys()[0]] == swatchbook.swatches[id].values[swatchbook.swatches[id].values.keys()[0]]:
					swatchbook.book.items.append(Swatch(id))
					continue
				else:
					sys.stderr.write('duplicated id: '+str(id)+'\n')
					if item.info.title == '':
						item.info.title = id
					id = str(id)+'col'+str(pos)
			item.info.identifier = id
			swatchbook.swatches[id] = item
			swatchbook.book.items.append(Swatch(id))

