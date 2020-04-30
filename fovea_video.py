# USAGE
# python fovea_video.py -v video/test2.mp4
# or
# python fovea_video.py -v video/test2.mp4 -q 70

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS
from PIL import Image
import numpy as np
import argparse
import imutils
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",  required=True, default='video/test2.mp4',
	help="path to video file")
ap.add_argument('-q', "--quality", default = 70, 
	help = "Rate of Background Compression, 1 = Lowest Quality, 256 = Best Quality", type = int)
args = vars(ap.parse_args())

prototxt = 'deploy.prototxt.txt'
model = 'res10_300x300_ssd_iter_140000.caffemodel'
confidence_ = 0.5

# function to reduce the color fluctutation
def compare_frame(oldFrame, newFrame):
	oldFrame = np.asarray(oldFrame)
	newFrame = np.asarray(newFrame)
	newFrame.setflags(write=1)

    # checking if oldframe is a np ndarray
	try:
		if(oldFrame.size):
			print('its a np array')
		else:
			print('not a np array')
			return Image.fromarray(newFrame)
	except:
		return Image.fromarray(newFrame)

    # looping through the old and new frame to calculate the difference 
    # between pixels. Update pixels in the new frame only if its different
    # than a certain level from old frame, to reduce fluctuation
	for i in range(oldFrame.shape[0]):
		for j in range(oldFrame.shape[1]):
			diff = abs(np.average(newFrame[i,j])-np.average(oldFrame[i,j]))
			# print(diff)
			if(diff<20):
				newFrame[i,j] = oldFrame[i,j] 
			else:
				pass
	return Image.fromarray(newFrame)

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
filename = args["video"]
vs = FileVideoStream(filename).start()
time.sleep(2.0)
count = 0
old_frame_bg = []
fps = None
# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

    # saving the original frame
	cv2.imwrite("saved_frames/before/frame%d.jpg" % count, frame)

    # quantizing the bg frame
	frame_bg = Image.fromarray(frame)
	frame_bg = frame_bg.quantize(args["quality"]).convert('RGB')

    ## reducing frame flactuation (take a lot of time to process)
    # frame_bg2 = compare_frame(old_frame_bg,frame_bg)
	# old_frame_bg = frame_bg
	# frame_bg = frame_bg2

	# grab the frame dimensions and convert it to a blob
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
		(300, 300), (104.0, 177.0, 123.0))
        
    # starting fps count
	fps = FPS().start()

    # pass the blob through the network and obtain the detections and
	# predictions
	net.setInput(blob)
	detections = net.forward()

	# loop over the detections
	# initialize the set of information we'll be displaying on
	# the frame
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence < 0.5:
			continue
			
		# compute the (x, y)-coordinates of the bounding box for the
		# object
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")

		# merging face to compressed bg image 
		faces = frame[startY:endY, startX:endX]
		# faces=cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)
		faces = Image.fromarray(faces)
		frame_bg = Image.fromarray(np.asarray(frame_bg))
		frame_bg.paste(faces, (startX, startY, endX, endY))
		frame_bg = np.asarray(frame_bg)
		
        # finish fps computing
		fps.update()
		fps.stop()

        # saving the new compressed frame
		cv2.imwrite("saved_frames/after/frame%d.jpg" % count, frame_bg, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
		count +=1

        # draw the bounding box of the face along with the associated
		# probability

		text = "{:.2f}%".format(confidence * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		cv2.rectangle(frame_bg, (startX, startY), (endX, endY),
			(0, 0, 200), 1)
		# cv2.putText(frame_bg, text, (startX, y),
		# 	cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)

		info = [
			("FPS", "{:.2f}".format(fps.fps()))
		]

		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame_bg, text, (10, h - ((i * 20) + 20)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

	if(frame_bg.size):
		pass
	else:
		frame_bg = frame
	# show the output frame
	cv2.imshow("Frame", frame_bg)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# closing video stream and window
cv2.destroyAllWindows()
vs.stop()

