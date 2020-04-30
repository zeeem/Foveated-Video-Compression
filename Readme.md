# Foveated Video Compression

A study and comparison between quantization based foveated video compression and interpolation based variable resolution technique.

## Required dependencies
- python 3.6 or higher
- numpy
- opencv
- imutils
- pillow (PIL)
- argparse

## How to run

- Make sure the required dependecies are installed

- Unzip the `FoveatedCompression.zip`

- Open terminal and `cd` to the extracted directory

### 1. VR compression:
- In the terminal write the command below and run.

		`python detect_faces_vr_compression.py -i image/test1.jpg`
	
- Here, `image/test1.jpg` is the location of the test image

- Press `q` to iterate through the output images

- the output images are saved in the root directory


### 2. Quantization video compression:
- In the terminal write the command below and run.

		`python fovea_video.py -v video/test5.mp4`
		
- Here, "video/test5.mp4" is the location of the test video

- To change the quantization rate use the command below:

		`python detect_faces_video.py -v video/test5.mp4 -q 70`
	
   Here, `-q` is an optional argument.
   
- Press `q` to stop streaming and close all window

- the output frames are saved in the `saved_frames` folder

## Results

VR Compression result
![VR compression result](https://github.com/zeeem/NN3D-Visualizer/blob/master/docs/vr_compr.jpg)

Color quantization Video Compression result
![Color quantization Video Compression result](https://github.com/zeeem/NN3D-Visualizer/blob/master/docs/face_ssd.jpg)

Output Comparison: Color quantization Video Compression vs VR Compression
![Output Comparison](https://github.com/zeeem/NN3D-Visualizer/blob/master/docs/quantize_vr_comapre.jpg)

Output Comparison: PSNR, SSIM, Compression ratio
![Output Comparison](https://github.com/zeeem/NN3D-Visualizer/blob/master/docs/psnr_ssim.jpg)



## Developers
[Naimur Rahman Jeem](https://www.linkedin.com/in/zeeem/)

[Subho Ghose](https://www.linkedin.com/in/subhoghose/)

[Hanming Li](https://www.linkedin.com/in/hanming-li-306b11199/)


## Acknowledgements
The basic code structure is based on the example code of [pyimagesearch](https://www.pyimagesearch.com/).


If needed, please contact at rahmanje[at]ualberta[dot]ca, subho[at]ualberta[dot]ca, hanming[at]ualberta[dot]ca.