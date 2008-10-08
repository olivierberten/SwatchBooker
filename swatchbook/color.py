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

def hex2(val):
	return hex(int(round(val)))[2:].rjust(2,'0')

def unicc(values):
	for val in values:
		if isinstance(val,tuple):
			values[val[0]] = values[val]
			del values[val]
	return values

def Lab2RGB(L,a,b):

	Lab = cmsCIELab(L,a,b)
	RGB = COLORW()
	
	hLab    = cmsCreateLabProfile(None)
	hsRGB   = cmsCreate_sRGBProfile()

	xform = cmsCreateTransform(hLab, TYPE_Lab_DBL, hsRGB, TYPE_RGB_16, INTENT_PERCEPTUAL, cmsFLAGS_NOTPRECALC)

	cmsDoTransform(xform, Lab, RGB, 1)

	cmsDeleteTransform(xform)
	cmsCloseProfile(hsRGB)
	cmsCloseProfile(hLab)

	return (RGB[0]/65535,RGB[1]/65535,RGB[2]/65535)

def XYZ2RGB(X,Y,Z):

	XYZ = cmsCIEXYZ(X/100,Y/100,Z/100)
	RGB = COLORW()
	
	hXYZ    = cmsCreateXYZProfile()
	hsRGB   = cmsCreate_sRGBProfile()

	xform = cmsCreateTransform(hXYZ, TYPE_XYZ_DBL, hsRGB, TYPE_RGB_16, INTENT_PERCEPTUAL, cmsFLAGS_NOTPRECALC)

	cmsDoTransform(xform, XYZ, RGB, 1)

	cmsDeleteTransform(xform)
	cmsCloseProfile(hsRGB)
	cmsCloseProfile(hXYZ)

	return (RGB[0]/65535,RGB[1]/65535,RGB[2]/65535)

#
# color model conversion formulas: http://www.easyrgb.com/math.php
#

# Observer= 2°, Illuminant= D65
ref_X =  95.047
ref_Y = 100.000
ref_Z = 108.883

def XYZ2Lab(X,Y,Z):
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

def CMYK2CMY(C,M,Y,K):
	C = ( C * ( 1 - K ) + K )
	M = ( M * ( 1 - K ) + K )
	Y = ( Y * ( 1 - K ) + K )

	return (C,M,Y)

def CMYK2RGB(C,M,Y,K):
	C,M,Y = CMYK2CMY(C,M,Y,K)
	return CMY2RGB(C,M,Y)
