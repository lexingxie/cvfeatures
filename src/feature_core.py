
import cv2
import numpy as np

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
			print " empty output for image %s " % in_file_name

	return success

def proc_one_file(in_file_name, args):
	if args.verbose>=2:
		print "processing file " + in_file_name
	
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

	return out_json, success

""" feature computation code below
"""

def gray_histogram(img, num_bins):
	try:
		img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		#rng = np.array([0, 256])
		#hist = cv2.calcHist(img2, [0], None, [num_bins], rng)
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





