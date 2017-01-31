#!/usr/bin/env python
# coding: utf-8
#
#       Copyright 2008, 2017 Olivier Berten <olivier.berten@gmail.com>
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
from lcms2 import *
from icc import *
import os.path
import math

DblTriplet = c_double * 3
DblQuad = c_double * 4

def dirpath(name):
	if not name:
		return name
	elif os.path.islink(name):
		return os.path.dirname(os.path.abspath(os.path.realpath(name)))
	else:
		return os.path.dirname(name)

def toRGB(model,values,prof_in=False,prof_out=False):
	if model in ('RGB','HSV','HLS','CMY','YIQ'):
		if model == 'RGB':
			R,G,B = values
		elif model == 'HSV':
			H,S,V = values
			R,G,B = HSV2RGB(H,S,V)
		elif model == 'HLS':
			H,L,S = values
			R,G,B = HSL2RGB(H,S,L)
		elif model == 'CMY':
			C,M,Y = values
			R,G,B = CMY2RGB(C,M,Y)
		elif model == 'YIQ':
			Y,I,Q = values
			R,G,B = YIQ2RGB(Y,I,Q)
		R,G,B = RGB2RGB(R,G,B,prof_in,prof_out)
	elif model in ('sRGB', 'Lab', 'XYZ', 'CMYK'):
		R,G,B = lcms2RGB(model,values,prof_in,prof_out)
	elif model == 'LCH':
		R,G,B = lcms2RGB('Lab',LCH2Lab(*values),prof_in,prof_out)
	elif model == 'xyY':
		R,G,B = lcms2RGB('XYZ',xyY2XYZ(*values),prof_in,prof_out)
	elif model == 'GRAY':
		R = G = B = 1-values[0]
	else:
		return False
	return (R,G,B)

def lcms2RGB(model,values,prof_in=False,prof_out=False):
	context = cmsCreateContext(None, None)
	if model in ('RGB', 'sRGB') and prof_in == prof_out:
		return values

	t = {'RGB': TYPE_RGB_DBL,
	     'Lab': TYPE_Lab_DBL,
	     'XYZ': TYPE_XYZ_DBL,
	     'sRGB': TYPE_RGB_DBL,
	     'CMYK': TYPE_CMYK_DBL}

	if prof_in:
		inprof = cmsOpenProfileFromFileTHR(context, prof_in,'r')
	elif model == 'Lab':
		inprof = cmsCreateLab4ProfileTHR(context, None)
	elif model == 'XYZ':
		inprof = cmsCreateXYZProfileTHR(context)
	elif model == 'CMYK':
		inprof = cmsOpenProfileFromFileTHR(context, (dirpath(__file__) or ".")+"/Fogra27L.icm",'r')
	else:
		inprof = cmsCreate_sRGBProfileTHR(context)

	if prof_out:
		outprof = cmsOpenProfileFromFileTHR(context, prof_out,'r')
	else:
		outprof = cmsCreate_sRGBProfileTHR(context)

	if model in ('XYZ', ):
		inbuf = DblTriplet(*(v/100 for v in values))
	elif model in ('CMYK', ):
		inbuf = DblQuad(*(v*100 for v in values))
	else:
		inbuf = DblTriplet(*values)

	outbuf = DblTriplet()
	xform = cmsCreateTransformTHR(context, inprof, t[model], 
	                           outprof, t['RGB'],
	                           INTENT_PERCEPTUAL, 0)
	cmsCloseProfile(inprof)
	cmsCloseProfile(outprof)

	cmsDoTransform(xform, inbuf, outbuf, 1)
	cmsDeleteTransform(xform)

	return tuple(outbuf)

def RGB2RGB(RR,GG,BB,prof_in=False,prof_out=False):
	if prof_in == prof_out:
		return (RR,GG,BB)
	else:
		return lcms2RGB('RGB',(RR,GG,BB),prof_in,prof_out)

#
# color model conversion formulas: http://www.easyrgb.com/math.php
#

ref_XYZ = {'2°':{
'A':(109.850,100,35.585),
'C':(98.074,100,118.232),
'D50':(96.422,100,82.521),
'D55':(95.682,100,92.149),
'D65':(95.047,100,108.883),
'D75':(94.972,100,122.638),
'F2':(99.187,100,67.395),
'F7':(95.044,100,108.755),
'F11':(100.966,100,64.370)
}, '10°':{
'A':(111.144,100,35.200),
'C':(97.285,100,116.145),
'D50':(96.720,100,81.427),
'D55':(95.799,100,90.926),
'D65':(94.811,100,107.304),
'D75':(94.416,100,120.641),
'F2':(103.280,100,69.026),
'F7':(95.792,100,107.687),
'F11':(103.866,100,65.627)
}}

# Observer= 2°, Illuminant= D65
ref_X,ref_Y,ref_Z = ref_XYZ['2°']['D65']

def XYZ2Lab(X,Y,Z): # This formula is used in the ASE codec
	X = X / ref_X
	Y = Y / ref_Y
	Z = Z / ref_Z

	if X > 0.008856:
		X = X**(1/3)
	else:
		X = (7.787*X)+(16/116)
	if Y > 0.008856:
		Y = Y**(1/3)
	else:
		Y = (7.787*Y)+(16/116)
	if Z > 0.008856:
		Z = Z**(1/3)
	else:
		Z = (7.787*Z)+(16/116)

	L = (116*Y)-16
	a = 500*(X-Y)
	b = 200*(Y-Z)

	return (L,a,b)

def xyY2XYZ(x,y,Y):
	if y == 0: # trick for the Munsell full range palette
		y = 5e-324
	X = x * ( Y / y )
	Z = ( 1 - x - y ) * ( Y / y )

	return (X,Y,Z)

