#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  takepic_undist_preproc_ocr_v1_1_L2.py
# 12 06 2025
# The program takes the scan image from the camera N 2  (left page)
# The program is using the camera calibration results obtained from calibrate_camera_v2_3.py script
# The program processes the scanned image to compensate for the camera N 2 distortion (left page) 
# The program rotates 90 degrees the scanned image
# The program performs OCR
# The program outputs the OCR results to the text file
# Command line: python takepic_undistort_preprocess_v1_0_L2.py 
# Output file names: <page_??>.jpg <page_??.txt>
# Output directory: script location 
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
import pytesseract
import os
from picamera2 import Picamera2, Preview 
from libcamera import controls			# added for camera mode controls
import time 
from time import sleep
import numpy as np
import cv2 as cv
import glob
import sys

# Define the camera calibration matrix (to be imported from the calibration script results)
camera_matrix = np.array([[1.68101687e+04,   0.00000000e+00, 1.35509275e+03],
       [  0.00000000e+00, 1.69201067e+04, 9.59995287e+02],
       [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
# Define the camera distortion coefficients (to be imported from the calibration script results)
dist_coefs = np. array([ -1.58612076e+01, 3.78786179e+02, 2.23227717e-02, -1.49957066e-02, 2.56512630e+03])

# Define scanned images names templates
img_prefix = "page_"
img_suffix = ".jpg"

# function takes picture 
def capture_image():
	picam2 = Picamera2()
	picam2.start_preview()
	time.sleep(2)
	config = picam2.create_still_configuration()
	picam2.configure(config)
	picam2.controls.ExposureTime = 10000	# set exposure time
	picam2.controls.AnalogueGain = 1.0			# set analogue gain
	picam2.controls.Sharpness = 1.0				# set sharpness from 0.0 to 16.0
	picam2.controls.Contrast = 1.0					# set contrast from 0.0 to 32.0
	picam2.controls.Brightness = 0.0				# set brightness from -1.0 to 1.0
	picam2.controls.Saturation = 1.0				# set saturation from 0.0 to 32.0
#	picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.0})		# set manual focus mode and lens position
#	picam2.controls.AfMode = Manual				# set manual focus mode 
#	picam2.controls.LensPosition = 0.0				# set lest position for manual focus
	picam2.start()
	image = picam2.capture_array()
	picam2.stop()
	return image

# function defines file names to save scanned file and OCR results text file
def next_filename(img_prefix, img_suffix):	
	"""Generates the next available filename in the path with a given prefix and suffix."""
	i = 1
	while os.path.exists(f"{img_prefix}{i}{img_suffix}"):
		i += 1
	return f"{img_prefix}{i}"

def main():
# load scan image from camera
	image = capture_image()
	img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
	h,  w = img.shape[:2]
	print('h w :', h, w)
	newcameramtx, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w,h), 1, (w,h))	
# undistort
	dst = cv.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)
# crop the image
	x, y, w, h = roi
	dst = dst[y:y+h, x:x+w]
# rotate the image 90 counterclockwise
	dstRotate90 = cv.rotate(dst, cv.ROTATE_90_COUNTERCLOCKWISE)

# Define names to save scanned image file and related OCR results file
	nextFileName = next_filename(img_prefix, img_suffix)
	nextImgFileName = f"{nextFileName}.jpg"
	nextTxtFileName = f"{nextFileName}.txt"
	
# Save scanned image to file
	cv.imwrite(nextImgFileName, dstRotate90)
	print('Scanned image saved to file name : ', nextImgFileName)

# Perform OCR for scanned image
	config = '--psm 6 -l rus'
	text = pytesseract.image_to_string(dstRotate90, config=config)

# Save OCR results to text file
	text_file = open(f"{nextTxtFileName}", "w")
	text_file.write(text)
	text_file.close()
	print('OCR results saved to file name : ', nextTxtFileName)

	return 0

if __name__ == '__main__':
	main()
