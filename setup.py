#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup
from distutils import cmd
from distutils.command.install_data import install_data as _install_data
from distutils.command.build import build as _build

import msgfmt
import os

class build_trans(cmd.Command):
    description = 'Compile .po files into .mo files'
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        po_dir = os.path.join(os.path.dirname(os.curdir), 'translations')
        for path, names, filenames in os.walk(po_dir):
            for f in filenames:
                if f.endswith('.po'):
                    lang = f[:len(f) - 3]
                    src = os.path.join(path, f)
                    dest_path = os.path.join('build', 'locale', lang, 'LC_MESSAGES')
                    dest = os.path.join(dest_path, 'swatchbooker.mo')
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    if not os.path.exists(dest):
                        print 'Compiling %s' % src
                        msgfmt.make(src, dest)
                    else:
                        src_mtime = os.stat(src)[8]
                        dest_mtime = os.stat(dest)[8]
                        if src_mtime > dest_mtime:
                            print 'Compiling %s' % src
                            msgfmt.make(src, dest)

class build(_build):
    sub_commands = _build.sub_commands + [('build_trans', None)]
    def run(self):
        _build.run(self)

class install_data(_install_data):

    def run(self):
        for lang in os.listdir('build/locale/'):
            lang_dir = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
            lang_file = os.path.join('build', 'locale', lang, 'LC_MESSAGES', 'swatchbooker.mo')
            self.data_files.append( (lang_dir, [lang_file]) )
        _install_data.run(self)

cmdclass = {
    'build': build,
    'build_trans': build_trans,
    'install_data': install_data,
}

setup(name='SwatchBooker',
      version='0.7.2',
	  description='Swatch edition and conversion utilities',
	  long_description='SwatchBooker is a swatch book editor and convertor. It includes SwatchBooker Batch Convertor.\n\nThis package provides the `swatchbook` python package.\n\nMore informations at http://www.selapa.net/swatchbooker/',
	  author='Olivier Berten',
	  author_email='olivier.berten@gmail.com',
	  url='http://www.selapa.net/swatchbooker/',
	  license='GPL v3 or later',
      packages=['swatchbook',
                'swatchbook.codecs',
                'swatchbook.websvc'],
      package_dir={'':'src'},
      package_data={'swatchbook': ['Fogra27L.icm'],
                    'swatchbook.websvc': ['*.png']},
      data_files=[('share/applications', ['data/swatchbooker.desktop','data/sbconvertor.desktop']),
                  ('share/icons', ['data/swatchbooker.svg','data/swatchbooker.ico']),
				  ('lib/swatchbooker', ['src/swatchbooker.pyw', 'src/sbconvertor.pyw','src/sbconvert.py','src/sbcommon.py']),
				  ('bin',['data/swatchbooker', 'data/sbconvertor','data/sbconvert'])],
      scripts=['swatchbooker_w32_postinst.py'],
      cmdclass=cmdclass
      )
