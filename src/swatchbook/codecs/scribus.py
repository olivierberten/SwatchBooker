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

class scribus(SBCodec):
	"""Scribus Swatch"""
	ext = ('xml',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag == 'SCRIBUSCOLORS':
			return True
		else:
			return False

	@staticmethod
	def read(swatchbook,file):
		xml = etree.parse(file).getroot()
		if 'Name' in xml.attrib:
			swatchbook.info.title = xmlunescape(unicode(xml.attrib['Name']))

		for elem in xml:
			if elem.tag == 'COLOR':
				item = Color(swatchbook)
				id = unicode(xmlunescape(elem.attrib['NAME']))
				if "RGB" in elem.attrib:
					rgb = elem.attrib['RGB']
					item.values[('RGB',False)] = [int(rgb[1:3],16)/0xFF,int(rgb[3:5],16)/0xFF,int(rgb[5:],16)/0xFF]
				if "CMYK" in elem.attrib:
					cmyk = elem.attrib['CMYK']
					item.values[('CMYK',False)] = [int(cmyk[1:3],16)/0xFF,int(cmyk[3:5],16)/0xFF,int(cmyk[5:7],16)/0xFF,int(cmyk[7:],16)/0xFF]
				if "Spot" in elem.attrib and elem.attrib['Spot'] == 1:
					item.usage.add('spot')
			elif elem.tag == 'Gradient':
				item = Gradient()
				id = unicode(xmlunescape(elem.attrib['Name']))
				opstops = []
				for stops in elem:
					if stops.tag == 'CSTOP':
						stop = ColorStop()
						stop.position = eval(stops.attrib['RAMP'])
						if stops.attrib['SHADE'] == "100":
							stop.color = stops.attrib['NAME']
						else:
							tint = Tint()
							tint.color = swatchbook.materials[stops.attrib['NAME']]
							tint.amount = eval(stops.attrib['SHADE'])/100
							tintid = stops.attrib['NAME']+' (Tint '+stops.attrib['SHADE']+'%)'
							tint.info.identifier = tintid
							swatchbook.materials[tintid] = tint
							stop.color = tintid
						item.stops.append(stop)
						opstops.append((stop.position, eval(stops.attrib['TRANS'])))
				if not (len(opstops) == 2 and opstops[0][1] == opstops[1][1]):
					for i in range(len(opstops)):
						if i > 0 and i < len(opstops)-1 and (opstops[i-1][1] == opstops[i][1] and opstops[i+1][1] == opstops[i][1]):
							pass
						else:
							stop = OpacityStop()
							stop.position = opstops[i][0]
							stop.opacity = opstops[i][1]
							item.opacitystops.append(stop)

			if not id or id == '':
				id = idfromvals(item.values[item.values.keys()[0]])
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

	@staticmethod
	def write(swatchbook):
		scsw = '<?xml version="1.0" encoding="UTF-8"?>\n<SCRIBUSCOLORS Name="'+xmlescape(swatchbook.info.title)+'">\n'
		scsw += scribus.writem(swatchbook,swatchbook.book.items)
		scsw += '</SCRIBUSCOLORS>'
		return scsw.encode('utf-8')

	@staticmethod
	def writem(swatchbook,items):
		scsw_tmp = u''
		for item in items:
			if isinstance(item,Swatch):
				item = swatchbook.materials[item.material]
				if isinstance(item,Color):
					values = unicc(item.values)
					scsw_tmp += ' <COLOR '
					if 'CMYK' in values:
						C,M,Y,K = values['CMYK']
						scsw_tmp += 'CMYK="#'+hex2(C*0xFF)+hex2(M*0xFF)+hex2(Y*0xFF)+hex2(K*0xFF)+'"'
					elif 'GRAY' in values:
						K = values['GRAY'][0]
						scsw_tmp += 'CMYK="#000000'+hex2(K*0xFF)+'"'
					else:
						if item.toRGB8():
							R,G,B = item.toRGB8()
							scsw_tmp += 'RGB="#'+hex2(R)+hex2(G)+hex2(B)+'"'
					if item.info.title > '':
						name_txt = item.info.title
					else:
						name_txt = item.info.identifier
					scsw_tmp += ' NAME="'+xmlescape(name_txt)+'"'
					if 'spot' in item.usage:
						scsw_tmp += ' Spot="1"'
					scsw_tmp += ' />\n'
			elif isinstance(item,Group):
				scsw_tmp += scribus.writem(swatchbook,item.items)
		return scsw_tmp


