#!/usr/bin/env python
# coding: utf-8
#
#       Copyright 2010 Olivier Berten <olivier.berten@gmail.com>
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

class DescriptorParser:
	def __init__(self,file):
		self.file = file

	def readClassID(self):
		length = struct.unpack('>L',self.file.read(4))[0]
		if length == 0:
			length = 4
		return self.file.read(length)

	def readUnicodeString(self):
		length = struct.unpack('>L',self.file.read(4))[0]
		string = unicode(self.file.read(length*2),'utf_16_be').split('\x00')[0]
		if string[0:4] == '$$$/':
			string = string.partition('=')[2]
		return string.replace('^C',u'©').replace('^R',u'®')

	def readDouble(self):
		return struct.unpack('>d',self.file.read(8))[0]

	def readInteger(self):
		return struct.unpack('>L',self.file.read(4))[0]

	def readBoolean(self):
		return struct.unpack('>?',self.file.read(1))[0]

	def readEnumerated(self):
		typeID = self.readClassID()
		enum = self.readClassID()
		return (typeID,enum)

	def readUnitFloat(self):
		unit = self.file.read(4)
		value = struct.unpack('>d',self.file.read(8))[0]
		return (unit,value)

	def readOSType(self):
		OSType = self.file.read(4)
		if OSType == 'VlLs':
			item = self.readList()
		elif OSType == 'TEXT':
			item = self.readUnicodeString()
		elif OSType == 'Objc':
			item = self.readDescriptor()
		elif OSType == 'long':
			item = self.readInteger()
		elif OSType == 'doub':
			item = self.readDouble()
		elif OSType == 'bool':
			item = self.readBoolean()
		elif OSType == 'enum':
			item = self.readEnumerated()
		elif OSType == 'UntF':
			item = self.readUnitFloat()
		elif OSType == 'tdta':
			item = self.readClassID()
		return item

	def readList(self):
		nbitems = struct.unpack('>L',self.file.read(4))[0]
		items = []
		for i in range(nbitems):
			items.append(self.readOSType())
		return items

	def readDescriptor(self):
		name = self.readUnicodeString()
		classID = self.readClassID()
		nbitems = struct.unpack('>L',self.file.read(4))[0]
		items = {}
		for i in range(nbitems):
			key = self.readClassID()
			item = self.readOSType()
			items[key] = item
		return (classID,name,items)

