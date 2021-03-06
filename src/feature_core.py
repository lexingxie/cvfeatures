
#============================================================================================
#				Preamble
#============================================================================================

import cv2
import numpy as np
import itertools

#============================================================================================
#				Enclosing Functions
#============================================================================================

def update_results(out_json, cur_dict, in_file_name, verbose=0):
	if cur_dict:
		success = 1
		#out_json = dict(cur_dict.items() + out_json.items())
		if 'feature' not in out_json:
			out_json['feature'] = []
		out_json['feature'].append(cur_dict)
	else:
		success = 0
		if verbose:
			print(" empty output for image %s " % in_file_name)

	return success

def proc_one_file(in_file_name, args):
	if args.verbose>=2:
		print("processing file " + in_file_name)
	
	success = 0
	out_json = {'uri': in_file_name}

	img = cv2.imread(in_file_name)
	# pre-processing

	# extract features
	if "average_rgb" in args.feature_list:
		out_dict = average_rgb(img)
		success = update_results(out_json, out_dict, in_file_name, args.verbose)

	if "gray_histogram16" in args.feature_list:
		out_dict = gray_histogram(img, 16)
		success = update_results(out_json, out_dict, in_file_name, args.verbose)

	if "sift_points" in args.feature_list:
		out_dict = sift_points(img)
		success = update_results(out_json, out_dict, in_file_name, args.verbose)
	
	if "color_metric" in args.feature_list:
		 out_dict = color_metric(img)
		 success = update_results(out_json, out_dict, in_file_name, args.verbose)

	if "avg_luminecence" in args.feature_list:
		 out_dict = avg_luminecence(img)
		 success = update_results(out_json, out_dict, in_file_name, args.verbose)

	if "lighting_quality" in args.feature_list:
		 out_dict = lighting_quality(img)
		 success = update_results(out_json, out_dict, in_file_name, args.verbose)

	if "region_of_interest" in args.feature_list:
		 dst,out_dict = region_of_interest(img)
		 success = update_results(out_json, out_dict, in_file_name, args.verbose)

	if "clarity_contrast" in args.feature_list:
		 out_dict = clarity_contrast(img)
		 success = update_results(out_json, out_dict, in_file_name, args.verbose)

	if "color_harmony" in args.feature_list:
		 out_dict = color_harmony(img)
		 success = update_results(out_json, out_dict, in_file_name, args.verbose)

	if "alt_color_harmony" in args.feature_list:
		 out_dict = alt_color_harmony(img)
		 success = update_results(out_json, out_dict, in_file_name, args.verbose)

	if "composition_geometry" in args.feature_list:
		 out_dict = composition_geometry(img)
		 success = update_results(out_json, out_dict, in_file_name, args.verbose)

	if "simplicity" in args.feature_list:
		 out_dict = simplicity(img)
		 success = update_results(out_json, out_dict, in_file_name, args.verbose)

	return out_json, success

#============================================================================================
#				Image feature extractors
#============================================================================================
def gray_histogram(img, num_bins):
	try:
		img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		#rng = np.array([0, 256])
		#hist =  cv2.calcHist([img],[ch],None,[256],[0,255])
		hist,_binedges = np.histogram(img2, bins=num_bins, range=(0,255))
		out_dict ={ "name": "gray_histogram%d" % num_bins, 
			'value': list(hist) } 
	except:
		out_dict = {}
		raise
	return out_dict

def average_rgb(img):
	h = np.zeros([3])
	try:
		for i in range(3):
			h[i] = np.mean(img[:,:,i])
		out_dict ={ "name": "average_rgb", 
			"value" : list(h) }
	except:
		out_dict = {}
		raise
	return out_dict

def sift_points(img, num_det=500):
	img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	try:
		sift = cv2.FeatureDetector_create('SIFT')
		detector = cv2.GridAdaptedFeatureDetector(sift, num_det) # max number of features
		fs = detector.detect(img2)
		points = []
		for f in fs:
			#reference code sample at
	        # http://shambool.com/2012/04/15/sift-and-all-the-other-feature-detectors-in-python/
			points.append( {'position': f.pt, 'radius': f.size/2, 'angle': f.angle} )
		out_dict = {"name": "sift_points", "value" : points}
	except:
		out_dict = {}
		raise
	return out_dict

  # Reference: "Measuring Colorfulness in Natural Images" - Hassler and Sustrank
  # Using trignometric length of the stdv and mean Chroma.
  ## Measure not yet working, returning values higher than expected
def color_metric(img):
	img2 = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	try:
		 a_list = list(itertools.chain(*img2[:,:,1]))
		 b_list = list(itertools.chain(*img2[:,:,2]))
		 a_std = np.std(a_list)
		 b_std = np.std(b_list)
		 ab_std = np.sqrt(a_std*a_std + b_std*b_std)
		 chroma_mean = np.mean([np.sqrt(float(a)*float(a)+float(b)*float(b)) 
			for (a,b) in zip(a_list, b_list)])
		 value = ab_std + 0.94*chroma_mean
		 out_dict = {"name": "color_metric", "value" : value}
	except:
		 out_dict = {}
		 raise
	return out_dict

  # Luminecence measure.
