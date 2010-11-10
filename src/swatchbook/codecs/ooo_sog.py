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

class ooo_sog(SBCodec):
	"""OpenOffice.org Gradients"""
	ext = ('sog',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag in ('{http://openoffice.org/2000/office}gradient-table','{http://openoffice.org/2004/office}gradient-table'):
			return True
		else:
			return False


	@staticmethod
	def read(swatchbook,file):
		xml = etree.parse(file).getroot()
		if xml.tag == '{http://openoffice.org/2000/office}gradient-table': # OOo 2
			draw = '{http://openoffice.org/2000/drawing}'
		elif xml.tag == '{http://openoffice.org/2004/office}gradient-table': # OOo 3
			draw = '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}'
		for elem in xml:
			if elem.tag == draw+'gradient':
				item = Gradient()
				name = xmlunescape(unicode(elem.attrib[draw+'name']))
				stop = ColorStop()
				stop.position = eval(elem.attrib[draw+'border'][:-1])/100
				color = Color(swatchbook)
				rgb = elem.attrib[draw+'start-color']
				color.values[('RGB',False)] = [int(rgb[1:3],16)/0xFF,int(rgb[3:5],16)/0xFF,int(rgb[5:],16)/0xFF]
				colorid = idfromvals(color.values[('RGB',False)])
				if not colorid in swatchbook.materials:
					color.info.identifier = colorid
					swatchbook.materials[colorid] = color
				if elem.attrib[draw+'start-intensity'] == '100%':
					stop.color = colorid
				else:
					shade = Shade()
					shade.color = swatchbook.materials[stops.attrib['NAME']]
					shade.amount = eval(elem.attrib[draw+'start-intensity'][:-1])/100
					shadeid = colorid+' (Shade '+elem.attrib[draw+'start-intensity']+')'
					shade.info.identifier = shadeid
					swatchbook.materials[shadeid] = shade
					stop.color = shadeid
				item.stops.append(stop)

				stop = ColorStop()
				stop.position = 1
				color = Color(swatchbook)
				rgb = elem.attrib[draw+'end-color']
				color.values[('RGB',False)] = [int(rgb[1:3],16)/0xFF,int(rgb[3:5],16)/0xFF,int(rgb[5:],16)/0xFF]
				colorid = idfromvals(color.values[('RGB',False)])
				if not colorid in swatchbook.materials:
					color.info.identifier = colorid
					swatchbook.materials[colorid] = color
				if elem.attrib[draw+'end-intensity'] == '100%':
					stop.color = colorid
				else:
					shade = Shade()
					shade.color = swatchbook.materials[colorid]
					shade.amount = eval(elem.attrib[draw+'end-intensity'][:-1])/100
					shadeid = colorid+' (Shade '+elem.attrib[draw+'end-intensity']+')'
					shade.info.identifier = shadeid
					swatchbook.materials[shadeid] = shade
					stop.color = shadeid
				item.stops.append(stop)

				id = name
				if id in swatchbook.materials or id == '':
					if name > '':
						item.info.title = name
					else:
						name = 'Gradient'
					i = 1
					while id in swatchbook.materials:
						id = name+' ('+str(i)+')'
						i += 1
				item.info.identifier = id
				swatchbook.materials[id] = item
				swatchbook.book.items.append(Swatch(id))
