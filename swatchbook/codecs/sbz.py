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

from swatchbook.codecs import *
import tempfile

class sbz(Codec):
	"""SwatchBooker"""
	ext = ('sbz',)
	@staticmethod
	def test(file):
		try:
			zip = ZipFile(file)
			if 'swatchbook.xml' in zip.namelist():
				return True
			else:
				return False
		except BadZipfile:
			return False

	@staticmethod
	def read(book,uri):
		zip = ZipFile(uri)
		xml = etree.fromstring(zip.read('swatchbook.xml'))
		for zipped in zip.namelist():
			if "profiles/" in zipped and zipped != "profiles/":
				uri = tempfile.mkstemp()[1]
				f = open(uri,'wb')
				f.write(zip.read(zipped))
				f.close()
				book.profiles[zipped[9:]] = ICCprofile(uri)
		for elem in xml:
			if elem.tag in ('group','color','spacer','break'):
				sbz.readitem(book,elem,book)
			elif elem.tag == 'info':
				if elem.attrib['type'] in ('version'):
					book.info['version'] = elem.text
				else:
					if elem.attrib['type'] not in book.info:
						book.info[elem.attrib['type']] = {}
					if 'lang' in elem.attrib:
						book.info[elem.attrib['type']][elem.attrib['lang']] = elem.text
					else:
						book.info[elem.attrib['type']][0] = elem.text
			elif elem.tag == 'display':
				book.display[elem.attrib['type']] = int(elem.text)

	@staticmethod
	def readitem(parent,item,book):
		if item.tag == 'group':
			bitem = Group()
			id = item.attrib['id']
			for elem in item:
				if elem.tag in ('group','color','spacer','break'):
					sbz.readitem(bitem,elem,book)
				elif elem.tag == 'info':
					if elem.attrib['type'] not in bitem.info:
						bitem.info[elem.attrib['type']] = {}
					if 'lang' in elem.attrib:
						bitem.info[elem.attrib['type']][elem.attrib['lang']] = elem.text
					else:
						bitem.info[elem.attrib['type']][0] = elem.text
		elif item.tag == 'color':
			bitem = Color(book)
			if 'spot' in item.attrib and item.attrib['spot'] == '1':
				bitem.attr.append('spot')
			id = item.attrib['id']
			for elem in item:
				if elem.tag == 'values':
					values = map(eval,elem.text.split())
					if 'space' in elem.attrib:
						bitem.values[(elem.attrib['model'],elem.attrib['space'])] = values
					else:
						bitem.values[(elem.attrib['model'],False)] = values
				elif elem.tag == 'info':
					if elem.attrib['type'] not in bitem.info:
						bitem.info[elem.attrib['type']] = {}
					if 'lang' in elem.attrib:
						bitem.info[elem.attrib['type']][elem.attrib['lang']] = elem.text
					else:
						bitem.info[elem.attrib['type']][0] = elem.text
				elif elem.tag == 'extra':
					bitem.extra[elem.attrib['type']] = elem.text
		elif item.tag == 'spacer':
			bitem = Spacer()
		elif item.tag == 'break':
			bitem = Break()
		if isinstance(bitem,Spacer) or isinstance(bitem,Break):
			id = str(bitem)
		parent.items[id] = bitem
		book.ids[id] = (bitem,parent)

	@staticmethod
	def write(book):
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n<SwatchBook version="0.2">\n'
		for info in book.info:
			if isinstance(book.info[info],dict):
				for lang in book.info[info]:
					if book.info[info][lang]:
						if lang == 0:
							xml += '  <info type="'+info+'">'+xmlescape(book.info[info][0])+'</info>\n'
						else:
							xml += '  <info type="'+info+'" lang="'+lang+'">'+xmlescape(book.info[info][lang])+'</info>\n'
			else:
				if book.info[info]:
					xml += '  <info type="'+info+'">'+xmlescape(book.info[info])+'</info>\n'
		for display in book.display:
			if book.display[display]:
				xml += '  <display type="'+display+'">'+str(book.display[display])+'</display>\n'
		xml += unicode(sbz.writem(book.items,0),'utf-8')
		xml += '</SwatchBook>\n'
		
		tf = open(tempfile.mkstemp()[1],"w+b")
		zip = ZipFile(tf,'w',ZIP_DEFLATED)
		zip.writestr('swatchbook.xml',xml.encode('utf-8'))
		for profile in book.profiles:
			#TODO: check if exists
			zip.write(book.profiles[profile].uri,'profiles/'+profile)
		zip.close()
		tf.seek(0)
		return tf.read()

	@staticmethod
	def writem(items,offset):
		xml = u''
		for id,item in items.items():
			if isinstance(item,Group):
				xml += '  '*(offset+1)+'<group id="'+id+'">\n'
			elif isinstance(item,Color):
				xml += '  '*(offset+1)+'<color id="'+id+'"'
				if 'spot' in item.attr:
					xml += ' spot="1"'
				xml += '>\n'
			if isinstance(item,Spacer):
				xml += '  '*(offset+1)+'<spacer />\n'
			elif isinstance(item,Break):
				xml += '  '*(offset+1)+'<break />\n'
			else:
				for info in item.info:
					if isinstance(item.info[info],dict):
						for lang in item.info[info]:
							if item.info[info][lang]:
								if lang == 0:
									xml += '  '*(offset+2)+'<info type="'+info+'">'+xmlescape(item.info[info][0])+'</info>\n'
								else:
									xml += '  '*(offset+2)+'<info type="'+info+'" lang="'+lang+'">'+xmlescape(item.info[info][lang])+'</info>\n'
					else:
						if item.info[info]:
							xml += '  '*(offset+2)+'<info type="'+info+'">'+xmlescape(item.info[info])+'</info>\n'
			if isinstance(item,Group):
				xml += sbz.writem(item.items,offset+1)
				xml += '  '*(offset+1)+'</group>\n'
			elif isinstance(item,Color):
				for value in item.values:
					xml += '  '*(offset+2)+'<values model="'+value[0]+'"'
					if value[1]:
						xml += ' space="'+value[1]+'"'
					xml += '>'+' '.join(str(round(x,16)) for x in item.values[value])+'</values>\n'
				for extra in item.extra:
					xml += '  '*(offset+2)+'<extra type="'+xmlescape(extra)+'">'
					if item.extra[extra]:
						xml += xmlescape(unicode(item.extra[extra]))
					xml += '</extra>\n'
				xml += '  '*(offset+1)+'</color>\n'

		return xml.encode('utf-8')
				
