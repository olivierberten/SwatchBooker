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

from swatchbook.websvc import *

class dtpstudio(WebSvc):
	"""Digital Colour Atlas"""

	content = ['swatchbook']

	about = u'These data come from dtp studio\'s <a href="http://www.dtpstudio.de/colordesigner/popup_e.htm">Color Designer</a> tool.<br /><br />© dtp studio · Grünteweg 31· D-26127 Oldenburg'

	nbLevels = 1
	url = "http://www.dtpstudio.de/colordesigner/"

	def level0(self):
		page = urlopen(self.url+"popup_d.htm").read()
		namelist = page.split('<option value="-1" selected>Farbsystem auswählen...</option>')[1].split('</option>\n            </select>')[0].strip().split('</option>')
		page = urlopen(self.url+"Scripts/main.js").read()
		syslist = page.split("var targetSystems = new Array('")[1].split("');",1)[0].split("','")
		systems = SortedDict()
		for i in range(len(namelist)):
			systems[syslist[i]] = namelist[i].split('">')[1]
		# Fix for some mistakes in the color system list
		if urlopen(self.url+"popup_d.htm").info().getdate('Last-Modified') == (2009, 10, 5, 7, 15, 57, 0, 1, 0) and urlopen(self.url+"Scripts/main.js").info().getdate('Last-Modified') == (2009, 10, 5, 13, 59, 20, 0, 1, 0):
			systems['AVERY900SUPERCAST-PANTONE.js'] = 'Avery900SuperCast-Pantone'
			systems['AVERY900SUPERCAST.js'] = 'Avery900SuperCast'
			del systems['BRILLUXSCALA.js']
			systems['BRILLUX_ACRYLCOLOR.js'] = 'Brillux AcrylColor'
			systems['BRILLUX_FARBKOLLEKTION.js'] = 'Brillux Farbkollektion'
			systems['BRILLUX_KUNSTHARZPUTZ.js'] = 'Brillux Kunstharzputz'
			systems['BRILLUX_LACK.js'] = 'Brillux Lack'
			systems['BRILLUX_MINERALPUTZ.js'] = 'Brillux Mineralputz'
			systems['BRILLUX_MIX.js'] = 'Brillux Mix'
			systems.insert(34,'BRILLUX_SCALA.js','Brillux SCALA')
			systems['COLORTREND_FACADE.js'] = 'Colortrend Facade'
			systems['COLORTREND_FACADE_PLUS.js'] = 'Colortrend Facade plus'
			systems['ORACAL_SERIE_8500.js'] = 'Oracal Serie 8500'
			systems['ORACAL_SERIE_851.js'] = 'Oracal Serie 851'
			systems['STOCOLORSYSTEM.js'] = 'StoColorSystem'
			systems['STO_SILIKAT.js'] = 'sto Silikat'
			systems['ZERO_COLORFASSFARBE.js'] = 'Zero ColorFassFarbe'
			systems['ZERO_COLORSYSTEM.js'] = 'Zero ColorSystem'
			systems['ZERO_COLOR_SYSTEM_720.js'] = 'zero Color System 720'
		return systems

	def read(self,swatchbook,system):
		page = urlopen(self.url+"ColorSystems/"+system).readlines()
		swatchbook.info.title = page[1].split('// ...::: ')[1].split(' :::...')[0]
		for line in page[2:]:
			line = eval(line.split('completeColor')[1].split(";")[0].replace('false','False').replace('true','True'))
			item = Color(swatchbook)
			item.usage.add('spot')
			try:
				id = unicode(line[4],'utf-8')
			except UnicodeDecodeError:
				id = unicode(line[4],'latin1')
			if line[0] == 0:
				item.values[('Lab',False)] = [line[1],line[2],line[3]]
			elif line[0] == 1:
				item.values[('Lhc',False)] = [line[2],line[1],line[3]]
			elif line[0] == 2:
				item.values[('sRGB',False)] = [line[1],line[2],line[3]]
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
