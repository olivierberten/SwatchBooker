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

	type = 'list'
	nbLevels = 1
	url = "http://www.dtpstudio.de/colordesigner/"

	def level0(self):
		page = urllib.urlopen(self.url+"popup_d.htm").read()
		namelist = page.split('<option value="-1" selected>Farbsystem auswählen...</option>')[1].split('</option>\n            </select>')[0].strip().split('</option>')
		page = urllib.urlopen(self.url+"Scripts/main.js").read()
		syslist = page.split("var targetSystems = new Array('")[1].split("');",1)[0].split("','")
		systems = SortedDict()
		for i in range(len(namelist)):
			systems[syslist[i]] = namelist[i].split('">')[1]
		return systems

	def read(self,book,system):
		page = urllib.urlopen(self.url+"ColorSystems/"+system).readlines()
		book.info['name'] = {0: page[1].split('// ...::: ')[1].split(' :::...')[0]}
		i=0
		for line in page[2:]:
			line = eval(line.split('completeColor')[1].split(";")[0].replace('false','False').replace('true','True'))
			item = Color(book)
			id = 'col'+str(i+1)
			if line[0] == 0:
				item.values[('Lab',False)] = [line[1],line[2],line[3]]
			elif line[0] == 1:
				item.values[('Lhc',False)] = [line[2],line[1],line[3]]
			elif line[0] == 2:
				item.values[('RGB',False)] = [line[1],line[2],line[3]]
			item.info['name'] =  {0: unicode(line[4])}
			book.items[id] = item
			book.ids[id] = (item,book)
			i += 1
