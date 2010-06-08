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

	content = ['swatchbook']

	about = u'These data come from Pantone\'s <a href="http://www.pantone.com/pages/pantone/color_xref.aspx">X-Ref</a> tool.<br /><br />PANTONE® and other Pantone, Inc. trademarks are the property of Pantone, Inc. © Pantone, Inc. 2010'

	nbLevels = 1
	url = 'http://www.pantone.com/images/xref/'

	guide = {'1': u'PANTONE® COLOR BRIDGE® coated',
	         '2': u'PANTONE® COLOR BRIDGE® uncoated',
	         '3': u'PANTONE® FORMULA GUIDE solid coated',
	         '4': u'PANTONE® FORMULA GUIDE solid matte',
	         '5': u'PANTONE® FORMULA GUIDE solid uncoated',
	         '6': u'PANTONE® GoeGuide™ coated',
	         '7': u'PANTONE® GoeGuide™ uncoated',
	         '8': u'PANTONE® FASHION + HOME cotton',
	         '9': u'PANTONE® FASHION + HOME paper',
	         '10':u'PANTONE® GoeBridge™ coated',
	         '11':u'PANTONE® METALLIC FORMULA GUIDE coated',
	         '12':u'PANTONE® PASTEL FORMULA GUIDE coated',
	         '13':u'PANTONE® PASTEL FORMULA GUIDE uncoated'}
	
	def level0(self):
		list0 = SortedDict()
		list0['3'] = self.guide['3']
		list0['5'] = self.guide['5']
		list0['4'] = self.guide['4']
		list0['1'] = self.guide['1']
		list0['2'] = self.guide['2']
		list0['6'] = self.guide['6']
		list0['7'] = self.guide['7']
		list0['10'] = self.guide['10']
		list0['8'] = self.guide['8']
		list0['9'] = self.guide['9']
		return list0

	def read(self,swatchbook,guide):
		page = urllib.urlopen(self.url+'xref_lib'+guide+'.js').readlines()
		swatchbook.info.title = self.guide[guide]
		for line in page[1:]:
			if line.strip() > '':
				line = line.split('"')[1].split(',')
				item = Color(swatchbook)
				item.usage.append('spot')
				id = unicode(line[1])
				item.info.title = 'PANTONE® '+id
				item.values[('Lab',False)] = [eval(line[2]),eval(line[3]),eval(line[4])]
				item.values[('sRGB',False)] = [eval(line[6])/0xFF,eval(line[7])/0xFF,eval(line[8])/0xFF]
				if line[13] == '1':
					item.values[('CMYK',False)] = [eval(line[9])/100,eval(line[10])/100,eval(line[11])/100,eval(line[12])/100]
	
				if id in swatchbook.materials:
					if item.values[item.values.keys()[0]] == swatchbook.materials[id].values[swatchbook.materials[id].values.keys()[0]]:
						swatchbook.book.items.append(Swatch(id))
						continue
					else:
						sys.stderr.write('duplicated id: '+id+'\n')
						item.info.title = id
						id = id+str(item.values[item.values.keys()[0]])
				item.info.identifier = id
				swatchbook.materials[id] = item
				swatchbook.book.items.append(Swatch(id))
