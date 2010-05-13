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
import time

class icipaints(WebSvc):
	"""ICI Dulux"""

	about = u'These data come from ICI Dulux\'s MousePainter tool.<br /><br />© Copyright Imperial Chemical Industries Limited'

	type = 'list'
	nbLevels = 1
	url = ['http://icivis.uslxprod.iciwce.com/colourtools/','http://www.icipaints.co.uk/servlet/MousePainterRedirectHandler?site=','http://mp.dulux.com.cn/colourtools/data.aspx?Site=']

	brands = []
	brands.append((u'ICI Dulux (International)',0,'Data?Site=CP4&'))
	brands.append((u'Alba (Argentina)',0,'Data?Site=CP4ESAR&'))
	brands.append((u'Coral (Brazil)',0,'Data?Site=CP4BRP&'))
	brands.append((u'Dulux (Austria)',1,'EATDLX&'))
	brands.append((u'Dulux (Belgium - French)',1,'EBEDLX_FR&'))
	brands.append((u'Dulux (Belgium - Dutch)',1,'EBEDLX_NL&'))
	brands.append((u'Dulux (China)',2,'CP4ZHCN&'))
	brands.append((u'Dulux (Croatia)',1,'EHRDLX&'))
	brands.append((u'Dulux (Czech Republic)',1,'ECZDLX&'))
	brands.append((u'Dulux (Cyprus - Greek)',1,'ECYDLX_EL&'))
	brands.append((u'Dulux (Cyprus - English)',1,'ECYDLX_EN&'))
	brands.append((u'Dulux (Germany)',1,'EDEDLX&'))
	brands.append((u'Dulux (Greece - Greek)',1,'EGRDLX_EL&'))
	brands.append((u'Dulux (Greece - English)',1,'EGRDLX_EN&'))
	brands.append((u'Dulux (Hong-Kong)',0,'hk/dulux/data.jsp?'))
	brands.append((u'Dulux (Hungary)',1,'EHUDLX&'))
	brands.append((u'Dulux (Ireland)',1,'EIEDLX&'))
	brands.append((u'Dulux (Malta)',1,'EMTDLX&'))
	brands.append((u'Dulux (Pakistan)',0,'PKData?'))
	brands.append((u'Dulux (Poland)',1,'EPLDLX&'))
	brands.append((u'Dulux (Singapore)',0,'SGData?'))
	brands.append((u'Dulux (Slovakia)',1,'ESKDLX&'))
	brands.append((u'Dulux (Turkey)',1,'ETRDLX&'))
	brands.append((u'Dulux (United Kingdom)',1,'EUKICI&'))
	brands.append((u'Dulux Valentine (France)',0,'Data?Site=CP4FRFRMPD&'))
	brands.append((u'Glidden (Puerto Rico)',0,'NPRGLIData?'))
	brands.append((u'Inca (Uruguay)',0,'Data?Site=CP4ESUY&'))

	def level0(self):
		list0 = SortedDict()
		for i in range(len(self.brands)):
			list0[str(i)] = self.brands[i][0]
		return list0

	def read(self,swatchbook,brand):
		brand = int(brand)
		colorlist = urllib.urlopen(self.url[self.brands[brand][1]]+self.brands[brand][2]+'Action=GetPaletteCompact&Gammas=2.2!2.2!2.2&ColourTemp=6500').read().split('::')
		for c in colorlist:
			item = Color(swatchbook)
			item.usage.append('spot')
			c = c.split('!')
			item.info.identifier = c[0]
			item.info.title = unicode(c[1],'UTF-8')
			if c[2] > '':
				item.info.title = c[2]
			rgb = hex(int(c[3]))[2:].zfill(6)
			item.values[('RGB',False)] = [int(rgb[0:2],16)/0xFF,int(rgb[2:4],16)/0xFF,int(rgb[4:6],16)/0xFF]
			swatchbook.swatches[c[0]] = item
		ranges = SortedDict()
		rangelist = urllib.urlopen(self.url[self.brands[brand][1]]+self.brands[brand][2]+'Action=GetRangeAndLaydownInfo&LiveOnly=true').read().rsplit('!',1)[0]+'!'
		rangelist = rangelist.split('::')
		swatchbook.info.title = self.brands[brand][0]
		swatchbook.book.display['columns'] = 0
		for range in rangelist:
			r0,r = range.split('@@',1)
			r0 = r0.split('!')
			group0 = Group()
			group0.info.title = unicode(r0[1],'UTF-8')
			if r0[2] > '':
				group0.info.description = unicode(r0[2],'UTF-8')
			r = r.split('@@')
			s = []
			for r1 in r:
				r1 = r1.split('!')
				s.append(r1)
				swatchbook.book.display['columns'] = max(swatchbook.book.display['columns'],eval(r1[3]))
			for r1 in s:
				group1 = Group()
				group1.info.title = unicode(r1[1],'UTF-8')
				if r1[2] > '':
					group1.info.description = unicode(r1[2],'UTF-8')
				collist = urllib.urlopen(self.url[self.brands[brand][1]]+self.brands[brand][2]+'Action=GetLaydownColourIds&LaydownId='+r0[0]+'!'+r1[0]).read().split('!')
				i = 0
				for col in collist:
					if col > '':
						item = Swatch(col)
					else:
						item = Spacer()
					group1.items.append(item)
					if int(r1[3]) < swatchbook.book.display['columns']:
						if i < int(r1[3])-1:
							i += 1
						else:
							i = 0
							group1.items.append(Break())
				group0.items.append(group1)
			swatchbook.book.items.append(group0)
