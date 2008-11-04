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
import xml.etree.cElementTree as etree
from swatchbook import *
from color import *
from string import *

class Codec(object):
	ext = False
	read = False
	write = False

class adobe_acb(Codec):
	"""Adobe Color Book"""
	ext = ('acb',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(4)
		file.close()
		if struct.unpack('4s', data)[0] == '8BCB':
			return True

	@staticmethod
	def read(book,file):
		def decode_str(str):
			if str[0:4] == '$$$/':
				str = str.partition('=')[2]
			return str.replace('^C',u'©').replace('^R',u'®')
		file = open(file)
		file.seek(8, 1)
		length = struct.unpack('>L',file.read(4))[0]
		if length > 0:
			name = decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))
		if name > u'':
			book.info['name'] = {0: name}
		length = struct.unpack('>L',file.read(4))[0]
		if length > 0:
			prefix = decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))
		else:
			prefix = u''
		length = struct.unpack('>L',file.read(4))[0]
		if length > 0:
			suffix = decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))
		else:
			suffix = u''
		length = struct.unpack('>L',file.read(4))[0]
		if length > 0:
			description = decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))
		if 'description' in vars() and description > u'':
			book.info['copyright'] = {0: description}
		nbcolors = struct.unpack('>H',file.read(2))[0]
		book.display['columns'] = struct.unpack('>H',file.read(2))[0]
		file.seek(2, 1)
		model = struct.unpack('>H',file.read(2))[0]
		for i in range(nbcolors):
			item = Color()
			length = struct.unpack('>L',file.read(4))[0]
			if length > 0:
				item.info['name'] = {0: prefix+decode_str(unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be'))+suffix}
			item.id = struct.unpack('>6s',file.read(6))[0]
			if model == 0:
				R,G,B = struct.unpack('>3B',file.read(3))
				item.values['RGB'] = (R/255,G/255,B/255)
			elif model == 2:
				C,M,Y,K = struct.unpack('>4B',file.read(4))
				item.values['CMYK'] = (1-C/255,1-M/255,1-Y/255,1-K/255)
			elif model == 7:
				L,a,b = struct.unpack('>3B',file.read(3))
				item.values['Lab'] = (L/2.55,a-128,b-128)
			else:
				sys.stderr.write('unknown color model ['+str(model)+']\n')
			if 'name' not in item.info:
				item = Spacer()
			book.items.append(item)
		if file.read(4):
			if struct.unpack('>4s',file.read(4))[0] == 'spot':
				for item in book.items:
					item.attr.append('spot')
		file.close()

class adobe_aco(Codec):
	"""Adobe Color Swatch"""
	ext = ('aco',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(2)
		file.close()
		if struct.unpack('>h', data)[0] in (1,2):
			return True

	@staticmethod
	def read(book,file):
		filesize = os.path.getsize(file)
		file = open(file)
		version, nbcolors = struct.unpack('>2H',file.read(4))
		if version == 1 and filesize > 4+nbcolors*10:
			file.seek(4+nbcolors*10)
			version, nbcolors = struct.unpack('>2H',file.read(4))
		for i in range(nbcolors):
			item = Color()
			item.id = 'col'+str(i+1)
			model = struct.unpack('>H',file.read(2))[0]
			if model == 2:
				C,M,Y,K = struct.unpack('>4H',file.read(8))
				item.values['CMYK'] = (1-C/65535,1-M/65535,1-Y/65535,1-K/65535)
			elif model == 9:
				C,M,Y,K = struct.unpack('>4H',file.read(8))
				item.values['CMYK'] = (C/10000,M/10000,Y/10000,K/10000)
			elif model == 0:
				R,G,B = struct.unpack('>3H',file.read(6))
				item.values['RGB'] = (R/65535,G/65535,B/65535)
				file.seek(2, 1)
			elif model == 1:
				H,S,V = struct.unpack('>3H',file.read(6))
				item.values['HSV'] = (H/65535,S/65535,V/65535)
				file.seek(2, 1)
			elif model == 7:
				L,a,b = struct.unpack('>H 2h',file.read(6))
				item.values['Lab'] = (L/100,a/100,b/100)
				file.seek(2, 1)
			elif model == 8:
				K = struct.unpack('>H',file.read(2))[0]
				item.values['Gray'] = (K/10000,)
				file.seek(6, 1)
			else:
				file.seek(8, 1)
				sys.stderr.write('unknown color model ['+str(model)+']\n')
			if version == 2:
				length = struct.unpack('>L',file.read(4))[0]
				if length > 0:
					item.info['name'] = {0: unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be').split('\x00', 1)[0]}
			book.items.append(item)
		file.close()

class adobe_ase(Codec):
	"""Adobe Swatch Exchange"""
	ext = ('ase',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(4)
		file.close()
		if struct.unpack('4s', data)[0] == 'ASEF':
			return True

	@staticmethod
	def read(book,file):
		file = open(file)
		file.seek(4)
		version = struct.unpack('>2H',file.read(4))
		nbblocks = struct.unpack('>L',file.read(4))[0]
		group = False
		col_count = 0
		grp_count = 0
		parent = book.items
		for i in range(nbblocks):
			block_type,block_size = struct.unpack('>HL',file.read(6))
			if block_type == 0xc001:
				group = Group()
				grp_count += 1
				group.id = 'grp'+str(grp_count)
				parent = group.items
			elif block_type == 0xc002:
				parent = book.items
				parent.append(group)
			elif block_type == 0x0001:
				item = Color()
				col_count += 1
				item.id = 'col'+str(col_count)
			if block_size > 0:
				length = struct.unpack('>H',file.read(2))[0]
				if length > 0:
					name = unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_be').split('\x00', 1)[0]
				if name > u'':
					if block_type == 0xc001:
						group.info['name'] = {0: name}
					elif block_type == 0x0001:
						item.info['name'] = {0: name}
				if block_type == 0x0001:
					model = struct.unpack('4s',file.read(4))[0]
					if model == "CMYK":
						item.values['CMYK'] = struct.unpack('>4f',file.read(16))
					elif model == "RGB ":
						item.values['RGB'] = struct.unpack('>3f',file.read(12))
					elif model == "LAB ":
						L,a,b = struct.unpack('>3f',file.read(12))
						item.values['Lab'] = (L*100,a,b)
					elif model == "Gray":
						item.values['Gray'] = (1-struct.unpack('>f',file.read(4))[0],)
					type = struct.unpack('>H',file.read(2))[0]
					if type == 0:
						item.attr.append('global')
					elif type == 1:
						item.attr.append('spot')
					parent.append(item)
		file.close()

	@staticmethod
	def write(book,lang=0):
		ase = 'ASEF\x00\x01\x00\x00'
		nbblocks,content = adobe_ase.writem(book.items)
		ase += struct.pack('>L',nbblocks)+content
		return ase

	@staticmethod
	def writem(items,nbblocks=0,lang=0):
		ase_tmp = ''
		for item in items:
			if isinstance(item,Color) or isinstance(item,Group):
				block_size = 0
				name = ''
				if 'name' in item.info:
					block_size += 4+len(item.info['name'][lang])*2
					name = struct.pack('>H',len(item.info['name'][lang])+1)+item.info['name'][lang].encode('utf_16_be')+'\x00\x00'
				if isinstance(item,Color):
					nbblocks += 1
					block_size += 6
					if 'spot' in item.attr:
						spot = '\x00\x01'
					elif 'global' in item.attr:
						spot = '\x00\x00'
					else:
						spot = '\x00\x02'
					values = unicc(item.values)
					if 'Lab' in values:
						L,a,b = values['Lab']
						block_size += 12
						values = 'LAB '+struct.pack('>3f',L/100,a,b)
					elif 'RGB' in values:
						R,G,B = values['RGB']
						block_size += 12
						values = 'RGB '+struct.pack('>3f',R,G,B)
					elif 'CMYK' in values:
						C,M,Y,K = values['CMYK']
						block_size += 16
						values = 'CMYK'+struct.pack('>4f',C,M,Y,K)
					elif 'Gray' in values:
						Gray = values['Gray'][0]
						block_size += 4
						values = 'Gray'+struct.pack('>f',1-Gray)
					elif 'HSL' in values:
						H,S,L = values['HSL']
						R,G,B = HSL2RGB(H,S,L)
						block_size += 12
						values = 'RGB '+struct.pack('>3f',R,G,B)
					elif 'HSV' in values:
						H,S,V = values['HSV']
						R,G,B = HSV2RGB(H,S,V)
						block_size += 12
						values = 'RGB '+struct.pack('>3f',R,G,B)
					elif 'CMY' in values:
						C,M,Y = values['CMY']
						R,G,B = CMY2RGB(C,M,Y)
						block_size += 12
						values = 'RGB '+struct.pack('>3f',R,G,B)
					elif 'XYZ' in values:
						X,Y,Z = values['XYZ']
						L,a,b = XYZ2Lab(X,Y,Z)
						block_size += 12
						values = 'LAB '+struct.pack('>3f',L/100,a,b)
					else:
						values = ''
					ase_tmp += '\x00\x01'+struct.pack('>L',block_size)+name+values+spot
				elif isinstance(item,Group):
					nbblocks += 2
					ase_tmp += '\xc0\x01'+struct.pack('>L',block_size)+name
					nbblocks,content_tmp = adobe_ase.writem(item.items,nbblocks)
					ase_tmp += content_tmp
					ase_tmp += '\xc0\x02'+'\x00\x00\x00\x00'
		return nbblocks,ase_tmp


class adobe_act(Codec):
	"""Adobe Color Table"""
	ext = ('act',)
	@staticmethod
	def test(file):
		filesize = os.path.getsize(file)
		if filesize == 772 or filesize%3 == 0:
			return True
	@staticmethod
	def read(book,file):
		filesize = os.path.getsize(file)
		if filesize == 772: # CS2
			file = open(file)
			file.seek(768, 0)
			nbcolors = struct.unpack('>H',file.read(2))[0]
			file.seek(0, 0)
		else:
			nbcolors = int(filesize/3)
			file = open(file)
		for i in range(nbcolors):
			item = Color()
			item.id = 'col'+str(i+1)
			R,G,B = struct.unpack('3B',file.read(3))
			item.values['RGB'] = (R/255,G/255,B/255)
			book.items.append(item)
		file.close()

class adobe_acf(Codec):
	"""ASCII Color Format"""
	ext = ('acf',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(7)
		file.close()
		if struct.unpack('7s', data)[0] in ('ACF 1.0','ACF 2.1'):
			return True
	@staticmethod
	def read(book,file):
		spot=False
		file = open(file, 'U').readlines()
		version = file[0].strip()
		book.info['name'] = {0: unicode(file[1].strip(),'macroman')}
		book.info['version'] = unicode(file[2].partition('LibraryVersion: ')[2].strip(),'macroman')
		copyright = {0: file[3].partition('Copyright: ')[2].strip()}
		if copyright > '':
			book.info['copyright'] = {0: unicode(copyright,'macroman')}
		description = file[4].partition('AboutMessage: ')[2].strip()
		if description > '':
			book.info['description'] = {0: unicode(description,'macroman')}
		name_format = file[5].partition('Names: ')[2].strip().lower() # Full Partial
		book.display['columns'] = eval(file[6].partition('Rows: ')[2].strip())
		book.display['rows'] = eval(file[7].partition('Columns: ')[2].strip())
		nbcolors = eval(file[8].partition('Entries: ')[2].strip())
		prefix = file[9].partition('Prefix: ')[2].strip()
		if prefix > '':
			prefix = unicode(prefix+' ','macroman')
		suffix = file[10].partition('Suffix: ')[2].strip()
		if suffix > '':
			suffix = unicode(' '+suffix,'macroman')
		type = file[11].partition('Type: ')[2].strip() # hifi Process Spot Mixed
		if type == 'Spot':
			spot = True
		models = file[12].partition('Models: ')[2].strip().split() # hifi Lab RGB CMYK
		preferredmodel = file[13].partition('PreferredModel: ')[2].strip()
		pos = 14
		if version == 'ACF 2.1':
			nbinks = int(file[pos].partition('Inks: ')[2].strip())
			pos = pos+1
			book.inks = []
			for i in range(nbinks):
				book.inks.append(file[pos].strip())
				pos = pos+1
		pos = pos+1
		for i in range(nbcolors):
			item = Color()
			item.id = 'col'+str(i+1)
			for model in models:
				colors = file[pos].strip().split()
				for k in range(len(colors)):
					if model == 'RGB':
						colors[k] = eval(colors[k])/65535
					else:
						colors[k] = eval(colors[k])
				item.values[model] = tuple(colors)
				pos = pos+1
			if type == 'Mixed':
				col_type = file[pos].strip()
				if col_type == 'Spot' or spot:
					item.attr.append('spot')
				pos = pos+1
			item.info['name'] = {0: prefix+unicode(file[pos].strip(),'macroman')+suffix}
			item.preferredmodel = preferredmodel
			book.items.append(item)
			pos = pos+1

bcf_model = {1: 'RGB', 2: 'CMYK',8: 'hifi', 16: 'Mixed'}

class adobe_bcf(Codec):
	"""Binary Color Format"""
	ext = ('bcf',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(7)
		file.close()
		if struct.unpack('7s', data)[0] in ('ACF 1.0','ACF 2.1','BCF 2.0'):
			return True
	@staticmethod
	def read(book,file):
		file = open(file)
		version = struct.unpack('8s',file.read(8))[0].split('\x00', 1)[0]
		name = struct.unpack('32s',file.read(32))[0].split('\x00', 1)[0]
		if name > '':
			book.info['name'] = {0: unicode(name,'macroman')}
		book.info['version'] = unicode(struct.unpack('8s',file.read(8))[0].split('\x00', 1)[0],'macroman')
		copyright = struct.unpack('32s',file.read(32))[0].split('\x00', 1)[0]
		if copyright > '':
			book.info['copyright'] = {0: unicode(copyright,'macroman')}
		description = struct.unpack('512s',file.read(512))[0].split('\x00', 1)[0]
		if description > '':
			book.info['description'] = {0: unicode(description,'macroman')}
		names, book.display['columns'], book.display['rows'], nbcolors =  struct.unpack('>4H',file.read(8))
		prefix =  struct.unpack('12s',file.read(12))[0].split('\x00', 1)[0]
		if prefix > '':
			prefix = unicode(prefix+' ','macroman')
		suffix = struct.unpack('4s',file.read(4))[0].split('\x00', 1)[0]
		if suffix > '':
			suffix = unicode(' '+suffix,'macroman')
		type, XYZ, CMYK, RGB, preferredmodel = struct.unpack('>5h',file.read(10))
		preferredmodel = bcf_model[preferredmodel]
		if version in ('ACF 2.1','BCF 2.0'):
			extender = struct.unpack('>H',file.read(2))[0]
			if extender  == 1:
				description2 = struct.unpack('100s',file.read(100))[0].split('\x00', 1)[0]
				book.info['description'][0] = book.info['description'][0]+unicode(description2,'macroman')
			inks,nbinks,Lab = struct.unpack('>3H',file.read(6))
			file.seek(24, 1)
			if inks  == 1:
				book.inks = []
				for i in range(nbinks):
					book.inks.append(struct.unpack('>10s 10s H 32s',file.read(54)))
		for i in range(nbcolors):
			item = Color()
			item.id = 'col'+str(i+1)
			if XYZ == 1:
				X,Y,Z  = struct.unpack('>3H',file.read(6))
				item.values['XYZ'] = (X/655.35,Y/655.35,Z/655.35)
			elif 'Lab' in vars() and Lab == 1:
				item.values['Lab'] = struct.unpack('>3h',file.read(6))
			else:
				file.seek(6, 1)
			if CMYK == 1:
				C,M,Y,K = struct.unpack('>4H',file.read(8))
				item.values['CMYK'] = (C/65535,M/65535,Y/65535,K/65535)
			else:
				file.seek(8, 1)
			if RGB == 1:
				R,G,B = struct.unpack('>3H',file.read(6))
				item.values['RGB'] = (R/65535,G/65535,B/65535)
			else:
				file.seek(6, 1)
			if version in ('ACF 2.1','BCF 2.0') and type in (8,16):
				col_nbinks = struct.unpack('>H',file.read(2))[0]
				hifi = []
				for j in range(col_nbinks):
					hifi.append( struct.unpack('>2H',file.read(4)))
				item.values['hifi'] = tuple(hifi)
				file.seek((8-col_nbinks)*4, 1)
			col_type = struct.unpack('>H',file.read(2))[0]
			if col_type == 1:
				item.attr.append('spot')
			if version in ('ACF 2.1','BCF 2.0') and type in (8,16):
				col_preferredmodel = struct.unpack('>H',file.read(2))[0]
				item.preferredmodel = bcf_model[col_preferredmodel]
			else:
				item.preferredmodel = preferredmodel
			name = struct.unpack('32s',file.read(32))[0].split('\x00', 1)[0]
			if name > '':
				item.info['name'] = {0: prefix+unicode(name,'macroman')+suffix}
			book.items.append(item)
		file.close()

class adobe_clr(Codec):
	"""Flash Color Set"""
	ext = ('clr',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(4)
		file.close()
		if data == '\xff\xff\x00\x00':
			return True
	@staticmethod
	def read(book,file):
		file = open(file)
		file.seek(16, 1)
		nbcolors = struct.unpack('<H',file.read(2))[0]
		file.seek(15, 1)
		for i in range(nbcolors):
			item = Color()
			item.id = 'col'+str(i+1)
			file.seek(1, 1)
			R,G,B,a = struct.unpack('4B',file.read(4))
			item.values['RGBa'] = (R/255,G/255,B/255,a/255)
			file.seek(2, 1)
			H,S,L = struct.unpack('<3H',file.read(6))
			item.values['HSL'] = (H/240,S/240,L/240)
			file.seek(2, 1)
			book.items.append(item)
		file.close()

class autocad_acb(Codec):
	"""AutoCAD Color Book"""
	ext = ('acb',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag == 'colorBook':
			return True
	@staticmethod
	def read(book,file):
		xml = etree.parse(file).getroot()
		book.info['name'] = {0: unicode(list(xml.getiterator('bookName'))[0].text)}
		if len(list(xml.getiterator('majorVersion'))) > 0:
			book.info['version'] = list(xml.getiterator('majorVersion'))[0].text+'.'+list(xml.getiterator('minorVersion'))[0].text
		nbcolors = len(list(xml.getiterator('colorEntry')))
		book.display['columns'] = 0
		i = 0
		for colorPage in xml.getiterator('colorPage'):
			book.display['columns'] = max(book.display['columns'],len(list(colorPage.getiterator('colorEntry'))))
		breaks = []
		encrypted = False
		for colorPage in xml.getiterator('colorPage'):
			for colorEntry in colorPage.getiterator('colorEntry'):
				item = Color()
				item.id = 'col'+str(i+1)
				item.info['name'] = {0: unicode(colorEntry.find('colorName').text)}
				if colorEntry.find('RGB8Encrypt'):
					encrypted = True
				elif colorEntry.find('RGB8'):
					item.values['RGB'] = (eval(colorEntry.find('RGB8').find('red').text)/255,eval(colorEntry.find('RGB8').find('green').text)/255,eval(colorEntry.find('RGB8').find('blue').text)/255)
				book.items.append(item)
				i += 1
			if len(list(colorPage.getiterator('colorEntry'))) < book.display['columns'] and i<nbcolors:
				breaks.append(i)
		if len(breaks)>0:
			book.display['breaks'] = breaks
		if encrypted:
			sys.stderr.write(file+": this script can't decode encrypted RGB values\n")

class ral_bcs(Codec):
	"""RAL"""
	ext = ('bcs',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(4)
		file.close()
		if struct.unpack('b3s', data)[1] in ('clf','rgb','atl'):
			return True
	@staticmethod
	def read(book,file):
		filesize = os.path.getsize(file)
		file = open(file)
		offset, sig = struct.unpack('B 3s',file.read(4))
		file.seek(offset+1, 0)
		nbcolors = struct.unpack('<H',file.read(2))[0]
		length = struct.unpack('B',file.read(1))[0]
		name_tmp = struct.unpack(str(length)+'s',file.read(length))[0].split(':')
		book.info['name'] = {0: unicode(name_tmp[0].split('English_')[1],'utf-8')}
		if name_tmp[1].split('German_')[1] != book.info['name'][0]:
			book.info['name']['de'] = unicode(name_tmp[1].split('German_')[1],'utf-8')
		file.seek(1, 1)
		for i in range(nbcolors):
			item = Color()
			item.id = 'col'+str(i+1)
			length = struct.unpack('B',file.read(1))[0]
			if length > 0:
				item.info['name'] =  {0: unicode(struct.unpack(str(length)+'s',file.read(length))[0],'latin1')}
			item.values['Lab'] = struct.unpack('<3f',file.read(12))
			if sig == 'clf':
				item.attr.append('spot')
			book.items.append(item)
			if file.tell() == filesize: break
		file.close()

class corel_cpl(Codec):
	"""Corel Palette"""
	ext = ('cpl',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(2)
		file.close()
		if data in ('\xcc\xbc','\xcc\xdc','\xcd\xbc','\xcd\xdc','\xdd\xdc','\xdc\xdc','\xcd\xdd'):
			return True
	@staticmethod
	def read(book,file):
		spot=False
		file = open(file)
		version = file.read(2)
		if version == '\xdc\xdc': #custom palettes
			length = struct.unpack('B',file.read(1))[0]
			if length > 0:
				book.info['name'] =  {0: unicode(struct.unpack(str(length)+'s',file.read(length))[0],'latin1')}
			nbcolors = struct.unpack('<H',file.read(2))[0]
		elif version in ('\xcc\xbc','\xcc\xdc'):
			nbcolors = struct.unpack('<H',file.read(2))[0]
		else:
			nbheaders = struct.unpack('<L',file.read(4))[0]
			headers = {}
			for i in range(nbheaders):
				id,offset = struct.unpack('<2L',file.read(8))
				headers[id] = offset
			# Header 0: Name
			file.seek(headers[0], 0)
			length = struct.unpack('B',file.read(1))[0]
			if length > 0:
				if version == '\xcd\xdc':
					book.info['name'] =  {0: unicode(struct.unpack(str(length)+'s',file.read(length))[0],'latin1')}
				else:
					book.info['name'] =  {0: unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_le')}
			# Header 1: Palette Type
			file.seek(headers[1], 0)
			type = struct.unpack('<H',file.read(2))[0]
			# Header 2: Number of colors
			file.seek(headers[2], 0)
			nbcolors = struct.unpack('<H',file.read(2))[0]
			# Header 3: Custom inks
			if 3 in headers:
				file.seek(headers[3], 0)
				nbinks = struct.unpack('<H',file.read(2))[0]
				book.inks = struct.unpack('<'+str(nbinks)+'H',file.read(nbinks*2))
			# Header 5: UI informations
			if 5 in headers:
				file.seek(headers[5], 0)
				book.display['columns'],book.display['rows'] = struct.unpack('<2H',file.read(4))
			file.seek(headers[2]+2, 0)
			if 'columns' not in book.display:
				if type in (38,):
					book.display['columns'] = 9
					book.display['rows'] = 8
				elif type in (23,26,27,28,29,30,32,32,35,36,37,39):
					book.display['columns'] = 7
					book.display['rows'] = 6
				elif type in (12,24,33,34):
					book.display['columns'] = 7
					book.display['rows'] = 7
			if type in (3,8,9,10,11,16,17,18,20,21,22,23,26,27,28,29,30,31,32,35,36,37):
				spot = True
		if version in ('\xcd\xbc','\xcd\xdc','\xcd\xdd') and type < 38 and type not in(5,16):
			long = True
		else:
			long = False
		row = {}
		col = {}
		breaks = []
		for i in range(nbcolors):
			item = Color()
			if long:
				item.id = struct.unpack('<L',file.read(4))[0]
			else:
				item.id = 'col'+str(i+1)
			model =  struct.unpack('<H',file.read(2))[0]
			file.seek(2, 1)
			if model == 2:
				file.seek(4, 1)
				C,M,Y,K =  struct.unpack('4B',file.read(4))
				item.values['CMYK'] = (C/100,M/100,Y/100,K/100)
			elif model in (3,17):
				file.seek(4, 1)
				C,M,Y,K =  struct.unpack('4B',file.read(4))
				item.values['CMYK'] = (C/255,M/255,Y/255,K/255)
			elif model == 4:
				file.seek(4, 1)
				C,M,Y =  struct.unpack('3B',file.read(3))
				item.values['CMY'] = (C/255,M/255,Y/255)
				file.seek(1, 1)
			elif model in (5,21):
				file.seek(4, 1)
				B,G,R = struct.unpack('3B',file.read(3))
				item.values['RGB'] = (R/255,G/255,B/255)
				file.seek(1, 1)
			elif model == 6:
				file.seek(4, 1)
				H,S,V = struct.unpack('<H2B',file.read(4))
				item.values['HSV'] = (H/360,S/255,V/255)
			elif model == 7:
				file.seek(4, 1)
				H,L,S = struct.unpack('<H2B',file.read(4))
				item.values['HSL'] = (H/360,S/255,L/255)
			elif model == 9:
				file.seek(4, 1)
				K =  struct.unpack('B',file.read(1))[0]
				item.values['Gray'] = (1-K/255,)
				file.seek(3, 1)
			elif model == 11:
				file.seek(4, 1)
				Y,I,Q =  struct.unpack('3B',file.read(3))
				item.values['YIQ'] = (Y/255,(I-100)/128,(Q-100)/128)
				file.seek(1, 1)
			elif model == 12:
				file.seek(4, 1)
				L,a,b =  struct.unpack('B 2b',file.read(3))
				item.values['Lab'] = (L/2.55,a,b)
				file.seek(1, 1)
			elif model == 15:
				file.seek(2, 1)
				Y,O,M,C,G,K =  struct.unpack('6B',file.read(6))
				item.values['6CLR'] = (C/255,M/255,Y/255,K/255,O/255,G/255)
			elif model == 18:
				file.seek(4, 1)
				L,a,b =  struct.unpack('3B',file.read(3))
				item.values['Lab'] = (L/2.55,a-128,b-128)
				file.seek(1, 1)
			else:
				file.seek(8, 1)
				sys.stderr.write('unknown color model ['+str(model)+']\n')
			if long:
				model2 =  struct.unpack('<H',file.read(2))[0]
				file.seek(2, 1)
				if model2 == model:
					file.seek(8, 1)
				else:
					if model2 == 2:
						file.seek(4, 1)
						C,M,Y,K =  struct.unpack('4B',file.read(4))
						item.values['CMYK'] = (C/100,M/100,Y/100,K/100)
					elif model2 in (3,17):
						file.seek(4, 1)
						C,M,Y,K =  struct.unpack('4B',file.read(4))
						item.values['CMYK'] = (C/255,M/255,Y/255,K/255)
					elif model2 == 4:
						file.seek(4, 1)
						C,M,Y =  struct.unpack('3B',file.read(3))
						item.values['CMY'] = (C/255,M/255,Y/255)
						file.seek(1, 1)
					elif model2 in (5,21):
						file.seek(4, 1)
						B,G,R = struct.unpack('3B',file.read(3))
						item.values['RGB'] = (R/255,G/255,B/255)
						file.seek(1, 1)
					elif model2 == 6:
						file.seek(4, 1)
						H,S,V = struct.unpack('<H2B',file.read(4))
						item.values['HSV'] = (H/360,S/255,V/255)
					elif model2 == 7:
						file.seek(4, 1)
						H,L,S = struct.unpack('<H2B',file.read(4))
						item.values['HSL'] = (H/360,S/255,L/255)
					elif model2 == 9:
						file.seek(4, 1)
						K =  struct.unpack('B',file.read(1))[0]
						item.values['Gray'] = (1-K/255,)
						file.seek(3, 1)
					elif model2 == 11:
						file.seek(4, 1)
						Y,I,Q =  struct.unpack('3B',file.read(3))
						item.values['YIQ'] = (Y/255,(I-100)/128,(Q-100)/128)
						file.seek(1, 1)
					elif model2 == 12:
						file.seek(4, 1)
						L,a,b =  struct.unpack('B 2b',file.read(3))
						item.values['Lab'] = (L/2.55,a,b)
						file.seek(1, 1)
					elif model2 == 15:
						file.seek(2, 1)
						Y,O,M,C,G,K =  struct.unpack('6B',file.read(6))
						item.values['6CLR'] = (C/255,M/255,Y/255,K/255,O/255,G/255)
					elif model2 == 18:
						file.seek(4, 1)
						L,a,b =  struct.unpack('3B',file.read(3))
						item.values['Lab'] = (L/2.55,a-128,b-128)
						file.seek(1, 1)
					else:
						file.seek(8, 1)
						sys.stderr.write('unknown color model ['+str(model2)+']\n')
			length = struct.unpack('B',file.read(1))[0]
			if length > 0:
				if version in ('\xdc\xdc','\xcc\xdc') or (version == '\xcd\xdc' and type not in (16,)):
					item.info['name'] =  {0: unicode(struct.unpack(str(length)+'s',file.read(length))[0],'latin1')}
				else:
					item.info['name'] =  {0: unicode(struct.unpack(str(length*2)+'s',file.read(length*2))[0],'utf_16_le')}
			if version == '\xcd\xdd':
				row[i], col[i] = struct.unpack('<2L',file.read(8))
				if row[i] > 0 and col[i] == 0 and col[i-1] < book.display['columns']-1:
					breaks.append(i)
				file.seek(4, 1)
			if spot:
				item.attr.append('spot')
			if 'name' in item.info and (find(item.info['name'][0],'NONASSIGNED') >= 0 or find(item.info['name'][0],'UNASSIGNED') >= 0):
				item = Spacer()
			book.items.append(item)
		if len(breaks)>0:
			book.display['breaks'] = breaks
		file.close()

class quark_qcl(Codec):
	"""QuarkXPress Color Library"""
	ext = ('qcl',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag == 'cgats17':
			format = 'quark_qcl'
			return True
	@staticmethod
	def read(book,file):
		xml = etree.parse(file).getroot()
		book.info['name'] = {0: unicode(list(xml.getiterator('file_descriptor'))[0].text)}
		book.info['copyright'] = {0: unicode(list(xml.getiterator('originator'))[0].text)}
		preferredmodel = list(xml.getiterator('default_color_space'))[0].text.strip()
		usage = list(xml.getiterator('color_usage_recommendation'))[0].text
		name_field_info = list(xml.getiterator('name_field_info'))
		if len(name_field_info) > 0:
			prefix = {}
			suffix = {}
			for name in name_field_info:
				nid = eval(name.attrib['format_id'])-1
				prefix[nid], suffix[nid] =  unicode(name.attrib['long_form']).split('%n')
		ui_spec =  os.path.dirname(file)+'/'+list(xml.getiterator('ui_spec'))[0].text
		if os.path.isfile(ui_spec):
			ui = etree.parse(ui_spec).getroot()
			book.display['columns'] = eval(list(ui.getiterator('rows_per_page'))[0].text)
			breaks = list(ui.getiterator('column_break'))
			if len(breaks)>0:
				for i in range(len(breaks)):
					breaks[i] = eval(breaks[i].text)
				book.display['breaks'] = breaks
		else:
			sys.stderr.write('ui file '+ui_spec+' doesn\'t exist\n')
		fields = xml.getiterator('field_info')
		data_format = {}
		for field in fields:
			data_format[field.attrib['name']] = field.attrib['pos']
		colors = xml.getiterator('tr')
		i = 0
		for color in colors:
			item = Color()
			item.id = 'col'+str(i+1)
			name = unicode(color.getchildren()[eval(data_format['SAMPLE_ID'])-1].text)
			if data_format.has_key('NAME_FORMAT_ID'):
				nid = eval(color.getchildren()[eval(data_format['NAME_FORMAT_ID'])-1].text)-1
				item.info['name'] = {0: prefix[nid]+name+suffix[nid]}
			elif name > u'':
				item.info['name'] = {0: name}
			if data_format.has_key('LAB_L'):
				item.values['Lab'] = (eval(color.getchildren()[eval(data_format['LAB_L'])-1].text),\
											  eval(color.getchildren()[eval(data_format['LAB_A'])-1].text),\
											  eval(color.getchildren()[eval(data_format['LAB_B'])-1].text))
			if data_format.has_key('RGB_R'):
				item.values['RGB'] = (eval(color.getchildren()[eval(data_format['RGB_R'])-1].text)/255,\
											  eval(color.getchildren()[eval(data_format['RGB_G'])-1].text)/255,\
											  eval(color.getchildren()[eval(data_format['RGB_B'])-1].text)/255)
			if data_format.has_key('CMYK_C'):
				item.values['CMYK'] = (eval(color.getchildren()[eval(data_format['CMYK_C'])-1].text)/100,\
											   eval(color.getchildren()[eval(data_format['CMYK_M'])-1].text)/100,\
											   eval(color.getchildren()[eval(data_format['CMYK_Y'])-1].text)/100,\
											   eval(color.getchildren()[eval(data_format['CMYK_K'])-1].text)/100)
			if data_format.has_key('PC6_1'):
				item.values['6CLR'] = (eval(color.getchildren()[eval(data_format['PC6_1'])-1].text)/100,\
											  eval(color.getchildren()[eval(data_format['PC6_2'])-1].text)/100,\
											  eval(color.getchildren()[eval(data_format['PC6_3'])-1].text)/100,\
											  eval(color.getchildren()[eval(data_format['PC6_4'])-1].text)/100,\
											  eval(color.getchildren()[eval(data_format['PC6_5'])-1].text)/100,\
											  eval(color.getchildren()[eval(data_format['PC6_6'])-1].text)/100)
			item.preferredmodel = preferredmodel
			if usage in ('4','5'):
				item.attr.append('spot')
			book.items.append(item)
			i += 1

class riff_pal(Codec):
	"""RIFF Palette"""
	ext = ('pal',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(12)
		RIFF, size, PAL = struct.unpack('<4s L 4s', data)
		file.close()
		if  RIFF == 'RIFF' and PAL == 'PAL ':
			return True
	@staticmethod
	def read(book,file):
		file = open(file)
		file.seek(12, 0)
		chunk = struct.unpack('<4s L', file.read(8))
		while chunk[0] != 'data':
			file.seek(chunk[1], 1)
			chunk = struct.unpack('<4s L', file.read(8))
		version, nbcolors = struct.unpack('<2H',file.read(4))
		for i in range(nbcolors):
			item = Color()
			item.id = 'col'+str(i+1)
			R,G,B = struct.unpack('3B',file.read(3))
			item.values['RGB'] = (R/255,G/255,B/255)
			file.seek(1, 1)
			book.items.append(item)
		file.close()

class colorschemer(Codec):
	"""ColorSchemer"""
	ext = ('cs',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(2)
		file.close()
		if struct.unpack('<H', data)[0] == 3:
			return True
	@staticmethod
	def read(book,file):
		file = open(file)
		version, nbcolors = struct.unpack('<2H',file.read(4))
		file.seek(4, 1)
		for i in range(nbcolors):
			item = Color()
			item.id = 'col'+str(i+1)
			R,G,B = struct.unpack('3B',file.read(3))
			item.values['RGB'] = (R/255,G/255,B/255)
			file.seek(1, 1)
			length = struct.unpack('<L',file.read(4))[0]
			if length > 0:
				item.info['name'] =  {0: unicode(struct.unpack(str(length)+'s',file.read(length))[0],'latin1')}
			file.seek(11, 1)
			book.items.append(item)
		file.close()

class gimp_gpl(Codec):
	"""Gimp Palette"""
	ext = ('gpl',)
	@staticmethod
	def test(file):
		file = open(file)
		data = file.read(12)
		file.close()
		if struct.unpack('12s', data)[0] == 'GIMP Palette':
			return True
	@staticmethod
	def read(book,file):
		file = open(file, 'U').readlines()[1:]
		if file[0][:5] == 'Name:':
			name = unicode(file[1].partition('Name: ')[2].strip(),'utf-8')
			if name > u'':
				book.info['name'] = {0: name}
			file = file[1:]
		if file[0][:8] == 'Columns:':
			cols = int(file[0].partition('Columns: ')[2].strip()) # max 64 in Gimp 2.6
			if cols > 0:
				book.display['columns'] = cols
			file = file[1:]
		i = 0
		for line in file:
			if line[0] == '#':
				continue
			else:
				entry = line.split(None,3)
				if entry[0].isdigit() and entry[1].isdigit() and entry[2].isdigit():
					item = Color()
					item.id = 'col'+str(i+1)
					item.values['RGB'] = (int(entry[0])/255,int(entry[1])/255,int(entry[2])/255)
					if len(entry) > 3 and entry[3].strip() not in ('Untitled','Sans titre'): # other languages to be added
						item.info['name'] =  {0: unicode(entry[3].strip(),'utf-8')}
					book.items.append(item)
					i += 1
				else:	
					sys.stderr.write('incorrect line: '+line.encode('utf-8'))
				
	@staticmethod
	def write(book,lang=0):
		gpl = 'GIMP Palette\n'
		if 'name' in book.info:
			gpl += 'Name: '+book.info['name'][lang]+'\n'
		if 'columns' in book.display and book.display['columns'] > 0:
			gpl += 'Columns: '+str(book.display['columns'])+'\n'
		gpl += '#'
		
		gpl += gimp_gpl.writem(book.items)
		
		return gpl.encode('utf-8')

	@staticmethod
	def writem(items,lang=0):
		gpl_tmp = u''
		for item in items:
			if isinstance(item,Color):
				R,G,B = item.toRGB8()
				gpl_tmp += '\n'+str(R).rjust(3)+' '+str(G).rjust(3)+' '+str(B).rjust(3)
				if item.info['name']:
					gpl_tmp += '\t'+item.info['name'][lang]
			elif isinstance(item,Group):
				gpl_tmp += '\n# '+item.info['name'][lang]
				gpl_tmp += gimp_gpl.writem(item.items)
			elif isinstance(item,Spacer):
				gpl_tmp += '\n  0   0   0'
		return gpl_tmp


class scribus(Codec):
	"""Scribus Swatch"""
	ext = ('xml',)
	@staticmethod
	def write(book,lang=0):
		scsw = '<?xml version="1.0" encoding="UTF-8"?>\n<SCRIBUSCOLORS Name="'+book.info['name'][lang]+'">\n'
		scsw += scribus.writem(book.items)
		scsw += '</SCRIBUSCOLORS>'
		return scsw.encode('utf-8')

	@staticmethod
	def writem(items,lang=0):
		scsw_tmp = u''
		for item in items:
			if isinstance(item,Color):
				values = unicc(item.values)
				scsw_tmp += '\t<COLOR '
				if 'CMYK' in values:
					C,M,Y,K = values['CMYK']
					scsw_tmp += 'CMYK="#'+hex2(C*255)+hex2(M*255)+hex2(Y*255)+hex2(K*255)+'"'
				elif 'Gray' in values:
					K = values['Gray'][0]
					scsw_tmp += 'CMYK="#000000'+hex2(K*255)+'"'
				else:
					if item.toRGB8():
						R,G,B = item.toRGB8()
						scsw_tmp += 'RGB="#'+hex2(R)+hex2(G)+hex2(B)+'"'
				if 'name' in item.info:
					scsw_tmp += ' NAME="'+item.info['name'][lang]+'"'
				if 'spot' in item.attr:
					scsw_tmp += ' Spot="1"'
				scsw_tmp += ' />\n'
			elif isinstance(item,Group):
				scsw_tmp += scribus.writem(item.items)
		return scsw_tmp


class html(Codec):
	"""HTML document"""
	ext = ('html','htm')
	@staticmethod
	def write(book,lang=0):
		htm = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta content="text/html; charset=UTF-8" http-equiv="content-type" />
<title>SwatchBook</title>
<style type="text/css">
	.swatch {
		width:30px;
		height:30px;
		float:left;
	}
	.group {
		border: 1px solid silver;
		clear: both;
	}
	.group_name {
		clear: both;
	}
	.group_descr {
		clear: both;
	}
	.clearall {
		clear: both;
	}
</style>
</head>

<body>
'''
		if 'name' in book.info:
			htm += '<p id="name">'+book.info['name'][lang]+'</p>\n'
		if 'description' in book.info:
			htm += '<p id="description">'+book.info['description'][lang]+'</p>\n'
		if 'copyright' in book.info:
			htm += '<p id="copyright">'+book.info['copyright'][lang]+'</p>\n'
		if 'version' in book.info:
			htm += '<p id="version">'+book.info['version']+'</p>\n'
		htm += '<div id="swatchbook"'
		if 'columns' in book.display:
			htm += ' style="width:'+str(book.display['columns']*30)+'px"'
		htm += '>\n'

		htm += html.writem(book.items,book.display['breaks'])[0]

		htm += '</div>\n</body>\n</html>'

		return htm.encode('utf-8')

	@staticmethod
	def writem(items,breaks,count=0,lang=0):
		html_tmp = u''
		for item in items:
			if isinstance(item,Group):
				html_tmp += '<div class="group"><div class="group_name">'+item.info['name'][0]+'</div>\n'
				htm,count = html.writem(item.items,breaks,count)
				html_tmp += htm+'\n<div class="group_descr">'
				if 'description'in item.info:
					html_tmp += item.info['description'][lang]
				html_tmp += '</div></div>\n'
			elif isinstance(item,Color):
				R,G,B = item.toRGB8()
				html_tmp += '<div class="swatch" style="background-color:#'+hex2(R)+hex2(G)+hex2(B)
				if 'name' in item.info:
					html_tmp += '" title="'+item.info['name'][lang]
				html_tmp += '"></div>\n'
			elif isinstance(item,Spacer):
				html_tmp += '<div class="swatch"></div>\n'
			count += 1
			if count in breaks:
				html_tmp += '<br class="clearall" />\n'
		return html_tmp,count
				

class sbxml(Codec):
	"""SwatchBook XML"""
	ext = ('sb',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag == 'SwatchBook' and etree.parse(file).getroot().attrib['version'] == '0.1':
			format = 'sbxml'
			return True

	@staticmethod
	def read(book,file):
		xml = etree.parse(file).getroot()
		for elem in xml:
			if elem.tag in ('group','color','spacer'):
				sbxml.readitem(book,elem)
			elif elem.tag in ('name','description','copyright'):
				if elem.tag not in book.info:
					book.info[elem.tag] = {}
				if 'lang' in elem.attrib:
					book.info[elem.tag][elem.attrib['lang']] = elem.text
				else:
					book.info[elem.tag][0] = elem.text
			elif elem.tag in ('version'):
				book.info['version'] = elem.text
			elif elem.tag in ('columns','rows'):
				book.display[elem.tag] = int(elem.text)
			elif elem.tag in ('breaks'):
				book.display['breaks'] = elem.text.split()
			elif elem.tag in ('colorspace'):
				book.profiles[elem.attrib['id']] = elem.attrib['href']

	@staticmethod
	def readitem(parent,item):
		if item.tag == 'group':
			bitem = Group()
			for elem in item:
				if elem.tag in ('group','color'):
					sbxml.readitem(bitem,elem)
				elif elem.tag in ('name','description'):
					if elem.tag not in bitem.info:
						bitem.info[elem.tag] = {}
					if 'lang' in elem.attrib:
						bitem.info[elem.tag][elem.attrib['lang']] = elem.text
					else:
						bitem.info[elem.tag][0] = elem.text
		elif item.tag == 'color':
			bitem = Color()
			if 'spot' in item.attrib and item.attrib['spot'] == '1':
				bitem.attr.append('spot')
			for elem in item:
				if elem.tag in ('RGB','CMYK','Lab','Gray','CMY','XYZ','YIQ'):
					values = elem.text.split()
					for i in range(len(values)):
						values[i] = eval(values[i])
					if 'space' in elem.attrib:
						bitem.values[(elem.tag,elem.attrib['space'])] = values
					else:
						bitem.values[elem.tag] = values
				elif elem.tag in ('name','description','copyright'):
					if elem.tag not in bitem.info:
						bitem.info[elem.tag] = {}
					if 'lang' in elem.attrib:
						bitem.info[elem.tag][elem.attrib['lang']] = elem.text
					else:
						bitem.info[elem.tag][0] = elem.text
		elif item.tag == 'spacer':
			bitem = Spacer()
		parent.items.append(bitem)
			

	@staticmethod
	def write(book):
		xml = '<?xml version="1.0" encoding = "UTF-8"?>\n<SwatchBook version="0.1">'
		for info in ('name','description','copyright'):
			if info in book.info:
				for lang in book.info[info]:
					if lang == 0:
						xml += '<'+info+'>'+book.info[info][0]+'</'+info+'>'
					else:
						xml += '<'+info+' label="'+lang+'">'+book.info[info][lang]+'</'+info+'>'
		if 'version' in book.info:
			xml += '<version>'+book.info['version']+'</version>'
		if 'columns' in book.display:
			xml += '<columns>'+str(book.display['columns'])+'</columns>'
		if 'rows' in book.display:
			xml += '<rows>'+str(book.display['rows'])+'</rows>'
		if len(book.display['breaks']) > 0:
			xml += '<breaks>'+book.display['breaks'].join(' ')+'</breaks>'

		xml += unicode(sbxml.writem(book.items),'utf-8')
		for profile in book.profiles:
			xml += '<colorspace id="'+profile+'" href="'+book.profiles[profile]+'" />'

		xml += '</SwatchBook>'

		return xml.encode('utf-8')

	@staticmethod
	def writem(items):
		xml = u''
		for item in items:
			if isinstance(item,Group):
				xml += '<group'
				if item.id:
					xml += ' id="'+item.id+'"'
				xml += '>'
				for info in ('name','description'):
					if info in item.info:
						for lang in item.info[info]:
							if lang == 0:
								xml += '<'+info+'>'+item.info[info][0]+'</'+info+'>'
							else:
								xml += '<'+info+' label="'+lang+'">'+item.info[info][lang]+'</'+info+'>'
				xml += sbxml.writem(item.items)
				xml += '</group>'
			elif isinstance(item,Color):
				xml += '<color'
				if item.id:
					xml += ' id="'+item.id+'"'
				if 'spot' in item.attr:
					xml += ' spot="1"'
				xml += '>'
				for info in ('name','description'):
					if info in item.info:
						for lang in item.info[info]:
							if lang == 0:
								xml += '<'+info+'>'+item.info[info][0]+'</'+info+'>'
							else:
								xml += '<'+info+' label="'+lang+'">'+item.info[info][lang]+'</'+info+'>'
				for model in item.values:
					if isinstance(model,tuple):
						xml += '<'+model[0]+' space="'+model[1]+'">'+' '.join(str(round(x,4)) for x in item.values[model])+'</'+model[0]+'>'
					else:
						xml += '<'+model+'>'+' '.join(str(round(x,4)) for x in item.values[model])+'</'+model+'>'
				xml += '</color>'
		return xml.encode('utf-8')
				

writes = []
reads = []
readexts = {}

for codec in Codec.__subclasses__():
	cname = codec.__name__
	exts = codec.ext
	if codec.read:
		reads.append(cname)
		for ext in exts:
			if ext in readexts.keys():
				readexts[ext].append(cname)
			else:
				readexts[ext] = [cname]
	if codec.write:
		writes.append(cname)
