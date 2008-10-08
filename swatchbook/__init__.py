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

import os
import sys
from color import *

class SwatchBook(object):
	"""Output values
       RGB,HSV,HSL,CMY,CMYK,6CLR,YIQ: 0 -> 1
       Lab: L 0 -> 100 | ab -128 -> 127
       XYZ: 0 -> ~100 (cfr. ref)"""

	def __init__(self, file=False):
		# Informations
		self.info = {}
		self.inks = False
		# Display informations
		self.display = {}
		self.display['breaks'] = []
		# Color Profiles
		self.profiles = {}
		# Swatches
		self.items = []

		if file:
			self.read(file)

	def read(self,file):
		if not os.path.isfile(file):
			sys.stderr.write('file '+file+' doesn\'t exist')
			return
		if os.path.getsize(file) == 0:
			sys.stderr.write('empty file')
			return
		import swatchbook.codecs as codecs
		ext =  os.path.splitext(os.path.basename(file))[1].lower()[1:]
		codec = False
		if ext in codecs.exts:
			for codec in codecs.exts[ext]:
				test = eval('codecs.'+codec).test(file)
				if test: break
			else:
				codec = False
		if codec:
			eval('codecs.'+codec).read(self,file)
			self.info['filename'] =  os.path.splitext(os.path.basename(file))[0]
			# Don't know if this is the right way...
			if isinstance(self.info['filename'],str):
				self.info['filename'] = unicode(self.info['filename'],'utf-8')
			if 'name' not in self.info:
				self.info['name'] = {0: self.info['filename'].replace('_',' ')}

		else:
			sys.stderr.write(file.encode('utf-8')+': unsupported input format\n')

	def write(self,format,output=None):
		import swatchbook.codecs as codecs
		if format in codecs.writes:
			codec = eval('codecs.'+format)
			if output == None:
				print codec.write(self)
			else:
				if not os.path.exists(output):
					content = codec.write(self)
					# TODO check if writable
					bookfile = open(output, 'w')
					bookfile.write(content)
					bookfile.close()
				else:
					sys.stderr.write('file exists\n')
		else:
			sys.stderr.write('unsupported output format\n')

class Group(object):
	def __init__(self):
		self.id = False
		self.info = {}
		self.items = []

class Swatch(object):
	def __init__(self):
		self.id = False
		self.info = {}

class Color(Swatch):
	def __init__(self):
		super(Color, self).__init__()
		self.values = {}
		self.attr = []

	def toRGB8(self):
		values = unicc(self.values)
		if 'RGB' in values:
			R,G,B = values['RGB']
		elif 'HSV' in values:
			H,S,V = values['HSV']
			R,G,B = HSV2RGB(H,S,V)
		elif 'HSL' in values:
			H,S,L = values['HSL']
			R,G,B = HSL2RGB(H,S,L)
		elif 'Lab' in values:
			L,a,b = values['Lab']
			R,G,B = Lab2RGB(L,a,b)
		elif 'CMYK' in values:
			C,M,Y,K = values['CMYK']
			R,G,B = CMYK2RGB(C,M,Y,K)
		elif 'Gray' in values:
			R = G = B = 1-values['Gray'][0]
		else:
			return False
		return (int(round(R*255)),int(round(G*255)),int(round(B*255)))
			
class Tint(Swatch):
	def __init__(self):
		super(Tint, self).__init__()
		self.color = False
		self.density = 1 # 0 = white

class Tone(Swatch):
	def __init__(self):
		super(Tone, self).__init__()
		self.color = False
		self.density = 1 # 0 = gray

class Shade(Swatch):
	def __init__(self):
		super(Shade, self).__init__()
		self.color = False
		self.density = 1 # 0 = black

class Gradient(Swatch):
	def __init__(self):
		super(Gradient, self).__init__()
		self.stops = []

class Stop(object):
	def __init__(self):
		pass
