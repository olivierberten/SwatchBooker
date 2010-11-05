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

class quark_qcl(SBCodec):
	"""QuarkXPress Color Library"""
	ext = ('qcl',)
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag == 'cgats17':
			return True
		else:
			return False

	@staticmethod
	def read(swatchbook,file):
		xml = etree.parse(file).getroot()
		swatchbook.info.title = xmlunescape(unicode(list(xml.getiterator('file_descriptor'))[0].text))
		swatchbook.info.rights = xmlunescape(unicode(list(xml.getiterator('originator'))[0].text))
		preferredmodel = list(xml.getiterator('default_color_space'))[0].text.strip()
		usage = list(xml.getiterator('color_usage_recommendation'))[0].text
		name_field_info = list(xml.getiterator('name_field_info'))
		if len(name_field_info) > 0:
			prefix = {}
			suffix = {}
			for name in name_field_info:
				nid = eval(name.attrib['format_id'])-1
				prefix[nid], suffix[nid] =  xmlunescape(unicode(name.attrib['long_form'])).split('%n')
		ui_spec =  os.path.dirname(file)+'/'+list(xml.getiterator('ui_spec'))[0].text
		breaks = []
		if os.path.isfile(ui_spec):
			ui = etree.parse(ui_spec).getroot()
			swatchbook.book.display['columns'] = eval(list(ui.getiterator('rows_per_page'))[0].text)
			breaks = list(ui.getiterator('column_break'))
			if len(breaks)>0:
				for i in range(len(breaks)):
					breaks[i] = eval(breaks[i].text)
		else:
			sys.stderr.write('ui file '+ui_spec+' doesn\'t exist\n')
		fields = xml.getiterator('field_info')
		data_format = {}
		for field in fields:
			data_format[field.attrib['name']] = field.attrib['pos']
		colors = xml.getiterator('tr')
		i = 0
		for color in colors:
			if i in breaks:
				swatchbook.book.items.append(Break())
			item = Color(swatchbook)
			id = xmlunescape(unicode(color.getchildren()[eval(data_format['SAMPLE_ID'])-1].text))
			if data_format.has_key('NAME_FORMAT_ID'):
				nid = eval(color.getchildren()[eval(data_format['NAME_FORMAT_ID'])-1].text)-1
				id = prefix[nid]+id+suffix[nid]
			if data_format.has_key('LAB_L'):
				item.values[('Lab',False)] = [eval(color.getchildren()[eval(data_format['LAB_L'])-1].text),\
											  eval(color.getchildren()[eval(data_format['LAB_A'])-1].text),\
											  eval(color.getchildren()[eval(data_format['LAB_B'])-1].text)]
			if data_format.has_key('RGB_R'):
				item.values[('RGB',False)] = [eval(color.getchildren()[eval(data_format['RGB_R'])-1].text)/0xFF,\
											  eval(color.getchildren()[eval(data_format['RGB_G'])-1].text)/0xFF,\
											  eval(color.getchildren()[eval(data_format['RGB_B'])-1].text)/0xFF]
			if data_format.has_key('CMYK_C'):
				item.values[('CMYK',False)] = [eval(color.getchildren()[eval(data_format['CMYK_C'])-1].text)/100,\
											   eval(color.getchildren()[eval(data_format['CMYK_M'])-1].text)/100,\
											   eval(color.getchildren()[eval(data_format['CMYK_Y'])-1].text)/100,\
											   eval(color.getchildren()[eval(data_format['CMYK_K'])-1].text)/100]
			if data_format.has_key('PC6_1'):
				item.values[('6CLR',False)] = [eval(color.getchildren()[eval(data_format['PC6_1'])-1].text)/100,\
											  eval(color.getchildren()[eval(data_format['PC6_2'])-1].text)/100,\
											  eval(color.getchildren()[eval(data_format['PC6_3'])-1].text)/100,\
											  eval(color.getchildren()[eval(data_format['PC6_4'])-1].text)/100,\
											  eval(color.getchildren()[eval(data_format['PC6_5'])-1].text)/100,\
											  eval(color.getchildren()[eval(data_format['PC6_6'])-1].text)/100]
			item.values.insert(0,(preferredmodel,False),item.values.pop((preferredmodel,False)))
			if usage in ('4','5'):
				item.usage.append('spot')
			if not id or id == '':
				id = idfromvals(item.values[item.values.keys()[0]])
			if id in swatchbook.materials:
				if item.values[item.values.keys()[0]] == swatchbook.materials[id].values[swatchbook.materials[id].values.keys()[0]]:
					swatchbook.book.items.append(Swatch(id))
					continue
				else:
					sys.stderr.write('duplicated id: '+id+'\n')
					item.info.title = id
					id = id+idfromvals(item.values[item.values.keys()[0]])
			item.info.identifier = id
			swatchbook.materials[id] = item
			swatchbook.book.items.append(Swatch(id))
			i += 1

