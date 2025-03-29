#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  calibrate_camera_v2_2.py
#  29 03 2025
# THE PROGRAM IS PARAMETRIZED FOR 11X8 CHESSBOARD TEST PATTERNS 
# How to use the camera calibration script
# 1. Create directory for camera calibration
# 2. Put camera calibration script to calibration directory
# 3. Take 10 pictures with chessboard 11x8 (camera calibration files)
# 4. Put camera calibration files - to calibration directory 
# 5. Enter the calibration directory 
# 6. Run the camera calibration script with output to file results.txt as shown below
# 7. python calibrate_camera_v2.py > results.txt
# 8. See the camera calibration matrix and distortion coefficients in results.txt 
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

import numpy as np
import cv2 as cv
import glob
 
# sample image (chessboard) size
chessboardSize = (11, 8)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1,2)
 
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# Reference to calibration files
images = glob.glob('./*.jpg')

def main():

	for fname in images:
		print('fname', fname) 
		img = cv.imread(fname)
		gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
		
 
# Find the chess board corners
		ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)
 
# If found, add object points, image points (after refining them)
		if ret == True:
			objpoints.append(objp)
			print('ret true', fname)
			corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
			imgpoints.append(corners2)
 
# Draw and display the corners
		cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
		cv.imshow('img', img)
		cv.waitKey(500)
	
#  Run calibration
	ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
	
	print("Camera matrix : \n")
	print(mtx)
	print("distortion : \n")
	print(dist)

	
			
	return 0

if __name__ == '__main__':
		main()
