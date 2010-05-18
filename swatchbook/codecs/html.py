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

class html(SBCodec):
	"""HTML document"""
	ext = ('html','htm')
	@staticmethod
	def write(swatchbook):
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
	.group_title {
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
		if swatchbook.info.title > '':
			htm += '<p id="title">'+xmlescape(swatchbook.info.title)+'</p>\n'
		if swatchbook.info.description > '':
			htm += '<p id="description">'+xmlescape(swatchbook.info.description)+'</p>\n'
		if swatchbook.info.rights:
			htm += '<p id="rights">'+xmlescape(swatchbook.info.rights)+'</p>\n'
		if swatchbook.info.version > '':
			htm += '<p id="version">'+xmlescape(swatchbook.info.version)+'</p>\n'
		htm += '<div id="swatchbook"'
		if swatchbook.book.display['columns']:
			htm += ' style="width:'+str(swatchbook.book.display['columns']*30)+'px"'
		htm += '>\n'

		htm += html.writem(swatchbook,swatchbook.book.items)

		htm += '</div>\n</body>\n</html>'

		return htm.encode('utf-8')

	@staticmethod
	def writem(swatchbook,items):
		html_tmp = u''
		for item in items:
			if isinstance(item,Group):
				html_tmp += '<div class="group">\n'
				if item.info.title > '':
					html_tmp += '<div class="group_title">'+xmlescape(item.info.title)+'</div>\n'
				html_tmp += html.writem(swatchbook,item.items)
				if item.info.description > '':
					html_tmp += '<div class="group_descr">'+xmlescape(item.info.description)+'</div>\n'
				html_tmp += '</div>\n'
			elif isinstance(item,Swatch):
				item = swatchbook.swatches[item.id]
				if isinstance(item,Color):
					if len(item.values) > 0:
						R,G,B = item.toRGB8()
					else:
						R,G,B = [0,0,0]
					if item.info.title > '':
						title_txt = item.info.title
					else:
						title_txt = item.info.identifier
					html_tmp += '<div class="swatch" style="background-color:#'+hex2(R)+hex2(G)+hex2(B)+'" title="'+xmlescape(title_txt)+'"></div>\n'
			elif isinstance(item,Spacer):
				html_tmp += '<div class="swatch"></div>\n'
			elif isinstance(item,Break):
				html_tmp += '<br class="clearall" />\n'
		return html_tmp
