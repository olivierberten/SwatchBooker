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
from datetime import *

dc = "http://purl.org/dc/elements/1.1/"
dcterms = "http://purl.org/dc/terms/"
rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xml = "http://www.w3.org/XML/1998/namespace"

class sbz(SBCodec):
	"""SwatchBooker"""
	ext = ('sbz',)
	@staticmethod
	def test(file):
		try:
			zip = ZipFile(file)
			if 'swatchbook.xml' in zip.namelist() and etree.fromstring(zip.read('swatchbook.xml')).tag == 'SwatchBook':
				return True
			else:
				return False
		except BadZipfile:
			return False

	@staticmethod
	def read(swatchbook,uri):
		zip = ZipFile(uri)
		xml = etree.fromstring(zip.read('swatchbook.xml'))
		for zipped in zip.namelist():
			if "profiles/" in zipped and zipped != "profiles/":
				uri = tempfile.mkstemp()[1]
				f = open(uri,'wb')
				f.write(zip.read(zipped))
				f.close()
				swatchbook.profiles[zipped[9:]] = ICCprofile(uri)
			if "patterns/" in zipped and zipped != "patterns/":
				zip.extract(zipped,swatchbook.tmpdir)
		if xml.attrib['version'] == '0.7':
			for elem in xml:
				if elem.tag == 'metadata':
					sbz.readmeta(swatchbook,elem)
				elif elem.tag == 'materials':
					for material in elem:
						sbz.readmaterial(material,swatchbook)
				elif elem.tag == 'book':
					for attrib in elem.attrib:
						if attrib in('columns','rows'):
							swatchbook.book.display[attrib] = int(elem.attrib[attrib])
						else:
							swatchbook.book.display[attrib] = elem.attrib[attrib]
					for item in elem:
						sbz.readitem(item,swatchbook.book)

	@staticmethod
	def readmeta(item,meta):
		for elem in meta:
			if elem.tag.find(dc):
				if elem.tag == '{'+dc+'}date':
					try:
						item.info.date = datetime.strptime(elem.text,"%Y-%m-%dT%H:%M:%S.%f")
					except ValueError, e:
						if str(e) == "'f' is a bad directive in format '%Y-%m-%dT%H:%M:%S.%f'": # Python 2.5
							item.info.date = datetime.strptime(elem.text.split('.')[0],"%Y-%m-%dT%H:%M:%S")
						else:
							remain = str(e)[26:]
							if remain == 'Z':
								item.info.date = datetime.strptime(elem.text[:-len(remain)],"%Y-%m-%dT%H:%M:%S.%f")
							else:
								date = datetime.strptime(elem.text[:-len(remain)],"%Y-%m-%dT%H:%M:%S.%f")
								delta = remain.split(':')
								item.info.date = date - timedelta(hours=int(delta[0]),minutes=int(delta[1]))
				elif elem.tag == '{'+dc+'}type':
					if elem.attrib['{'+rdf+'}resource'] != 'http://purl.org/dc/dcmitype/Dataset':
						raise FileFormatError
				elif elem.tag == '{'+dc+'}format':
					if elem.text != 'application/swatchbook':
						raise FileFormatError
				elif '{'+xml+'}lang' in elem.attrib:
					exec("item.info."+elem.tag[(len(dc)+2):]+"_l10n[elem.attrib['{'+xml+'}lang']] = xmlunescape(elem.text)")
				elif elem.tag == '{'+dcterms+'}license':
					item.info.license = xmlunescape(elem.attrib['{'+rdf+'}resource'])
				else:
					exec("item.info."+elem.tag[(len(dc)+2):]+" = xmlunescape(elem.text)")
			

	@staticmethod
	def readmaterial(material,swatchbook):
		if material.tag == 'color':
			sitem = Color(swatchbook)
			if 'usage' in material.attrib:
				sitem.usage = material.attrib['usage'].split(',')
		elif material.tag == 'pattern':
			sitem = Pattern(swatchbook)
			for elem in material:
				if elem.tag == 'values':
					values = map(eval,elem.text.split())
					if 'space' in elem.attrib:
						sitem.values[(elem.attrib['model'],unicode(elem.attrib['space']))] = values
					else:
						sitem.values[(elem.attrib['model'],False)] = values
				elif elem.tag == 'metadata':
					sbz.readmeta(sitem,elem)
				elif elem.tag == 'extra':
					sitem.extra[xmlunescape(elem.attrib['type'])] = xmlunescape(elem.text)
			if sitem.info.identifier > '':
				id = sitem.info.identifier
			else:
				raise FileFormatError
		swatchbook.materials[id] = sitem

	@staticmethod
	def readitem(item,parent):
		if item.tag == 'group':
			bitem = Group()
			for elem in item:
				if elem.tag == 'metadata':
					sbz.readmeta(bitem,elem)
				else:
					sbz.readitem(elem,bitem)
		elif item.tag == 'swatch':
			bitem = Swatch(item.attrib['material'])
		elif item.tag == 'spacer':
			bitem = Spacer()
		elif item.tag == 'break':
			bitem = Break()
		parent.items.append(bitem)

	@staticmethod
	def write(swatchbook):
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n<SwatchBook version="0.7"\n    xmlns:dc="'+dc+'"\n    xmlns:dcterms="'+dcterms+'"\n    xmlns:rdf="'+rdf+'">\n'
		xml += sbz.writemeta(swatchbook.info)
		xml += '  <materials>\n'
		for id in swatchbook.materials:
				material = swatchbook.materials[id]
			if isinstance(swatchbook.materials[id], Color):
				xml += '    <color'
				if len(material.usage) > 0:
					xml += ' usage="'+(','.join(material.usage))+'"'
				xml += '>\n'
				xml += sbz.writemeta(material.info,2)
				for value in material.values:
					xml += '      <values model="'+value[0]+'"'
					if value[1]:
						xml += ' space="'+value[1]+'"'
					xml += '>'+' '.join(str(round(x,16)) for x in material.values[value])+'</values>\n'
				for extra in material.extra:
					xml += '      <extra type="'+xmlescape(extra)+'">'
					if material.extra[extra]:
						xml += xmlescape(unicode(material.extra[extra]))
					xml += '</extra>\n'
				xml += '    </color>\n'
			elif isinstance(swatchbook.materials[id], Pattern):
				xml += '    <pattern>\n'
				xml += sbz.writemeta(material.info,2)
				for extra in material.extra:
					xml += '      <extra type="'+xmlescape(extra)+'">'
					if material.extra[extra]:
						xml += xmlescape(unicode(material.extra[extra]))
					xml += '</extra>\n'
				xml += '    </pattern>\n'
		xml += '  </materials>\n'
		if len(swatchbook.book.items) > 0:
			xml += '  <book'
			for display in swatchbook.book.display:
				if swatchbook.book.display[display]:
					xml += ' '+display+'="'+str(swatchbook.book.display[display])+'"'
			xml += '>\n'
			xml += unicode(sbz.writem(swatchbook.book.items),'utf-8')
			xml += '  </book>\n'
		xml += '</SwatchBook>\n'
		
		tf = open(tempfile.mkstemp()[1],"w+b")
		zip = ZipFile(tf,'w',ZIP_DEFLATED)
		zip.writestr('swatchbook.xml',xml.encode('utf-8'))
		for profile in swatchbook.profiles:
			zip.write(swatchbook.profiles[profile].uri,'profiles/'+profile)
		def addfiles(dir):
			for s in sorted(os.listdir(dir)):
				file = os.path.join(dir,s)
				if os.path.isdir(file) and file not in ('.','..'):
					addfiles(file)
				else:
					zip.write(file,file[len(swatchbook.tmpdir):])
		addfiles(swatchbook.tmpdir)
		zip.close()
		tf.seek(0)
		return tf.read()

	@staticmethod
	def writemeta(meta,offset=0):
		xml = u''
		if offset == 0:
			xml += '    <dc:format>application/swatchbook</dc:format>\n    <dc:type rdf:resource="http://purl.org/dc/dcmitype/Dataset" />\n'
		if meta.date:
			xml += '  '*(offset+2)+'<dc:date>'+meta.date.isoformat()+'Z</dc:date>\n'
		for dc in meta.dc:
			info = eval('meta.'+dc)
			if len(info) > 0:
				xml += '  '*(offset+2)+'<dc:'+dc+'>'+xmlescape(info)+'</dc:'+dc+'>\n'
			if meta.dc[dc][0]:
				info_l10n = eval('meta.'+dc+'_l10n')
				for lang in info_l10n:
					xml += '  '*(offset+2)+'<dc:'+dc+' xml:lang="'+lang+'">'+xmlescape(info_l10n[lang])+'</dc:'+dc+'>\n'
		if meta.license > '':
			xml += '  '*(offset+2)+'<dcterms:license rdf:resource="'+xmlescape(meta.license)+'" />\n'
		if xml > u'':
			return '  '*(offset+1)+'<metadata>\n'+xml+'  '*(offset+1)+'</metadata>\n'
		else:
			return u''

	@staticmethod
	def writem(items,offset=0):
		xml = u''
		for item in items:
			if isinstance(item,Group):
				xml += '  '*(offset+2)+'<group>\n'
				xml += sbz.writemeta(item.info,2)
				xml += sbz.writem(item.items,offset+1)
				xml += '  '*(offset+2)+'</group>\n'
			elif isinstance(item,Swatch):
				xml += '  '*(offset+2)+'<swatch material="'+item.material+'" />\n'
			elif isinstance(item,Spacer):
				xml += '  '*(offset+2)+'<spacer />\n'
			elif isinstance(item,Break):
				xml += '  '*(offset+2)+'<break />\n'
		return xml.encode('utf-8')
				
