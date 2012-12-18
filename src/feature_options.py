
#from optparse import OptionParser
import os

from argparse import ArgumentParser

def parse_input(argv):
	if len(argv)<2:
		argv = ['-h']

	parser = ArgumentParser(description='image/video feature extraction toolkit, using OpenCV')
	parser.add_argument('-i', '--input', dest='input', default="", help='input file or dir')
	parser.add_argument('-o', '--out_dir', dest='out_dir', default="", help='')
	parser.add_argument('-a', '--assemble_output', dest='assemble_output', type=int,
	    default=0, help='save json for each input file, or [assmeble all into one]')
	
	parser.add_argument('-f', '--feature_list', dest='feature_list', 
		default="gray_histogram16,average_rgb", help='list of feature names to extract')
	parser.add_argument('-p', '--pre_processing', dest='pre_processing', 
		default=None, help='list of (global) pre-processing operations')
	parser.add_argument('-v', '--verbose', dest='verbose', type=int,
		default=1, help='verbose level (0: completely quiet, [1], ..., 3: print a lot)')
	
	adv_option = parser.add_argument_group(title='advanced options',
		description='these should be less oftenly tweaked by users')
	adv_option.add_argument('--out_file_name', dest='out_file_name', default="cvfeatures.json", help='')
	adv_option.add_argument('--incremental', dest='incremental', type=int,
			default=0, help='incremental processing, i.e. read existing input')
	adv_option.add_argument('--pre_scale', dest='pre_scale', type=int, 
		default=320, help='max. dimension of pre-scaling before feature extraction')
	adv_option.add_argument('-z', '--zip_output', dest='zip_output', 
		default="", help='save json [unzipped]/.gz/.zip/.bzip2 (to save space)')
	
	args = parser.parse_args(argv)
	if args.verbose==3:
		print args

	args.input = args.input.split(",")
	if not type(args.input) is list:
		args.input = [args.input]
	
	if args.verbose:
		print " processing input from: %s" % str(args.input) #( "\n".join(args.input) )
	
	if not args.out_dir:
		args.out_dir = os.path.dirname(args.input[0])
		if args.verbose:
			print " set output path to %s" % args.out_dir
	
	return args