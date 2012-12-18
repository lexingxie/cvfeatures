
import os, sys
import json
from datetime import datetime

from feature_core import proc_one_file
from feature_options import parse_input
from feature_utils import is_image_or_video


def cv_features(argv):
	# parse input args
	args = parse_input(argv)
	print_msg = True if args.verbose==3 else False

	if args.assemble_output:
		cur_out_file = os.path.join(args.out_dir, args.out_file_name)
		fo = open(cur_out_file, "w")
		#fo.write('{"images": [\n')
		fo.write('[\n')  # beginning of array of img jsons
	else:
		fo = None

	cnt = 0
	# loop over input items
	for item in args.input:
		# this is an image
		if is_image_or_video(item):
			cur_file = item
			cur_json,success = proc_one_file(cur_file, args)
			cnt += success

			outstr = json.dumps(cur_json, indent=4)
			if fo :
				fo.write( outstr + ",\n")
			else:
				cur_out_file = os.path.join(args.out_dir, 
					os.path.splitext(os.path.basename(item))[0]+".json" )
				open(cur_out_file, "w").write(outstr)

			if success and args.verbose == 3:
				print outstr
		# walk the dir to find all imgs if it's a dir
		elif os.path.isdir(item):
			for p, _n, flist in os.walk(item):
				for f in flist:
					cur_file = os.path.join(p, f)
					if is_image_or_video(cur_file):
						cur_json,success = proc_one_file(cur_file, args)
						cnt += success

					if success and args.verbose >= 1:
						print_msg = True if print_msg or (args.verbose==2 and cnt>0 and cnt%100 ==0) else False
						print_msg = True if print_msg or (args.verbose==1 and cnt>0 and cnt%1000==0) else False

						if print_msg:
							tt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
							print "%s %d files processed, the last one %s " % (tt, cnt, cur_file)

					outstr = json.dumps(cur_json, indent=4)
					if fo :
						if cnt == 0: # first entry
							fo.write( outstr )	
						else:
							fo.write( ",\n" + outstr ) # first append an array separator
					else:
						cur_out_file = os.path.join(args.out_dir, 
							os.path.splitext(os.path.basename(item))[0]+".json" )
						open(cur_out_file, "w").write(outstr)
					# assemble output, write json
					if success and args.verbose == 3:
						print outstr
		else:
			if print_msg:
				print "  skipped item %s" % item
	if fo :
		fo.write('\n]\n')  # end of array for img jsons
		fo.close()
		if print_msg:	print "%s last output file %s " % (tt, cur_out_file)
	
	# out-of-loop, done 
	if print_msg:
		tt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
		print "%s %d files processed, Done " % (tt, cnt)
	

if __name__ == '__main__':
	cv_features(sys.argv[1:])