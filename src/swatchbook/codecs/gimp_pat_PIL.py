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

from PIL import Image, ImageFile
import struct

class gimp_pat(ImageFile.ImageFile):
	format = "GPAT"
	format_description = "Gimp Pattern"

	def _open(self):

		# check header
		header = self.fp.read(24)
		header_size,version,width,height,bytes,GPAT = struct.unpack('>5I 4s',header)
		if GPAT != "GPAT":
			raise SyntaxError, "not a Gimp pattern file"

		# size in pixels (width, height)
		self.size = width,height

		self.info['title'] = self.fp.read(header_size-24).split('\x00')[0]

		# mode setting
		mode = {1:"L",2:"LA",3:"RGB",4:"RGBA"}
		if bytes in mode:
			self.mode = mode[bytes]
			# data descriptor
			self.tile = [("raw", (0, 0) + self.size, header_size,
						(self.mode, 0, 1))]
		else:
			raise SyntaxError, "unknown number of bits"

Image.register_open("GPAT", gimp_pat)
		
Image.register_extension("GPAT", ".pat")