def LCH2Lab(L,C,H):
	a = math.cos(math.radians(H)) * C
	b = math.sin(math.radians(H)) * C

	return (L,a,b)

def Hue_2_RGB(v1,v2,vH):
	if ( vH < 0 ):
		vH = vH+1
	if ( vH > 1 ):
		vH = vH-1
	if ( ( 6 * vH ) < 1 ):
		return ( v1 + ( v2 - v1 ) * 6 * vH )
	if ( ( 2 * vH ) < 1 ):
		return ( v2 )
	if ( ( 3 * vH ) < 2 ):
		return ( v1 + ( v2 - v1 ) * ( ( 2 / 3 ) - vH ) * 6 )

	return ( v1 )

def HSV2RGB(H,S,V):
	if ( S == 0 ):
		R = V
		G = V
		B = V
	else:
		var_h = H * 6
		if ( var_h == 6 ):
			var_h = 0
		var_i = int( var_h )
		var_1 = V * ( 1 - S )
		var_2 = V * ( 1 - S * ( var_h - var_i ) )
		var_3 = V * ( 1 - S * ( 1 - ( var_h - var_i ) ) )

		if ( var_i == 0 ):
			R = V
			G = var_3
			B = var_1
		elif ( var_i == 1 ):
			R = var_2
			G = V
			B = var_1
		elif ( var_i == 2 ):
			R = var_1
			G = V
			B = var_3
		elif ( var_i == 3 ):
			R = var_1
			G = var_2
			B = V
		elif ( var_i == 4 ):
			R = var_3
			G = var_1
			B = V
		else:
			R = V
			G = var_1
			B = var_2

	return (R,G,B)

def HSL2RGB(H,S,L):
	if ( S == 0 ): 
		R = L 
		G = L
		B = L
	else:
		if ( L < 0.5 ):
			var_2 = L * ( 1 + S )
		else:
			var_2 = ( L + S ) - ( S * L )

		var_1 = 2 * L - var_2

		R = Hue_2_RGB( var_1, var_2, H + ( 1 / 3 ) )
		G = Hue_2_RGB( var_1, var_2, H )
		B = Hue_2_RGB( var_1, var_2, H - ( 1 / 3 ) )

	return (R,G,B)

def RGB2HSV(var_R,var_G,var_B):
	var_Min = min( var_R, var_G, var_B )    # Min. value of RGB
	var_Max = max( var_R, var_G, var_B )    # Max. value of RGB
	del_Max = var_Max - var_Min             # Delta RGB value 

	V = var_Max

	if del_Max == 0:                        # This is a gray, no chroma...
		H = 0                               # HSV results from 0 to 1
		S = 0
	else:                                   # Chromatic data...
		S = del_Max / var_Max

		del_R = ( ( ( var_Max - var_R ) / 6 ) + ( del_Max / 2 ) ) / del_Max
		del_G = ( ( ( var_Max - var_G ) / 6 ) + ( del_Max / 2 ) ) / del_Max
		del_B = ( ( ( var_Max - var_B ) / 6 ) + ( del_Max / 2 ) ) / del_Max

		if var_R == var_Max: H = del_B - del_G
		elif var_G == var_Max: H = ( 1 / 3 ) + del_R - del_B
		elif var_B == var_Max: H = ( 2 / 3 ) + del_G - del_R

		if H < 0: H += 1
		if H > 1: H -= 1

	return (H,S,V)

def RGB2HSL(var_R,var_G,var_B):
	var_Min = min( var_R, var_G, var_B )    # Min. value of RGB
	var_Max = max( var_R, var_G, var_B )    # Max. value of RGB
	del_Max = var_Max - var_Min             # Delta RGB value
	
	L = ( var_Max + var_Min ) / 2
	
	if del_Max == 0:                        # This is a gray, no chroma...
	   H = 0                                # HSL results from 0 to 1
	   S = 0
	else:                                   # Chromatic data...
		if L < 0.5: S = del_Max / ( var_Max + var_Min )
		else: S = del_Max / ( 2 - var_Max - var_Min )
		
		del_R = ( ( ( var_Max - var_R ) / 6 ) + ( del_Max / 2 ) ) / del_Max
		del_G = ( ( ( var_Max - var_G ) / 6 ) + ( del_Max / 2 ) ) / del_Max
		del_B = ( ( ( var_Max - var_B ) / 6 ) + ( del_Max / 2 ) ) / del_Max
		
		if var_R == var_Max: H = del_B - del_G
		elif var_G == var_Max: H = ( 1 / 3 ) + del_R - del_B
		elif var_B == var_Max: H = ( 2 / 3 ) + del_G - del_R
		
		if H < 0: H += 1
		if H > 1: H -= 1

	return H,S,L

def CMY2RGB(C,M,Y):
	R = ( 1 - C )
	G = ( 1 - M )
	B = ( 1 - Y )

	return (R,G,B)

# from http://en.wikipedia.org/wiki/YIQ
def YIQ2RGB(Y,I,Q):
	R = Y + 0.9563 * I + 0.6210 * Q
	G = Y - 0.2721 * I - 0.6474 * Q
	B = Y - 1.1070 * I + 1.7046 * Q
	return (R,G,B)

# from http://www.4p8.com/eric.brasseur/gamma.html
def sRGB_to_linear (s) :
	a = 0.055
	if s <= 0.04045 :
		return s / 12.92
	else :
		return ( (s+a) / (1+a) ) ** 2.4

def linear_to_sRGB (s) :
	a = 0.055
	if s <= 0.0031308 :
		return 12.92 * s
	else :
		return (1+a) * s**(1/2.4) - a
