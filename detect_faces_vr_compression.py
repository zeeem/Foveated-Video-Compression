# USAGE
# python detect_faces_vr_compression.py -i test/test1.jpg

import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

prototxt = 'deploy.prototxt.txt'
model = 'res10_300x300_ssd_iter_140000.caffemodel'
confidence_ = 0.5

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
image = cv2.imread(args["image"])
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
	(300, 300), (104.0, 177.0, 123.0))

print("[INFO] computing object detections...")
net.setInput(blob)
detections = net.forward()

for i in range(0, detections.shape[2]):
	confidence = detections[0, 0, i, 2]
	if confidence > confidence_:
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")
		text = "{:.2f}%".format(confidence * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		# cv2.rectangle(image, (startX, startY), (endX, endY),
		# 	(0, 0, 255), 2)
		# cv2.putText(image, text, (startX, y),
		# 	cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
		right = endX
		left = startX
		face_range = endX - startX
		range_right = w - right
		range_left = startX
		grad_left = int(range_left / 3)
		grad_right = int(range_right / 3)

		a = list(range(right, right + grad_right, 4))
		b = list(range(left - grad_left, left, 4))
		c = list(range(right + grad_right, right + grad_right * 2, 3))
		d = list(range(left - grad_left * 2, left - grad_left, 3))
		e = list(range(right + grad_right * 2, right + grad_right * 3, 2))
		f = list(range(left - grad_left * 3, left - grad_left * 2, 2))
		# colum need to be deleted

		res = a + b + c + d + e + f
		compressed__image = np.delete(image, res, 1)

		cv2.imshow("original", image)
		cv2.waitKey(0)
		cv2.imshow("compressed_", compressed__image)
		cv2.waitKey(0)
		cv2.imwrite("compressed_.jpg", compressed__image, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

		left_cut = b + d + f
		right_cut = a + c + e
		# left and right part deleted 

		need_recover_left = range(range_left - len(left_cut))
		need_recover_light = range(face_range + len(need_recover_left), compressed__image.shape[1])
		
		need_recover_left = compressed__image[:, :len(need_recover_left)]
		need_recover_light = compressed__image[:, (len(range(range_left - len(left_cut))) + face_range):]
		
		recovered_left = cv2.resize(need_recover_left, (range_left, h), interpolation = cv2.INTER_LANCZOS4)
		recovered_right = cv2.resize(need_recover_light, (range_right, h), interpolation = cv2.INTER_LANCZOS4)
		# resize the left and right part to original left and right part
		
		blank_image = np.zeros((h, w, 3), np.uint8)
		blank_image[:, :left] = recovered_left
		blank_image[:, right:] = recovered_right
		blank_image[:, left:right] = image[:, left:right]
		# cv2.imwrite('output.jpg', blank_image)
		cv2.imwrite("decompressed_output.jpg", blank_image, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

cv2.imshow("decompressed_output", blank_image)
cv2.waitKey(0)

# closing window
cv2.destroyAllWindows()