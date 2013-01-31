#============================================================================================
#				Preamble
#============================================================================================

import os
import re
import cv2
import cv2.cv as cv
import numpy as np
import itertools

#============================================================================================
#				Public Variable Def
#============================================================================================

img_ext = re.compile("jpg$|jpeg$|png$|bmp$|gif$|tif$|tiff$|ppm$|pgm$")
vid_ext = re.compile("flv$|webv$|wmv$|avi$|mp4$")

#============================================================================================
#				TypeFinding Functions
#============================================================================================

def is_image_file(in_str):
	if not os.path.isfile(in_str):
		is_img = False
	else:
		m = re.findall(img_ext, in_str.lower())
		if m:
			is_img = True
		else:
			is_img = False

	return is_img

def is_image_or_video(in_str):	
	if is_image_file(in_str):
		is_img_vid = True
	else:
		m = re.findall(vid_ext, in_str.lower())
		if m:
			is_img_vid = True
		else:
			is_img_vid = False

	return is_img_vid

#============================================================================================
#				Video Processing
#============================================================================================

# Takes in a video and an integer (rate), and returns a list of sample frames at the rate specified.
# Default rate of 5 frames per second.
def frame_reduction(in_file_name, fps = 5):
	vid_file = cv.CaptureFromFile(in_file_name)
	vid_frames = cv.GetCaptureProperty(vid_file,cv.CV_CAP_PROP_FRAME_COUNT)
	vid_fps = cv.GetCaptureProperty(vid_file,cv.CV_CAP_PROP_FPS)
	img_list = []
	for f in range(int(vid_frames)):
		if(f%(int(vid_frames/fps))==0):
			frameImg = cv.QueryFrame(vid_file)
			img_list.append(frameImg)
	return img_list

	#vid_file = cv2.VideoCapture(in_file_name)
	#vid_frames = vid_file.get(cv.CV_CAP_PROP_FRAME_COUNT)
	#vid_fps = vid_file.get(cv.CV_CAP_PROP_FPS)
	#img_list = []
	#for f in range(int(vid_frames)):
		#if(f%(int(vid_frames/fps))==0):
			#frame_img = vid_file.read()
			#img_list.append(frame_img)
	#return img_list
