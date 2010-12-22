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

	guide = {'1': u'COLOR BRIDGE® Coated',
	         '2': u'COLOR BRIDGE® Uncoated',
	         '3': u'FORMULA GUIDE Solid Coated',
	         '4': u'FORMULA GUIDE Solid Matte',
	         '5': u'FORMULA GUIDE Solid Uncoated',
	         '6': u'GoeGuide™ coated',
	         '7': u'GoeGuide™ uncoated',
	         '8': u'FASHION + HOME cotton',
	         '9': u'FASHION + HOME paper',
	         '10': u'GoeBridge™ coated',
	         '11': u'COLOR BRIDGE® coated',
	         '12': u'COLOR BRIDGE® uncoated',
	         '13': u'FORMULA GUIDE Solid Coated',
	         '14': u'FORMULA GUIDE Solid Uncoated',
	         '15': u'PREMIUM METALLICS Coated',
	         '16': u'PASTELS & NEONS Coated',
	         '17': u'PASTELS & NEONS Uncoated',
	         '18': u'CMYK Coated',
	         '19': u'CMYK Uncoated',
	         '20': u'METALLIC FORMULA GUIDE coated'}
	
	def level0(self):
		guides = SortedDict()
		guides[u'PANTONE® MATCHING SYSTEM'] = SortedDict()
		guides[u'PANTONE® MATCHING SYSTEM']['3'] = self.guide['3']
		guides[u'PANTONE® MATCHING SYSTEM']['5'] = self.guide['5']
		guides[u'PANTONE® MATCHING SYSTEM']['4'] = self.guide['4']
		guides[u'PANTONE® MATCHING SYSTEM']['1'] = self.guide['1']
		guides[u'PANTONE® MATCHING SYSTEM']['2'] = self.guide['2']
		guides[u'PANTONE® MATCHING SYSTEM']['20'] = self.guide['20']
		guides[u'PANTONE® MATCHING SYSTEM']['8'] = self.guide['8']
		guides[u'PANTONE® MATCHING SYSTEM']['9'] = self.guide['9']
		guides[u'PANTONE® Goe™ System'] = SortedDict()
		guides[u'PANTONE® Goe™ System']['6'] = self.guide['6']
		guides[u'PANTONE® Goe™ System']['7'] = self.guide['7']
		guides[u'PANTONE® Goe™ System']['10'] = self.guide['10']
		guides[u'PANTONE® PLUS SERIES'] = SortedDict()
		guides[u'PANTONE® PLUS SERIES']['13'] = self.guide['13']
		guides[u'PANTONE® PLUS SERIES']['14'] = self.guide['14']
		guides[u'PANTONE® PLUS SERIES']['11'] = self.guide['11']
		guides[u'PANTONE® PLUS SERIES']['12'] = self.guide['12']
		guides[u'PANTONE® PLUS SERIES']['15'] = self.guide['15']
		guides[u'PANTONE® PLUS SERIES']['16'] = self.guide['16']
		guides[u'PANTONE® PLUS SERIES']['17'] = self.guide['17']
		guides[u'PANTONE® PLUS SERIES']['18'] = self.guide['18']
		guides[u'PANTONE® PLUS SERIES']['19'] = self.guide['19']
		return guides

	def read(self,swatchbook,guide):
		page = urlopen(self.url+'xref_lib'+guide+'.js').readlines()
		swatchbook.info.title = 'PANTONE® '+self.guide[guide]
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
