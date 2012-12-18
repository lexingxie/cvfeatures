import os
import re

img_ext = re.compile("jpg$|jpeg$|png$|bmp$|gif$|tif$|tiff$|ppm$|pgm$")
vid_ext = re.compile("flv$|webv$|wmv$|avi$|mp4$")

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