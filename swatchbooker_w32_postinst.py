#!/usr/bin/env python
# coding: utf-8

# Many thanks to Florian Birée for the tips about that file!
# http://filyb.info/post/2006/11/11/418-creer-un-installateur-windows-pour-un-programme-en-python-a-l-aide-des-distutils-a-l-usage-des-programmeurs-perdus-en-dehors-de-leur-systeme-familier

import os
import sys

if sys.argv[1] == '-install':
	python_path = sys.prefix
	pyw_path = os.path.abspath(os.path.join(python_path, 'pythonw.exe'))
	script_dir = os.path.abspath(os.path.join(python_path, 'lib', 'swatchbooker'))
	ico_path = os.path.join(os.path.join(python_path, 'share', 'icons', 'swatchbooker.ico'))
	swatchbooker_path = os.path.join(script_dir, 'swatchbooker.pyw')
	sbconvertor_path = os.path.join(script_dir, 'sbconvertor.pyw')

	try:
		start_path = get_special_folder_path("CSIDL_COMMON_PROGRAMS")
	except OSError:
		start_path = get_special_folder_path("CSIDL_PROGRAMS")
	programs_path = os.path.join(start_path, "SwatchBooker")

	try :
		os.mkdir(programs_path)
	except OSError:
	    pass
	directory_created(programs_path)

	create_shortcut(pyw_path,
	                "Swatch book editor",
	                os.path.join(programs_path, 'SwatchBooker Editor.lnk'),
	                swatchbooker_path,
	                script_dir,
	                ico_path
	                )
	file_created(os.path.join(programs_path, 'SwatchBooker Editor.lnk'))

	create_shortcut(pyw_path,
	                "Swatch book convertor",
	                os.path.join(programs_path, 'SwatchBooker Batch Convertor.lnk'),
	                sbconvertor_path,
	                script_dir,
	                ico_path
	                )
	file_created(os.path.join(programs_path, 'SwatchBooker Batch Convertor.lnk'))

	sys.exit()
