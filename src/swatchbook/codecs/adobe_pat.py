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

class PSDImage:
	def __init__(self):
		self.header = '8BPS\x00\x01\x00\x00\x00\x00\x00\x00'
		self.colorModeData = "\x00\x00\x00\x00"
		self.imageResources = "\x00\x00\x00\x00"
		self.layerAndMask = "\x00\x00\x00\x00"
		self.imageData = ""

	def addHeader(self,nbchannels,width,height,depth,mode):
		self.header += struct.pack('>H 2L 2H',nbchannels,height,width,depth,mode)
		self.depth = depth
		self.width = width
		self.height = height

	def addColorModeData(self,data):
		self.colorModeData = '\x00\x00\x03\x00' # 768
		for i in (0,1,2):
			for j in range(256):
				self.colorModeData += data[i]
				i += 3

	def unrle(self,channeldata):
		unpacked = b''
		chsizes = struct.unpack('>'+str(self.height)+'H',channeldata[:self.height*2])
		i = self.height*2
		for linesize in chsizes:
			line = channeldata[i:i+linesize]
			i+= linesize
			j = 0
			while j < linesize:
				c = struct.unpack('b',line[j])[0]
				j +=1
				if 0 <= c <= 127:
					unpacked += line[j:j+c+1]
					j += c+1
				elif -127 <= c <= -1:
					unpacked += line[j]*(-c+1)
					j += 1
				else:
					pass
		return unpacked

	def addImageData(self,channels,alpha):
		# Layer info
		if len(alpha) > 0:
			li = struct.pack('>h 4L H',-1,0,0,self.height,self.width,len(channels)+len(alpha)) # nblayers,top,left,bottom,right,nbchan
			li += struct.pack('>h L', -1, len(alpha[0][1])+2)
			for i in range(len(channels)):
				 li += struct.pack('>h L', i, len(channels[i][1])+2)
			li += '8BIMnorm'
			li += '\xFF'+'\x00'+'\x00'+'\x00' # Opacity,Clipping,Flags,Filler
			li += '\x00\x00\x00\x0C' # Extra Data Size
			li += '\x00\x00\x00\x00'+'\x00\x00\x00\x00' # Layer mask data, Layer blending ranges data
			li += '\x00\x00\x00\x00' # Layer name
			li += struct.pack('>H',alpha[0][0]) + alpha[0][1]
			for c in channels:
				li += struct.pack('>H',c[0]) + c[1]
			self.layerAndMask = struct.pack('>L',len(li)+4) + struct.pack('>L',len(li)) + li
		# Image data
		#TODO: blend against white like photoshop does
		compression = set()
		for c in channels:
			compression.add(c[0])
		for a in alpha:
			compression.add(a[0])
		if len(compression) > 1:
			for i in range(len(channels)):
				if channels[i][0] == 1:
					channels[i] = (0,self.unrle(channels[i][1]))
			for i in range(len(alpha)):
				if alpha[i][0] == 1:
					alpha[i] = (0, self.unrle(alpha[i][1]))
			comp = 0
		elif len(compression) == 1:
			comp = compression.pop()
		else:
			return
		if comp == 0:
			self.imageData += struct.pack('>H',0)
			for c in channels:
				self.imageData += c[1]
			for a in alpha:
				self.imageData += a[1]
		elif comp == 1:
			self.imageData += struct.pack('>H',1)
			csizes = b''
			cdata = b''
			for c in channels:
				csizes += c[1][:self.height*2]
				cdata += c[1][self.height*2:]
			for a in alpha:
				csizes += a[1][:self.height*2]
				cdata += a[1][self.height*2:]
			self.imageData += csizes+cdata
	def returnContent(self):
		return self.header+self.colorModeData+self.imageResources+self.layerAndMask+self.imageData

class adobe_pat(SBCodec):
	"""Adobe Pattern"""
	ext = ('pat',)
	@staticmethod
	def test(file):
		file = open(file,'rb')
		data = file.read(4)
		file.close()
		if data == '8BPT':
			return True
		else:
			return False

	@staticmethod
	def read(swatchbook,file):
		def decode_str(str):
			if str[0:4] == '$$$/':
				str = str.partition('=')[2]
			return str.replace('^C',u'©').replace('^R',u'®')
		file = open(file,'rb')
		file.seek(4, 1)
		version,pat_count = struct.unpack('>H L',file.read(6))
		patdir = os.path.join(swatchbook.tmpdir, "patterns")
		if not os.path.isdir(patdir):
			os.mkdir(patdir)
		for i in range(pat_count):
			psd = PSDImage()
			item = Pattern(swatchbook)
			version1,model,height,width,name_length = struct.unpack('>2L 2H L',file.read(16))
			if name_length > 0:
				item.info.title = decode_str(unicode(struct.unpack(str(name_length*2)+'s',file.read(name_length*2))[0],'utf_16_be')).split('\x00')[0]
			length = struct.unpack('B',file.read(1))[0]
			id = file.read(length)
			pal_size = unk2 = 0
			palette = False
			if model == 2:
				palette = file.read(256*3)
				psd.addColorModeData(palette)
				pal_size,unk2 = struct.unpack('>H h',file.read(4))
			version3,size,top,left,bottom,right,maxchannels = struct.unpack('>7L',file.read(28))
			channels = []
			for c in range(maxchannels):
				array_loaded = struct.unpack('>L',file.read(4))[0]
				if array_loaded:
					channel_size,depth1,top,left,bottom,right,depth2,compression = struct.unpack('>6L H B',file.read(27))
					data = file.read(channel_size-23)
					channels.append((compression,data))
			zero,nbalpha = struct.unpack('>2L',file.read(8))
			alpha = []
			for m in range(nbalpha):
				channel_size,depth1,top,left,bottom,right,depth2,compression = struct.unpack('>6L H B',file.read(27))
				data = file.read(channel_size-23)
				alpha.append((compression,data))
			psd.addHeader(len(channels)+len(alpha),width,height,depth1,model)
			psd.addImageData(channels,alpha)
			psd_file = open(os.path.join(patdir,id+'.psd'),'wb')
			psd_file.write(psd.returnContent())
			psd_file.close()
			item.info.identifier = id+'.psd'
			swatchbook.materials[id+'.psd'] = item
			swatchbook.book.items.append(Swatch(id+'.psd'))
		file.close()

