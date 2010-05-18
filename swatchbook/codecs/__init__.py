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
import struct
import xml.etree.cElementTree as etree
from xml.sax.saxutils import escape as xmlescape
from xml.sax.saxutils import unescape as xmlunescape
from zipfile import *
from swatchbook import *
from string import *

def hex2(val):
	return hex(int(round(val)))[2:].rjust(2,'0')

def unicc(values): # meant to disappear - used in the ASE and Scribus codecs
	values = values.copy()
	for val in values:
		if isinstance(val,tuple):
			values[val[0]] = values[val]
			del values[val]
	return values

class SBCodec(object):
	ext = False
	read = False
	write = False

for codec in os.listdir((dirpath(__file__) or ".")):
	if os.path.splitext(codec)[1] == '.py' and codec not in ('__init__.py','template.py'):
		exec 'from '+os.path.splitext(codec)[0]+' import *'

writes = []
reads = []
readexts = {}

for codec in SBCodec.__subclasses__():
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
