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
import os
import sys
import struct

class ICCprofile():
	'''Gets basic informations about a profile'''
	def __init__(self,file):
		file.seek(0)
		self.file = file.read()
		file.seek(8)
		version = struct.unpack('>B 1s 2s',file.read(4))              # Profile version number
		version1 = version[1].encode('hex')
		self.info = {}
		self.info['version'] = (version[0],eval('0x'+version1[0]),eval('0x'+version1[1]))
		self.info['class'] = struct.unpack('4s',file.read(4))[0]      # Profile/Device Class
		self.info['space'] = struct.unpack('4s',file.read(4))[0]      # Color space of data
		self.info['pcs'] = struct.unpack('4s',file.read(4))[0]        # Profile Connection Space
		file.seek(128)
		tags = struct.unpack('>L',file.read(4))[0]
		self.info['tags'] = {}
		for i in range(tags):
			tag = struct.unpack('>4s 2L',file.read(12))
			self.info['tags'][tag[0]] = (tag[1],tag[2])

		cprt = self.info['tags']['cprt']
		self.info['cprt'] = self.readfield(file,cprt[1],cprt[0])

		desc = self.info['tags']['desc']
		self.info['desc'] = self.readfield(file,desc[1],desc[0])

		file.close()
		
	def readfield(self,file,size,start):
		file.seek(start)
		type,zero = struct.unpack('>4s L',file.read(8))
		# text and desc fields are supposed to be coded in plain ascii but I've come across some mac_roman encoded
		if type == 'text':
			content = struct.unpack(str(size-8)+'s',file.read(size-8))[0]
			return {0: unicode(content,'mac_roman').split('\x00', 1)[0]}
		elif type == 'desc':
			acount = struct.unpack('>L',file.read(4))[0]
			return {0: unicode(struct.unpack(str(acount)+'s',file.read(acount))[0],'mac_roman').split('\x00', 1)[0]}
		elif type == 'mluc':
			content = {}
			records = struct.unpack('>L',file.read(4))[0]
			size = struct.unpack('>L',file.read(4))[0]
			for i in range(records):
				if size == 12:
					lang,country,length,offset = struct.unpack('>2s 2s 2L',file.read(12))
					file.seek(start+offset)
					content[lang+'_'+country] = unicode(struct.unpack(str(length)+'s',file.read(length))[0],'utf_16_be')
			return content
		
