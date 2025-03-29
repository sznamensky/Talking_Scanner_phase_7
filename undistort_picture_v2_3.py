#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  undistort_picture_v2_3.py
# 27 03 2025
# The program is using the camera calibration results obtained from calibrate_camera_v2.py script
# The program processes the input image to compensate the camera distortion 
# Command line: python undistort_picture.py <distorted file name>.jpg
# Output file name: <distorted file name>.png
# Script to be executed from the catalog containing the distorted file
#  
#  Copyright 2025 Сергей Львович Знаменский <serzn@mail.ru>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import numpy as np
import cv2 as cv
import glob
import sys
import os
# Define the camera calibration matrix (to be imported from the calibration script results)
camera_matrix = np.array([[5.59371698e+03,   0.00000000e+00, 1.40224398e+03],
       [  0.00000000e+00, 5.61669456e+03, 9.52242052e+02],
       [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
# Define the camera distortion coefficients (to be imported from the calibration script results)
dist_coefs = np. array([ -1.67427332e+00, 6.31145307e+00, -1.44173455e-03, -1.75687244e-02, -3.24836339e+01])

# Define the location for input files
# images = glob.glob('*.jpg')
# Define variable to store the name of input name  from the command line
input_name = ""	
# Define variable to store the output file extension
extension_out = ".png"
# Define variable to store the name of the output file
output_filename = ""

def main():
# load picture from file
	input_filename = sys.argv[1]
	print('input_filename :', input_filename)
	img = cv.imread(input_filename)
	h,  w = img.shape[:2]
	print('h w :', h, w)
	newcameramtx, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w,h), 1, (w,h))	
# undistort
	dst = cv.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)
# crop the image
	x, y, w, h = roi
	dst = dst[y:y+h, x:x+w]
# define the name for the output file
	fname, extension_old = os.path.splitext(input_filename)
	output_filename = fname + extension_out
	print('Output file name :', output_filename)
# create the output file
	cv.imwrite(output_filename, dst)
	return 0

if __name__ == '__main__':
	main()
