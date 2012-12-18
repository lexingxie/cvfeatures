cvfeatures
==========

image/video feature extraction toolkit, using OpenCV (cv2)
depend on numpy

read input image/video or directory containing many images
output json of various features

TODOs
=====
* TODO 2012-12-18 decide on which set of features to extract (Lexing and Prithvi)
* TODO 2012-12-18 concatenating the json output has error right now 
* TODO 2012-12-18 a number of command options does not work right now (zipped output, etc)

dir structure
=====
test.sh -- test script, also see here for example use
./imgs -- a number of test imgs
./tmp -- where the test outputs go, its content should not be committed to git
./src -- source code dir, cvfeatures.py is the main script
./apps -- application / utility scripts for processing data, not part of the core (reusable) tools

misc
=====
this seems a pretty good recipe for installing opencv on ubuntu 12.04
http://www.ozbotz.org/opencv-installation/