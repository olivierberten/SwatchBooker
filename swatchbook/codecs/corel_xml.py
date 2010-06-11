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
import tempfile

class corel_xml(SBCodec):
	"""Corel X5"""
	ext = ('xml',)
	langcodes = {'EN': 'en',
				 'BR': 'pt',
				 'CS': 'zh-Hans',
				 'CT': 'zh-Hant',
				 'CZ': 'cs',
				 'DE': 'de',
				 'ES': 'es',
				 'FR': 'fr',
				 'IT': 'it',
				 'JP': 'ja',
				 'KR': 'ko',
				 'MA': 'hu',
				 'NL': 'nl',
				 'PL': 'pl',
				 'RU': 'ru',
				 'SU': 'fi',
				 'SV': 'sv',
				 'TR': 'tr'}
	@staticmethod
	def test(file):
		if etree.parse(file).getroot().tag == 'palette':
			return True
		else:
			return False

	@staticmethod
	def profile(fname):
		profile = False
		if os.path.isfile(fname):
			# the next 6 lines are a workaround for the unability of lcms to deal with unicode file names
			fi = open(fname, 'rb')
			uri = tempfile.mkstemp()[1]
			fo = open(uri,'wb')
			fo.write(fi.read())
			fi.close()
			fo.close()
			try:
				profile = icc.ICCprofile(uri)
			except BadICCprofile:
				pass
		return profile

	@staticmethod
	def read(swatchbook,file):
		dir = os.path.realpath(os.path.dirname(file)).split(os.sep)
		AdobeRGB = False
		HksRGB = False
		Hexachrome = False
		if 'Color' in dir:
			tmp = os.path.realpath(os.path.dirname(file)).split(os.sep+'Color'+os.sep)
			dirColor = tmp[0]+os.sep+'Color'+os.sep
			AdobeRGB = corel_xml.profile(dirColor+'AdobeRGB1998.icc')
			HksRGB = corel_xml.profile(dirColor+'HKS RGB.icc')
			Hexachrome = corel_xml.profile(dirColor+'Hexachrome.icc')
		xml = etree.parse(file).getroot()
		localization = xml.find('localization')
		l10n = {}
		if localization:
			for resource in localization.getchildren():
				l10n[resource.attrib['id']] = resource.getchildren()
		if 'name' in xml.attrib:
			swatchbook.info.title = xmlunescape(unicode(xml.attrib['name']))
		elif 'resid' in xml.attrib:
			swatchbook.info.title = xmlunescape(unicode(l10n[xml.attrib['resid']][0].text))
			for lang in l10n[xml.attrib['resid']]:
				swatchbook.info.title_l10n[corel_xml.langcodes[lang.tag]] = xmlunescape(unicode(lang.text))
		colorspaces = xml.find('colorspaces')
		if colorspaces:
			for cs in colorspaces.getchildren():
				if not (cs.attrib['name'].endswith(' (2)') and cs.attrib['name'][:-4] in swatchbook.materials):
					material = Color(swatchbook)
					material.info.identifier = cs.attrib['name']
					for color in cs.getchildren():
						space = color.attrib['cs']
						value = eval(color.attrib['tints'])
						if space == 'LAB':
							L,a,b = value
							material.values[('Lab',False)] = [L*100,a*255-128,b*255-128]
						elif space == 'CMYK':
							material.values[('CMYK',False)] = list(value)
						elif space == 'RGB':
							material.values[('RGB',False)] = list(value)
						elif space == 'sRGB':
							material.values[('sRGB',False)] = list(value)
						elif space == 'AdobeRGB':
							if AdobeRGB:
								if 'AdobeRGB1998.icc' not in swatchbook.profiles:
									swatchbook.profiles['AdobeRGB1998.icc'] = AdobeRGB
								material.values[('RGB','AdobeRGB1998.icc')] = list(value)
							else:
								material.values[('RGB',False)] = list(value)
						elif space == 'HksRGB':
							if HksRGB:
								if 'HKS RGB.icc' not in swatchbook.profiles:
									swatchbook.profiles['HKS RGB.icc'] = HksRGB
								material.values[('RGB','HKS RGB.icc')] = list(value)
							else:
								material.values[('RGB',False)] = list(value)
						elif space == 'Hexachrome':
							if Hexachrome:
								if 'Hexachrome.icc' not in swatchbook.profiles:
									swatchbook.profiles['Hexachrome.icc'] = Hexachrome
								material.values[('6CLR','Hexachrome.icc')] = list(value)
							else:
								material.values[('6CLR',False)] = list(value)
					if not 'process' in cs.attrib:
						material.usage.append('spot')
					swatchbook.materials[material.info.identifier] = material
		colors = xml.find('colors')
		if len(colors.getchildren()) > 1:
			for page in colors.getchildren():
				swatchbook.book.display['columns'] = max(swatchbook.book.display['columns'],len(list(page.getchildren())))
		elif 'width' in colors.find('page').attrib:
			swatchbook.book.display['columns'] = int(colors.find('page').attrib['width'])
		for page in colors.getchildren():
			for color in page.getchildren():
				cs = color.attrib['cs']
				if cs.endswith(' (2)') and cs[:-4] in swatchbook.materials:
					cs = cs[:-4]
				if cs in swatchbook.materials:
					swatchbook.book.items.append(Swatch(cs))
					if 'name' in color.attrib and color.attrib['name'] != cs:
						swatchbook.materials[cs].info.title = color.attrib['name']
				else:
					material = Color(swatchbook)
					value = eval(color.attrib['tints'])
					id = False
					if cs == 'LAB':
						L,a,b = value
						material.values[('Lab',False)] = [L*100,a*255-128,b*255-128]
					elif cs == 'CMYK':
						material.values[('CMYK',False)] = list(value)
					elif cs == 'RGB':
						material.values[('RGB',False)] = list(value)
					elif cs == 'Gray':
						material.values[('GRAY',False)] = 1-value
					if 'name' in color.attrib:
						id = color.attrib['name']
					elif 'resid' in color.attrib:
						material.info.title = xmlunescape(unicode(l10n[color.attrib['resid']][0].text))
						for lang in l10n[color.attrib['resid']]:
							material.info.title_l10n[corel_xml.langcodes[lang.tag]] = xmlunescape(unicode(lang.text))
						id = material.info.title
					if not id or id == '':
						id = str(material.values[material.values.keys()[0]])
					if id in swatchbook.materials:
						if material.values[material.values.keys()[0]] == swatchbook.materials[id].values[swatchbook.materials[id].values.keys()[0]]:
							swatchbook.book.items.append(Swatch(id))
							continue
						else:
							sys.stderr.write('duplicated id: '+id+'\n')
							material.info.title = id
							id = id+str(material.values[material.values.keys()[0]])
					material.info.identifier = id
					swatchbook.materials[id] = material
					swatchbook.book.items.append(Swatch(id))
			if len(colors.getchildren()) > 1 and len(page.getchildren()) < swatchbook.book.display['columns']:
				swatchbook.book.items.append(Break())
		if isinstance(swatchbook.book.items[-1],Break):
			del swatchbook.book.items[-1]
