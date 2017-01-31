#!/usr/bin/env python
# coding: utf-8

from swatchbook import *
import swatchbook.codecs as codecs
import swatchbook.websvc as websvc
from optparse import OptionParser

__version__ = "0.5"

parser = OptionParser(usage="usage: %prog -o output [-i input -d dir] file1 file2 ...\n   or  %prog -w websvc -o output [-d dir] palette1 palette2 ...\n Help: %prog -h", version="%prog "+__version__)
parser.add_option("-i", "--input", help="input format: "+", ".join(codecs.reads))
parser.add_option("-w", "--websvc", help="web service: "+", ".join(websvc.members.keys()))
parser.add_option("-o", "--output", help="output format: "+", ".join(codecs.writes))
parser.add_option("-d", "--dir", help="output directory")

(options, args) = parser.parse_args()

if not options.output:
	parser.error("Output format is mandatory")
if options.output and options.output not in codecs.writes:
	parser.error("Wrong output format. Should be one of these: "+", ".join(codecs.writes))
if options.input and options.input not in codecs.reads:
	parser.error("Wrong input format. Should be one of these: "+", ".join(codecs.reads))
if options.websvc and options.websvc not in websvc.list:
	parser.error("Wrong web service. Should be one of these: "+", ".join(websvc.members.keys()))
if len(args) == 0:
	parser.error("No file to convert")

for file in args:
	skip = False
	try:
		print "Converting "+file
		if options.websvc:
			sb = SwatchBook(websvc=options.websvc,webid=file)
		else:
			sb = SwatchBook(file,options.input)
	except FileFormatError:
		sys.stderr.write(file+": unknown file format\n")
	except (IndexError,ValueError):
		sys.stderr.write(file+": invalid palette id\n")
	else:
		filename =  os.path.splitext(os.path.basename(file))[0]
		dir = options.dir or ""
		fileout = os.path.join(dir,filename)+"."+eval('codecs.'+options.output).ext[0]
		while os.path.exists(fileout):
			wtd = raw_input(fileout+" exists. [O]verwrite, [S]kip or [R]ename? ")
			if wtd.lower() == "o":
				break
			elif wtd.lower() == "r":
				fileout = raw_input("New file name: ")
				if dir not in fileout:
					fileout = os.path.join(dir,fileout)
			elif wtd.lower() == "s":
				skip = True
				break
		if not skip:
			try:
				sb.write(options.output,fileout)
			except IOError,e:
				parser.error(e)
