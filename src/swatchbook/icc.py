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
import struct
import string

class BadICCprofile(Exception):
	pass

# I need that class because littlecms can't currently deal with ICCv4 names. This will be solved with v2.
class ICCprofile():
	'''Gets basic informations about a profile'''
	def __init__(self,uri):
		if os.path.getsize(uri) < 128:
			raise BadICCprofile, "That file doesn't seem to be an ICC color profile"
		else:
			file = open(uri,'rb')
			self.uri = uri
			file.seek(0)
			size,cmm = struct.unpack('>L 4s',file.read(8))                    # Profile size
			if os.path.getsize(uri) != size:
				raise BadICCprofile, "That file doesn't have the expected size"
			if not (all(c in string.ascii_letters+' '+string.digits for c in cmm) or cmm == '\x00\x00\x00\x00'):
				raise BadICCprofile, "That file doesn't seem to be an ICC color profile"
			else:
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

				try:
					cprt = self.info['tags']['cprt']
					self.info['cprt'] = self.readfield(file,cprt[1],cprt[0])
	
					desc = self.info['tags']['desc']
					self.info['desc'] = self.readfield(file,desc[1],desc[0])
				except KeyError:
					raise BadICCprofile, "That file misses one mandatory tag"
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
			records = []
			nbrecords = struct.unpack('>L',file.read(4))[0]
			size = struct.unpack('>L',file.read(4))[0]
			for i in range(nbrecords):
				records.append(struct.unpack('>2s 2s 2L',file.read(12)))
			for r in records:
				lang,country,length,offset = r
				file.seek(start+offset)
				if country != '\x00\x00':
					lg = lang+'_'+country
				else:
					lg = lang
				content[lg] = unicode(struct.unpack(str(length)+'s',file.read(length))[0],'utf_16_be').strip('\x00')
			return content
		