class adobe_grd(SBCodec):
	"""Adobe Gradient"""
	ext = ('grd','jgd','PspGradient')
	@staticmethod
	def test(file):
		file = open(file,'rb')
		data = file.read(4)
		file.close()
		if data == '8BGR':
			return True
		else:
			return False

	@staticmethod
	def read(swatchbook,file):
		file = open(file,'rb')
		signature,version = struct.unpack('>4s H',file.read(6))
		if version == 3:
			ColorModels = ['RGB','HSB','CMYK','Pantone','Focoltone','Trumatch','Toyo','Lab','Gray','WideCMYK','HKS','DIC','TotalInk','MonitorRGB','Duotone','Opacity']
			ColorTypes = ['User color','Foreground color','Background color']
			nbgradients = struct.unpack('>H',file.read(2))[0]
			for i in range(nbgradients):
				item = Gradient(swatchbook)
				name_length = struct.unpack('B',file.read(1))[0]
				name = file.read(name_length)
				nbstops = struct.unpack('>H',file.read(2))[0]
				for j in range(nbstops):
					stop = ColorStop()
					location,midpoint,model = struct.unpack('>2L H',file.read(10))
					stop.position = location/0x1000
					if midpoint != 50:
						stop.args['midpoint'] = midpoint/100
					color = Color(swatchbook)
					if model == 2:
						C,M,Y,K = struct.unpack('>4H',file.read(8))
						color.values[('CMYK',False)] = [1-C/0xFFFF,1-M/0xFFFF,1-Y/0xFFFF,1-K/0xFFFF]
					elif model == 9:
						C,M,Y,K = struct.unpack('>4H',file.read(8))
						color.values[('CMYK',False)] = [C/10000,M/10000,Y/10000,K/10000]
					elif model == 0:
						R,G,B = struct.unpack('>3H',file.read(6))
						color.values[('RGB',False)] = [R/0xFFFF,G/0xFFFF,B/0xFFFF]
						file.seek(2, 1)
					elif model == 1:
						H,S,V = struct.unpack('>3H',file.read(6))
						color.values[('HSV',False)] = [H/0xFFFF,S/0xFFFF,V/0xFFFF]
						file.seek(2, 1)
					elif model == 7:
						L,a,b = struct.unpack('>H 2h',file.read(6))
						color.values[('Lab',False)] = [L/100,a/100,b/100]
						file.seek(2, 1)
					elif model == 8:
						K = struct.unpack('>H',file.read(2))[0]
						color.values[('GRAY',False)] = [K/10000,]
						file.seek(6, 1)
					else:
						file.seek(8, 1)
						sys.stderr.write('unsupported color model ['+ColorModels[model]+']\n')
					colorid = idfromvals(color.values[color.values.keys()[0]])
					type = struct.unpack('>H',file.read(2))[0]
					if type != 0:
						colorid = ColorTypes[type]
					if not colorid in swatchbook.materials:
						color.info.identifier = colorid
						swatchbook.materials[colorid] = color
					stop.color = colorid
					stop.interpolation = "sine"
					item.stops.append(stop)
				nbopstops = struct.unpack('>H',file.read(2))[0]
				opstops = []
				transparency = False
				for j in range(nbopstops):
					location,midpoint,opacity = struct.unpack('>2L H',file.read(10))
					opstops.append((location,midpoint,opacity))
					if opacity != 0xFF:
						transparency = True
				if transparency:
					for opstop in opstops:
						stop = OpacityStop()
						stop.position = opstop[0]/0x1000
						if opstop[1] != 50:
							stop.args['midpoint'] = opstop[1]/100
						stop.opacity = opstop[2]/0xFF
						stop.interpolation = "sine"
						item.opacitystops.append(stop)
				file.seek(6, 1)
				id = name
				if id in swatchbook.materials or id == '':
					if name > '':
						item.info.title = name
					else:
						name = 'Gradient'
					i = 1
					while id in form.sb.materials:
						id = name+' ('+str(i)+')'
						i += 1
				item.info.identifier = id
				swatchbook.materials[id] = item
				swatchbook.book.items.append(Swatch(id))
		elif version == 5:
			ColorTypes = {'UsrS': 'User color', 'FrgC': 'Foreground color', 'BckC': 'Background color'}
			ps6 = struct.unpack('>L',file.read(4))[0]
			DescriptorContent = DescriptorParser(file)
			gradients = DescriptorContent.readDescriptor()
			for gradient in gradients[2]['GrdL']:
				item = Gradient(swatchbook)
				grdn = gradient[2]['Grad'][2]
				name = grdn['Nm  ']
				type = grdn['GrdF'][1]
				if type == 'CstS':
					item.extra['smoothness'] = grdn['Intr']/0x1000
					for CstS in grdn['Clrs']:
						stop = ColorStop()
						stop.position = CstS[2]['Lctn']/0x1000
						if CstS[2]['Mdpn'] != 50:
							stop.args['midpoint'] = CstS[2]['Mdpn']/100
						color = Color(swatchbook)
						colorid = False
						if CstS[2]['Type'][1] == 'UsrS':
							Clr = CstS[2]['Clr ']
							if Clr[0] == 'RGBC':
								R = Clr[2]['Rd  ']/0xFF
								G = Clr[2]['Grn ']/0xFF
								B = Clr[2]['Bl  ']/0xFF
								color.values[('RGB',False)] = [R,G,B]
							elif Clr[0] == 'HSBC':
								H = Clr[2]['H   '][1]/360
								S = Clr[2]['Strt']/100
								V = Clr[2]['Brgh']/100
								color.values[('HSV',False)] = [H,S,V]
							elif Clr[0] == 'CMYC':
								C = Clr[2]['Cyn ']/100
								M = Clr[2]['Mgnt']/100
								Y = Clr[2]['Ylw ']/100
								K = Clr[2]['Blck']/100
								color.values[('CMYK',False)] = [C,M,Y,K]
							elif Clr[0] == 'Grsc':
								K = Clr[2]['Gry ']/100
								color.values[('GRAY',False)] = [K]
							elif Clr[0] == 'LbCl':
								L = Clr[2]['Lmnc']
								a = Clr[2]['A   ']
								b = Clr[2]['B   ']
								color.values[('Lab',False)] = [L,a,b]
							elif Clr[0] == 'BkCl':
								colorid = Clr[2]['Nm  ']
							else:
								sys.stderr.write('unknown color model ['+Clr[0]+']\n')
						elif CstS[2]['Type'][1] == 'FrgC':
							colorid = 'Foreground color'
							color.values[('sRGB',False)] = [0,0,0]
						elif CstS[2]['Type'][1] == 'BckC':
							colorid = 'Background color'
							color.values[('sRGB',False)] = [1,1,1]
						if not colorid:
							colorid = idfromvals(color.values[color.values.keys()[0]])
						if not colorid in swatchbook.materials:
							color.info.identifier = colorid
							swatchbook.materials[colorid] = color
						stop.color = colorid
						stop.interpolation = "sine"
						item.stops.append(stop)
					opstops = []
					transparency = False
					for opstop in grdn['Trns']:
						opstops.append((opstop[2]['Lctn'],opstop[2]['Mdpn'],opstop[2]['Opct'][1]))
						if opstop[2]['Opct'][1] != 100.0:
							transparency = True
					if transparency:
						for opstop in opstops:
							stop = OpacityStop()
							stop.position = opstop[0]/0x1000
							if opstop[1] != 50:
								stop.args['midpoint'] = opstop[1]/100
							stop.opacity = opstop[2]/100
							item.opacitystops.append(stop)
				id = name
				if id in swatchbook.materials:
					if name > '':
						item.info.title = name
					i = 1
					while id in swatchbook.materials:
						id = name+' ('+str(i)+')'
						i += 1
				item.info.identifier = id
				swatchbook.materials[id] = item
				swatchbook.book.items.append(Swatch(id))

		file.close()

