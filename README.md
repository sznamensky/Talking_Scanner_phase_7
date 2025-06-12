# Talking_Scanner_phase_7
This is the repository for sw created by Sergei Znamensky for phase 7 of the Talking Scanner project 
Two scripts presented can be used to compensate camera distorsion.
In order to be able to compensate distorsion you first need to calibrate the camera being used.
Print the camera calibration pattern (Chessboard_12x8.png).
Create the new directory for camera calibration.
Take few test pattern pictures with your camera of the camera calibration pattern (examples here: scan*.jpg).
Create the camera calibration directory.
Copy the test pattern pictures to the calibration directory.
Copy the calibration script to the calibration directory (calibrate_camera_v2_2.py).
Enter the calibration directory and run the script (python calibrate_camera_2_2.py > results.txt).
See your camera calibration results in results.txt file.
Now enter the camera calibration results values (camera matrix and distorsion coef.) to the camera distorsion compensation script (you need to replace values in undistort_picture_v2_3.py).
Take some pictures with your camera and test the camera distorsion compensation script (python undistort_picture_v2_3.py <your picture name.jpg>). You get results in <your picture name>.png. (See some examples in Testimage.jpg Testimage_undistorted.png).
Added the program <takepic_undist_preproc_ocr_v1_2_L2.py> that takes left page scan with camera 2, undistorts scanned image, rotates image 90 degrees, saves scanned image to file, performs OCR, saves OCR results to text file.