def avg_luminecence(img):
	img2 = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	try:
		l_mean = np.mean(img2[:,:,0])
		out_dict = {"name": "avg_luminecence", "value" : l_mean}
	except:
		out_dict = {}
		raise
	return out_dict

  # Reference: "Photo and Video Qualtiy Evaluation: Focousing on the Subject" - Lou & Tang.
  # A measure of qulity of the lighting in an image.
  ## Method for excluding ROI and background may not work.
def lighting_quality(img):
	try:
		img2, out_dict = region_of_interest(img)
		img3 = cv2.GetSubRect(img,GetImageROI(img2))
		img4 = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)
		roi = cv2.cvtColor(img3, cv2.COLOR_BGR2LAB)
		background = cv2.Sub(img2,roi) # There may be an issue with the arrays not being of the same size.
		b_background = np.mean(background[:,:,0]) # Mean might not be completely correct, mean of an array with many 0s in it, which are counted in the mean.
		b_roi = np.mean(ROI[:,:,0])
		lighting_measure = abs(np.log(b_roi/b_background))
		out_dict = {"name" : "lighting_quality", "value" : lighting_measure}
	except:
		out_dict = {}
		raise
	return out_dict

  # Reference: "Photo and Video Qualtiy Evaluation: Focousing on the Subject" - Lou & Tang.
  # region of interest extraction via blur degree/focous.
  ## Still needs work
def region_of_interest(img,w_size=1,alpha=0.9):
	try:
		y = len(img)
		x = len(img[1])
		U_Mat = [[0]*y]*x
		k_max = 0.0
		for j in range(y):
			for i in range(x):
				for k in range(1,2):
					k_array = np.ones((k,k), dtype=np.int32)
					img2 = cv2.blur(img,(1,1))# Convolve image with a kernel deteminted by n.
					diffx_img = map(np.linalg.norm, cv2.Sobel(img2, cv2.CV_32F,1,0)) # Take derivatives of the smoothened image in the
					diffy_img = map(np.linalg.norm, cv2.Sobel(img2, cv2.CV_32F,0,1))
					histx,x_binedges = np.histogram(diffx_img, bins=10, range=(0,10000))
					histy,y_binedges = np.histogram(diffy_img, bins=10, range=(0,10000))
					print(diffx_img)
					w_sum = 0
					for j_w in range(i-w_size,i+w_size): # Loop through the image.
						for i_w  in range(j-w_size,j+w_size+1):
							try:
								w_sum +=1
								#w_sum += np.log(list(histx)[int(np.digitize(diffx_img[i_w,j_w],x_binedges))]) + np.log(list(histy)[int(np.digitize(diffy_img[i_w,j_w],y_binedges))])
							except:
								raise
								continue
					if(w_sum > k_max):
						k_max = w_sum
				if k_max == 1:
					U_Mat[i,j] = 1 # Build binary image.
		U_Mat_x = [sum(y) for y in zip(*U_Mat)]
		U_Mat_y = [sum(x) for x in U_Mat]
		xenergy_bound = (1-alpha)*np.linalg.norm(U_Mat_x)/2
		yenergy_bound = (1-alpha)*np.linalg.norm(U_Mat_y)/2
		f = lambda l,bound: x if (np.linalg.norm(l[0:x]) == bound for x in range(len(l))) else None
		g = lambda l,bound: x if (np.linalg.norm(l[x:len(l)]) == bound for x in range(len(l))) else None
		(x1,x2) = (f(U_Mat_x,xenergy_bound),g(U_Mat_x,xenergy_bound))
		print(x1 +" "+ x2)
		#(y1,y2) = (f(U_Mat_y,yenergy_bound),g(U_Mat_y,yenergy_bound))
		#(x,y) = (int(x1)+1,int(y1)+1)
		#(width,height) = (x2-x1+2,y1-y2+2)
		out_dict = {"name": "region_of_interest", "x1" : x1, "x2" : x2, "y1" : y1, "y2" : y2}
	except:
		out_dict = {}
		print("Region of Interest extraction error")
		raise
	return img, out_dict

  # Reference: "Photo and Video Qualtiy Evaluation: Focousing on the Subject" - Lou & Tang.
  # A measure of the distinction between the subject in focous and the background.
