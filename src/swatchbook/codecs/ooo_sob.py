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

from swatchbook.codecs import *
import tempfile

class ooo_sob(SBCodec):
	"""OpenOffice.org Bitmap Patterns"""
	ext = ('sob',)
	@staticmethod
	def test(file):
		try:
			zip = ZipFile(file)
			if 'Content.xml' in zip.namelist() and etree.fromstring(zip.read('Content.xml')).tag in ('{http://openoffice.org/2000/office}bitmap-table','{http://openoffice.org/2004/office}bitmap-table'):
				return True
			else:
				return False
		except BadZipfile:
			return False

	@staticmethod
	def read(swatchbook,uri):
		zip = ZipFile(uri)
		xml = etree.fromstring(zip.read('Content.xml'))
		for zipped in zip.namelist():
			if "Pictures/" in zipped and zipped != "Pictures/":
				zip.extract(zipped,swatchbook.tmpdir)
		os.rename(os.path.join(swatchbook.tmpdir,"Pictures/"),os.path.join(swatchbook.tmpdir,"patterns/"))
		if xml.tag == '{http://openoffice.org/2000/office}bitmap-table': # OOo 2
			draw = '{http://openoffice.org/2000/drawing}'
		elif xml.tag == '{http://openoffice.org/2004/office}bitmap-table': # OOo 3
			draw = '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}'
		for elem in xml:
			id = False
			if elem.tag == draw+'fill-image':
				item = Pattern(swatchbook)
				if draw+'name' in elem.attrib:
					item.info.title = xmlunescape(unicode(elem.attrib[draw+'name']))
				if '{http://www.w3.org/1999/xlink}href' in elem.attrib:
					id = item.info.identifier = elem.attrib['{http://www.w3.org/1999/xlink}href'].replace("Pictures/","")
				if id in swatchbook.materials:
					swatchbook.book.items.append(Swatch(id))
					continue
				swatchbook.materials[id] = item
				swatchbook.book.items.append(Swatch(id))
