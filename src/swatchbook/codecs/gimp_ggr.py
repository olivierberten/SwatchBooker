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

class gimp_ggr(SBCodec):
	"""Gimp Gradient"""
	ext = ('ggr',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(13)
		file.close()
		if struct.unpack('13s', data)[0] == 'GIMP Gradient':
			return True

	@staticmethod
	def read(swatchbook,file):
		item = Gradient()
		file = open(file, 'U').readlines()[1:]
		if file[0][:5] == 'Name:':
			item.info.identifier = unicode(file[0].partition('Name: ')[2].strip(),'utf-8')
			file = file[1:]
		if file[0].strip().isdigit():
			nbstops = eval(file[0].strip())
		else:
			sys.stderr.write('expected an integer, got: '+file[0].strip().encode('utf-8'))
			return
		file = file[1:]
		segments = []
		for i in range(nbstops):
			segment = file[i].split()
			segment = map(eval,segment)
			if len(segment) == 13:
				segment.append(0)
				segment.append(0)
			segments.append(segment)

		BlendingFunctions = ("linear","curved","sinusoidal","spherical (increasing)","spherical (decreasing)")
		ColoringTypes = ("RGB","HSV CCW","HSV CW")
		opstops = []
		for i in range(len(segments)):
			if i > 0 and [segments[i][3],segments[i][4],segments[i][5],segments[i][6],segments[i][13]] != [segments[i-1][7],segments[i-1][8],segments[i-1][9],segments[i-1][10],segments[i-1][14]]:
				stop = ColorStop()
				stop.location = segments[i-1][2]
				color = Color(swatchbook)
				if segments[i-1][14] == 0:
					color.values[('RGB',False)] = [segments[i-1][7],segments[i-1][8],segments[i-1][9]]
					colorid = idfromvals(color.values[('RGB',False)])
					opstops.append((segments[i-1][2],False,segments[i-1][10]))
				elif segments[i-1][14] == 1:
					colorid = "Foreground color"
					sys.stderr.write('unsupported color type [Foreground color]\n')
					opstops.append((segments[i-1][2],False,1.0))
				elif segments[i-1][14] == 2:
					colorid = "Foreground color"
					sys.stderr.write('unsupported color type [Foreground color]\n')
					opstops.append((segments[i-1][2],False,0.0))
				elif segments[i-1][14] == 3:
					colorid = "Background color"
					sys.stderr.write('unsupported color type [Background color]\n')
					opstops.append((segments[i-1][2],False,1.0))
				elif segments[i-1][14] == 4:
					colorid = "Background color"
					sys.stderr.write('unsupported color type [Background color]\n')
					opstops.append((segments[i-1][2],False,0.0))
				if not colorid in swatchbook.materials:
					color.info.identifier = colorid
					swatchbook.materials[colorid] = color
				stop.color = colorid
				item.stops.append(stop)
			stop = ColorStop()
			stop.position = segments[i][0]
			if round(segments[i][1], 2) != round(segments[i][0] + (segments[i][2]-segments[i][0])/2, 2):
				stop.args['midpoint'] = (segments[i][1]-segments[i][0])/(segments[i][2]-segments[i][0])
			stop.formula = BlendingFunctions[segments[i][11]]
			stop.args['coloring'] = ColoringTypes[segments[i][12]]
			color = Color(swatchbook)
			if segments[i][13] == 0:
				color.values[('RGB',False)] = [segments[i][3],segments[i][4],segments[i][5]]
				colorid = idfromvals(color.values[('RGB',False)])
				opstops.append((segments[i][0],stop.args['midpoint'],segments[i][6]))
			elif segments[i][13] == 1:
				colorid = "Foreground color"
				sys.stderr.write('unsupported color type [Foreground color]\n')
				opstops.append((segments[i-1][2],stop.args['midpoint'],1.0))
			elif segments[i][13] == 2:
				colorid = "Foreground color"
				sys.stderr.write('unsupported color type [Foreground color]\n')
				opstops.append((segments[i][0],stop.args['midpoint'],0.0))
			elif segments[i][13] == 3:
				colorid = "Background color"
				sys.stderr.write('unsupported color type [Background color]\n')
				opstops.append((segments[i][0],stop.args['midpoint'],1.0))
			elif segments[i][13] == 4:
				colorid = "Background color"
				sys.stderr.write('unsupported color type [Background color]\n')
				opstops.append((segments[i][0],stop.args['midpoint'],0.0))
			if not colorid in swatchbook.materials:
				color.info.identifier = colorid
				swatchbook.materials[colorid] = color
			stop.color = colorid
			item.stops.append(stop)
		stop = ColorStop()
		stop.position = segments[i][2]
		color = Color(swatchbook)
		if segments[i][14] == 0:
			color.values[('RGB',False)] = [segments[i][7],segments[i][8],segments[i][9]]
			colorid = idfromvals(color.values[('RGB',False)])
			opstops.append((segments[i][2],False,segments[i][10]))
		elif segments[i][14] == 1:
			colorid = "Foreground color"
			sys.stderr.write('unsupported color type [Foreground color]\n')
			opstops.append((segments[i][2],False,1.0))
		elif segments[i][14] == 2:
			colorid = "Foreground color"
			sys.stderr.write('unsupported color type [Foreground color]\n')
			opstops.append((segments[i][2],False,0.0))
		elif segments[i][14] == 3:
			colorid = "Background color"
			sys.stderr.write('unsupported color type [Background color]\n')
			opstops.append((segments[i][2],False,1.0))
		elif segments[i][14] == 4:
			colorid = "Background color"
			sys.stderr.write('unsupported color type [Background color]\n')
			opstops.append((segments[i][2],False,0.0))
		if not colorid in swatchbook.materials:
			color.info.identifier = colorid
			swatchbook.materials[colorid] = color
		stop.color = colorid
		item.stops.append(stop)

		if not (len(opstops) == 2 and opstops[0][2] == opstops[1][2]):
			for i in range(len(opstops)):
				if i > 0 and i < len(opstops)-1 and (opstops[i-1][2] == opstops[i][2] and opstops[i+1][2] == opstops[i][2]):
					pass
				else:
					stop = OpacityStop()
					stop.position = opstops[i][0]
					stop.args['midpoint'] = opstops[i][1]
					stop.opacity = opstops[i][2]
					item.opacitystops.append(stop)

		swatchbook.materials[item.info.identifier] = item
		swatchbook.book.items.append(Swatch(item.info.identifier))
				
