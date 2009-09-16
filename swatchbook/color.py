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
from lcms import *
from icc import *
import os.path

def unicc(values): # meant to disappear - used in the ASE and Scribus codecs
	for val in values:
		if isinstance(val,tuple):
			values[val[0]] = values[val]
			del values[val]
	return values

def toRGB(model,values,prof_in=False,prof_out=False):
	if prof_in:
		icc_in = ICCprofile(prof_in)
#		if icc_in.info['space'] == model:
		
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
	elif model == 'Lab':
		L,a,b = values
		R,G,B = Lab2RGB(L,a,b,prof_out)
	elif model == 'CMYK':
		C,M,Y,K = values
		R,G,B = CMYK2RGB(C,M,Y,K,prof_in,prof_out)
	elif model == 'GRAY':
		R = G = B = 1-values[0]
	else:
		return False
	return (R,G,B)


def Lab2RGB(L,a,b,prof_out=False):

	Lab = cmsCIELab(L,a,b)
	RGB = COLORW()
	
	hLab    = cmsCreateLabProfile(None)
	if prof_out:
		hRGB = cmsOpenProfileFromFile(prof_out,'r')
	else:
		hRGB = cmsCreate_sRGBProfile()

	xform = cmsCreateTransform(hLab, TYPE_Lab_DBL, hRGB, TYPE_RGB_16, INTENT_PERCEPTUAL, cmsFLAGS_NOTPRECALC)

	cmsDoTransform(xform, Lab, RGB, 1)

	cmsDeleteTransform(xform)
	cmsCloseProfile(hRGB)
	cmsCloseProfile(hLab)

	return (RGB[0]/0xFFFF,RGB[1]/0xFFFF,RGB[2]/0xFFFF)

def XYZ2RGB(X,Y,Z,prof_out=False):

	XYZ = cmsCIEXYZ(X/100,Y/100,Z/100)
	RGB = COLORW()
	
	hXYZ    = cmsCreateXYZProfile()
	if prof_out:
		hRGB = cmsOpenProfileFromFile(prof_out,'r')
	else:
		hRGB = cmsCreate_sRGBProfile()

	xform = cmsCreateTransform(hXYZ, TYPE_XYZ_DBL, hRGB, TYPE_RGB_16, INTENT_PERCEPTUAL, cmsFLAGS_NOTPRECALC)

	cmsDoTransform(xform, XYZ, RGB, 1)

	cmsDeleteTransform(xform)
	cmsCloseProfile(hRGB)
	cmsCloseProfile(hXYZ)

	return (RGB[0]/0xFFFF,RGB[1]/0xFFFF,RGB[2]/0xFFFF)

def CMYK2RGB(C,M,Y,K,prof_in=False,prof_out=False):
	
	CMYK = COLORW()
	RGB = COLORW()
	
	CMYK[0] = int(C*0xFFFF)
	CMYK[1] = int(M*0xFFFF)
	CMYK[2] = int(Y*0xFFFF)
	CMYK[3] = int(K*0xFFFF)

	if prof_out:
		hRGB = cmsOpenProfileFromFile(prof_out,'r')
	else:
		hRGB = cmsCreate_sRGBProfile()
	if prof_in:
		hCMYK = cmsOpenProfileFromFile(prof_in,'r')
	else:
		hCMYK = cmsOpenProfileFromFile((os.path.dirname(__file__) or ".")+"/Fogra27L.icm",'r')

	xform = cmsCreateTransform(hCMYK, TYPE_CMYK_16, hRGB, TYPE_RGB_16, INTENT_PERCEPTUAL, cmsFLAGS_NOTPRECALC)

	cmsDoTransform(xform, CMYK, RGB, 1)

	cmsDeleteTransform(xform)
	cmsCloseProfile(hRGB)
	cmsCloseProfile(hCMYK)

	return (RGB[0]/0xFFFF,RGB[1]/0xFFFF,RGB[2]/0xFFFF)

def RGB2RGB(RR,GG,BB,prof_in=False,prof_out=False):
	
	RRGGBB = COLORW()
	RGB = COLORW()
	
	RRGGBB[0] = int(RR*0xFFFF)
	RRGGBB[1] = int(GG*0xFFFF)
	RRGGBB[2] = int(BB*0xFFFF)

	if prof_out:
		hRGB = cmsOpenProfileFromFile(prof_out,'r')
	else:
		hRGB = cmsCreate_sRGBProfile()
	if prof_in:
		hRRGGBB = cmsOpenProfileFromFile(prof_in,'r')
	else:
		hRRGGBB = cmsCreate_sRGBProfile()

	xform = cmsCreateTransform(hRRGGBB, TYPE_RGB_16, hRGB, TYPE_RGB_16, INTENT_PERCEPTUAL, cmsFLAGS_NOTPRECALC)

	cmsDoTransform(xform, RRGGBB, RGB, 1)

	cmsDeleteTransform(xform)
	cmsCloseProfile(hRGB)
	cmsCloseProfile(hRRGGBB)

	return (RGB[0]/0xFFFF,RGB[1]/0xFFFF,RGB[2]/0xFFFF)

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
