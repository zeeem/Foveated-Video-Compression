## Required dependencies
- python 3.6 or higher
- numpy
- opencv
- imutils
- pillow (PIL)
- argparse

## How to run
	a. Make sure the required dependecies are installed
	b. Unzip the "FoveatedCompression.zip"
	c. Open terminal and `cd` to the extracted directory

### 1. VR compression:
	a. In the terminal write the command below and run.
		`python detect_faces_vr_compression.py -i image/test1.jpg`
	b. Here, "image/test1.jpg" is the location of the test image.
	c. Press 'q' to iterate through the output images
	d. the output images are saved in the root directory

### 2. Quantization video compression:
	a. In the terminal write the command below and run.
		`python fovea_video.py -v video/test5.mp4`
	b. Here, "video/test5.mp4" is the location of the test video.
	c. To change the quantization rate use the command below:
		`python detect_faces_video.py -v video/test5.mp4 -q 70`
	   Here, -q is an optional argument.
	d. Press 'q' to stop streaming and close all window.
	e. the output frames are saved in the "saved_frames" folder