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

class icc_nmcl(SBCodec):
	"""ICC Named Colors Profile"""
	ext = ('icc','icm')
	@staticmethod
	def test(file):
		try:
			prof = ICCprofile(file)
			if prof.info['class'] == 'nmcl' and 'ncl2' in prof.info['tags']:
				return True
			else:
				return False
		except BadICCprofile:
			return False

	@staticmethod
	def read(swatchbook,file):
		prof = ICCprofile(file)
		if 0 in prof.info['desc']:
			swatchbook.info.title = prof.info['desc'][0]
		else:
			swatchbook.info.title = prof.info['desc'][prof.info['desc'].keys()[0]]
			swatchbook.info.title_l10n = prof.info['desc']
		if 0 in prof.info['cprt']:
			swatchbook.info.rights = prof.info['cprt'][0]
		else:
			swatchbook.info.rights = prof.info['cprt'][prof.info['cprt'].keys()[0]]
			swatchbook.info.rights_l10n = prof.info['cprt']
		file = open(file)
		file.seek(prof.info['tags']['ncl2'][0]+8)
		tag,n,m = struct.unpack('>4s 2L',file.read(12))
		prefix,suffix = struct.unpack('>32s 32s',file.read(64))
		prefix = unicode(prefix.split('\x00', 1)[0],'latin_1')
		suffix = unicode(suffix.split('\x00', 1)[0],'latin_1')
		for i in range(n):
			item = Color(swatchbook)
			# This is supposed to be coded in plain ascii but X-Rite Pantone NCPs use Latin 1
			id = prefix+unicode(struct.unpack('>32s',file.read(32))[0].split('\x00', 1)[0],'latin_1')+suffix
			if prof.info['pcs'] == 'Lab ':
				L,a,b = struct.unpack('>3H',file.read(6))
				# I'm not really sure this is the right criterion
				if prof.info['version'][0] == 4:
					item.values[('Lab',False)] = [L*100/0xFFFF,(a-0x8080)/0x101,(b-0x8080)/0x101]
				elif prof.info['version'][0] == 2:
					item.values[('Lab',False)] = [L*100/0xFF00,(a-0x8000)/0x100,(b-0x8000)/0x100]
			elif prof.info['pcs'] == 'XYZ ':
				X,Y,Z = struct.unpack('>3H',file.read(6))
				item.values[('XYZ',False)] = [X*100/0x8000,Y*100/0x8000,Z*100/0x8000]
			file.seek(m*2,1)
			item.usage.add('spot')
			item.info.identifier = id
			swatchbook.materials[id] = item
			swatchbook.book.items.append(Swatch(id))
		file.close()

