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

	guide = {'1': u'PANTONE® COLOR BRIDGE® Coated',
	         '2': u'PANTONE® COLOR BRIDGE® Uncoated',
	         '3': u'PANTONE® FORMULA GUIDE Solid Coated',
	         '4': u'PANTONE® FORMULA GUIDE Solid Matte',
	         '5': u'PANTONE® FORMULA GUIDE Solid Uncoated',
	         '6': u'PANTONE® GoeGuide™ coated',
	         '7': u'PANTONE® GoeGuide™ uncoated',
	         '8': u'PANTONE® FASHION + HOME cotton',
	         '9': u'PANTONE® FASHION + HOME paper',
	         '10': u'PANTONE® GoeBridge™ coated',
	         '15': u'PANTONE® PREMIUM METALLICS Coated',
	         '16': u'PANTONE® PASTELS & NEONS Coated',
	         '17': u'PANTONE® PASTELS & NEONS Uncoated',
	         '18': u'PANTONE® CMYK Coated',
	         '19': u'PANTONE® CMYK Uncoated',
	         '20': u'PANTONE® METALLIC FORMULA GUIDE coated'}
	
	def level0(self):
		list0 = SortedDict()
		list0['3'] = self.guide['3']
		list0['5'] = self.guide['5']
		list0['4'] = self.guide['4']
		list0['1'] = self.guide['1']
		list0['2'] = self.guide['2']
		list0['15'] = self.guide['15']
		list0['20'] = self.guide['20']
		list0['16'] = self.guide['16']
		list0['17'] = self.guide['17']
		list0['18'] = self.guide['18']
		list0['19'] = self.guide['19']
		list0['6'] = self.guide['6']
		list0['7'] = self.guide['7']
		list0['10'] = self.guide['10']
		list0['8'] = self.guide['8']
		list0['9'] = self.guide['9']
		return list0

	def read(self,swatchbook,guide):
		page = urlopen(self.url+'xref_lib'+guide+'.js').readlines()
		swatchbook.info.title = self.guide[guide]
		for line in page[1:]:
			if line.strip() > '':
				line = line.split('"')[1].split(',')
				item = Color(swatchbook)
				item.usage.add('spot')
				id = unicode(line[1])
				item.info.title = u'PANTONE® '+id
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
						id = id+idfromvals(item.values[item.values.keys()[0]])
				item.info.identifier = id
				swatchbook.materials[id] = item
				swatchbook.book.items.append(Swatch(id))
