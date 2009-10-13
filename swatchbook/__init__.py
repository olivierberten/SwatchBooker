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

# from http://code.djangoproject.com/browser/django/trunk/django/utils/datastructures.py
class SortedDict(dict):
	"""
	A dictionary that keeps its keys in the order in which they're inserted.
	"""
	def __new__(cls, *args, **kwargs):
		instance = super(SortedDict, cls).__new__(cls, *args, **kwargs)
		instance.keyOrder = []
		return instance

	def __init__(self, data=None):
		if data is None:
			data = {}
		super(SortedDict, self).__init__(data)
		if isinstance(data, dict):
			self.keyOrder = data.keys()
		else:
			self.keyOrder = []
			for key, value in data:
				if key not in self.keyOrder:
					self.keyOrder.append(key)

	def __deepcopy__(self, memo):
		from copy import deepcopy
		return self.__class__([(key, deepcopy(value, memo))
							   for key, value in self.iteritems()])

	def __setitem__(self, key, value):
		super(SortedDict, self).__setitem__(key, value)
		if key not in self.keyOrder:
			self.keyOrder.append(key)

	def __delitem__(self, key):
		super(SortedDict, self).__delitem__(key)
		self.keyOrder.remove(key)

	def __iter__(self):
		for k in self.keyOrder:
			yield k

	def pop(self, k, *args):
		result = super(SortedDict, self).pop(k, *args)
		try:
			self.keyOrder.remove(k)
		except ValueError:
			# Key wasn't in the dictionary in the first place. No problem.
			pass
		return result

	def popitem(self):
		result = super(SortedDict, self).popitem()
		self.keyOrder.remove(result[0])
		return result

	def items(self):
		return zip(self.keyOrder, self.values())

	def iteritems(self):
		for key in self.keyOrder:
			yield key, super(SortedDict, self).__getitem__(key)

	def keys(self):
		return self.keyOrder[:]

	def iterkeys(self):
		return iter(self.keyOrder)

	def values(self):
		return [super(SortedDict, self).__getitem__(k) for k in self.keyOrder]

	def itervalues(self):
		for key in self.keyOrder:
			yield super(SortedDict, self).__getitem__(key)

	def update(self, dict_):
		for k, v in dict_.items():
			self.__setitem__(k, v)

	def setdefault(self, key, default):
		if key not in self.keyOrder:
			self.keyOrder.append(key)
		return super(SortedDict, self).setdefault(key, default)

	def value_for_index(self, index):
		"""Returns the value of the item at the given zero-based index."""
		return self[self.keyOrder[index]]

	def insert(self, index, key, value):
		"""Inserts the key, value pair before the item with the given index."""
		if key in self.keyOrder:
			n = self.keyOrder.index(key)
			del self.keyOrder[n]
			if n < index:
				index -= 1
		self.keyOrder.insert(index, key)
		super(SortedDict, self).__setitem__(key, value)

	def copy(self):
		"""Returns a copy of this object."""
		# This way of initializing the copy means it works for subclasses, too.
		obj = self.__class__(self)
		obj.keyOrder = self.keyOrder[:]
		return obj

	def __repr__(self):
		"""
		Replaces the normal dict.__repr__ with a version that returns the keys
		in their sorted order.
		"""
		return '{%s}' % ', '.join(['%r: %r' % (k, v) for k, v in self.items()])

	def clear(self):
		super(SortedDict, self).clear()
		self.keyOrder = []

class SwatchBook(object):
	"""Output values
       RGB,HSV,HSL,CMY,CMYK,6CLR: 0 -> 1
       YIQ: Y 0 -> 1 : IQ -0.5 -> 0.5
       Lab: L 0 -> 100 : ab -128 -> 127
       XYZ: 0 -> ~100 (cfr. ref)"""

	def __init__(self, file=False):
		# Informations
		self.info = {}
		self.ids = {}
		self.inks = False
		# Display informations
		self.display = {}
		# Color Profiles
		self.profiles = {}
		# Swatches
		self.items = SortedDict()

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
		if ext in codecs.readexts:
			for codec in codecs.readexts[ext]:
				test = eval('codecs.'+codec).test(file)
				if test: break
			else:
				codec = False
		if codec:
			eval('codecs.'+codec).read(self,file)
			if sys.getfilesystemencoding() == 'UTF-8' and isinstance(file,unicode):
				filename =  os.path.splitext(os.path.basename(file))[0]
			else:
				filename =  os.path.splitext(os.path.basename(file))[0].decode(sys.getfilesystemencoding())
			if 'name' not in self.info:
				self.info['name'] = {0: filename.replace('_',' ')}

		else:
			sys.stderr.write(file.encode('utf-8')+': unsupported input format\n')

	def write(self,format,output=None):
		import swatchbook.codecs as codecs
		if format in codecs.writes:
			codec = eval('codecs.'+format)
			if output == None:
				print codec.write(self)
			else:
				content = codec.write(self)
				# TODO check if writable
				bookfile = open(output, 'wb')
				bookfile.write(content)
				bookfile.close()
		else:
			sys.stderr.write('unsupported output format\n')

class Group(object):
	def __init__(self):
		self.info = {}
		self.items = SortedDict()

class Swatch(object):
	def __init__(self,book):
		self.info = {}
		self.book = book

class Spacer(object):
	def __init__(self):
		pass

class Break(object):
	def __init__(self):
		pass

class Color(Swatch):
	def __init__(self,book):
		super(Color, self).__init__(book)
		self.values = SortedDict()
		self.attr = []

	def toRGB(self,prof_out=False):
		for key in self.values:
			if key[1]:
				prof_in = self.book.profiles[key[1]].uri
			else:
				prof_in = False
			if toRGB(key[0],self.values[key],prof_in,prof_out):
				return toRGB(key[0],self.values[key],prof_in,prof_out)
				break
		else:
			return False
			
	def toRGB8(self,prof_out=False):
		if self.toRGB(prof_out):
			R,G,B = self.toRGB(prof_out)
			return (int(round(R*0xFF)),int(round(G*0xFF)),int(round(B*0xFF)))
		else:
			return False

class Gradient(Swatch):
	def __init__(self,book):
		super(Gradient, self).__init__(book)

class Pattern(Swatch):
	def __init__(self,book):
		super(Pattern, self).__init__(book)
		self.colors = []

