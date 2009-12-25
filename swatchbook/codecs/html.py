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

		htm += html.writem(book.items)

		htm += '</div>\n</body>\n</html>'

		return htm.encode('utf-8')

	@staticmethod
	def writem(items,lang=0):
		html_tmp = u''
		for item in items.values():
			if isinstance(item,Group):
				html_tmp += '<div class="group"><div class="group_name">'+item.info['name'][0]+'</div>\n'
				html_tmp += html.writem(item.items)
				html_tmp += '\n<div class="group_descr">'
				if 'description'in item.info:
					html_tmp += item.info['description'][lang]
				html_tmp += '</div></div>\n'
			elif isinstance(item,Color):
				if len(item.values) > 0:
					R,G,B = item.toRGB8()
				else:
					R,G,B = [0,0,0]
				html_tmp += '<div class="swatch" style="background-color:#'+hex2(R)+hex2(G)+hex2(B)
				if 'name' in item.info:
					html_tmp += '" title="'+item.info['name'][lang]
				html_tmp += '"></div>\n'
			elif isinstance(item,Spacer):
				html_tmp += '<div class="swatch"></div>\n'
			elif isinstance(item,Break):
				html_tmp += '<br class="clearall" />\n'
		return html_tmp
				