def clarity_contrast(img,beta = 0.2):
	try:
		img2, out_dict = region_of_interest(img)
		roi = cv2.GetSubRect(img,GetImageROI(img2))
		fourier_img = cv2.cvDFT(img)
		fourier_roi = cv2.cvDFT(roi)
		img_area = len(img)*len(img[0])
		(x,y,roi_width,roi_height) = GetImageROI(img2)
		roi_area = roi_width*roi_height
		img_max = max(fourier_img)
		roi_max = max(fourier_roi)
		img_set = 0.0
		roi_set = 0.0
		for item in list(fourier_img):
			if item >= beta*img_max:
				image_set += item*item
		for item in list(fourier_roi):
			if item >= beta*roi_max:
				roi_set += item*item
		m_i = np.sqrt(image_set)
		m_r = np.sqrt(roi_set)
		clarity_feature = (m_r/roi_area)/(m_i/img_area)
		out_dict = {"name" : "clarity_contrast", "value" : clarity_feature}
	except:
		out_dict = {}
		raise
	return out_dict

  # Reference: "Color Harmonization" - Cohen-Or et al.
  # Measure of the harmony of colors in an image.
  ## Difficult, need to consider pattern matching algoritms.
def color_harmony(img):
	try:
		out_dict = {}
	except:
		out_dict = {}
		raise
	return out_dict

  # Reference: "Photo and Video Qualtiy Evaluation: Focousing on the Subject" - Lou & Tang.
  # Measure of color harmony through hues
  ## Don't have training pictures.
def alt_color_harmony(img):
	try:
		out_dict = {}
	except:
		out_dict = {}
		raise
	return out_dict


  # Reference: "Photo and Video Qualtiy Evaluation: Focousing on the Subject" - Lou & Tang.
  # Distribution of the compositional elements of the image around the 4 power points of the image.
def composition_geometry(img):
	try:
		img2, out_dict = region_of_interest(img)
		(i,j,roi_width,roi_height) = cv2.GetImageROI(img2)
		c_x = round(i+roi_width/2)
		c_y = round(j+roi_height/2)
		X = len(img[1])
		Y = len(img)
		geometry_measure = "inf" #NOTE must find float max
		power_points = [(X/3,Y/3),(2*X/3,Y/3),
			(X/3,2*Y/3),(2*X/3,2*Y/3)]
		for (x,y) in power_points:
			value = np.sqrt((c_x - x)*(c_x - x)/(X*X)
				+ (c_y - y)*(c_y - y)/(Y*Y))
			if value < geometry_measure:
				geometry_measure = value
		out_dict = {"name" : "composition_geometry", "value" : geometry_measure}
	except:
		out_dict = {}
		raise
	return out_dict

  # Reference: "Photo and Video Qualtiy Evaluation: Focousing on the Subject" - Lou & Tang.
  # Measure of the simplicity of the background of an image.
def simplicity(img, gamma=0.1):
  #NOTE Probably fucked up.
	try:
		img2, out_dict = region_of_interest(img)
		img3 = cv2.GetSubRect(img,cv2.GetImageROI(img2))
		background = cv2.Sub(img2,ROI) # There may be an issue with the arrays not being of the same size.
		# Need to quantize the image into 16 channels.
		hist,_binedges = np.histogram(background, bins=4096)
		max_bound = max(list(hist))
		color_div = 0.0
		for item in list(hist):
			if item >= gamma*max_bound:
				color_div += item*item
		simplicity_measure = np.sqrt(color_div)/4.096 
		out_dict = {"name" : "simplicity", "value" : simplicity_measure}
	except:
		out_dict = {}
		raise
	return out_dict

#============================================================================================
#				Video Feature Extractors
#============================================================================================

  # Reference: "Photo and Video Qualtiy Evaluation: Focousing on the Subject" - Lou & Tang.
  # Measure for the motion of the subject.
def subject_region_motion(vid):
	imgs, no_frames, fps = frame_reduction(in_file_name, fps = 5)
	frame_Y = len(imgs[1,:,:])*len(imgs[1,:,:])
	frame_X = len(imgs[1,1,:])*len(imgs[1,1,:])
	try:
		centroid_variation_sum = 0.0
		for i in len(imgs):
			img, out_dict = region_of_interest(imgs[i])
			(i,j,roi_width,roi_height) = cv2.GetImageROI(img)
			xcentroid_img1 = round(i+roi_width/2)
			ycentroid_img1 = round(j+roi_height/2)
			img, out_dict = region_of_interest(imgs[i+1])
			(i,j,roi_width,roi_height) = cv2.GetImageROI(img)
			xcentroid_img2 = round(i+roi_width/2)
			ycentroid_img2 = round(j+roi_height/2)
			centroid_variation_sum += np.sqrt((xcentroid_img2-xcentroid_img1)*(xcentroid_img2-xcentroid_img1)/(frame_X*frame_X )
				(ycentroid_img2-ycentroid_img1)*(ycentroid_img2-ycentroid_img1)/(frame_Y*frame_Y))
		region_motion_measure = centroid_variation_sum/(no_frames-1)
		out_dict = {"name" : "subject_region_motion", "value" : region_motion_measure}
	except:
		out_dict = {}
		raise
	return out_dict

  # Reference: "Photo and Video Qualtiy Evaluation: Focousing on the Subject" - Lou & Tang.
  # Measure for motion stabilty using Yan and Kankanhali's method.
def motion_stability(img):
	try:
		 out_dict = {}
	except:
		 out_dict = {}
		 raise
	return out_dict
