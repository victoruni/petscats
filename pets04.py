# USAGE
# python pets04.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel --show True
# python3 pets04.py --prototxt mobilenet-ssd.prototxt --model mobilenet-ssd.caffemodel --show True -c 0.3
# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import sys
import argparse
import imutils
import time
import cv2
from urllib.request import urlopen
from datetime import datetime
import os

tekcamera=1
pathSaveImg="/home/petin/python3_prgs_1/OpenVino01"
cameras=[[0,0,0,0,0],
	[0,0,0,0,0],
	[False,False,False,False,False],
	["","Camera1","Camera2","Camera3","Camera4"]]

cameras[1][1] = 'rtsp://admin:191066@192.168.0.109:554/mode=real&idc=1&ids=1'
cameras[1][2] = 'rtsp://admin:191066@192.168.0.109:554/mode=real&idc=2&ids=1'
cameras[1][3] = 'rtsp://admin:191066@192.168.0.109:554/mode=real&idc=3&ids=1'
cameras[1][4] = 'rtsp://admin:191066@192.168.0.109:554/mode=real&idc=4&ids=1'


fps = FPS().start()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("--show", required=True, 
	help="Show cv2.imshow)")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))



# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
# initialize the video stream, allow the cammera sensor to warmup,
print("[INFO] starting video stream...")

#if args["source"] == "webcam":
#vs = cv2.VideoCapture(host)
#vs[0] = cv2.VideoCapture(cameras[0][t])
for i in range(1,5):
	cameras[0][i] = cv2.VideoCapture(cameras[1][i])
#cameras[0][1] = cv2.VideoCapture(cameras[1][1])
#cameras[0][3] = cv2.VideoCapture(cameras[1][3])
print("OK")
time.sleep(5.0)

detected_objects = []
# loop over the frames from the video stream
while(1):
	tekcamera = tekcamera +1
	if tekcamera == 5:
		tekcamera = 1
		ff=open("log.txt","w+")
		ftime=datetime.now()
		strlog=ftime.strftime("%d-%m-%Y_%H:%M:%S.%f")
		ff.write(strlog)
		ff.close()

	if cameras[2][tekcamera] == False:
		continue	
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	ret, frame = cameras[0][tekcamera].read()
	
	frame = imutils.resize(frame, width=800)
		
	# grab the frame dimensions and convert it to a blob
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)

	# pass the blob through the network and obtain the detections and
	# predictions
	net.setInput(blob)
	detections = net.forward()
    
	# loop over the detections
	print("******************")
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
		confidence = detections[0, 0, i, 2]
		idx = int(detections[0, 0, i, 1])
		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		#if confidence > args["confidence"]:
		if confidence > args["confidence"] and idx==15 :
		#if confidence > args["confidence"] and (idx==8 or idx==12) :
			# save files
			ftime=datetime.now()
			if(os.path.exists(pathSaveImg+"/cam"+str(tekcamera)+"/"+ftime.strftime("%d-%m-%Y"))==False):
				os.mkdir(pathSaveImg+"/cam"+str(tekcamera)+"/"+ftime.strftime("%d-%m-%Y"))
			f=cv2.imwrite(pathSaveImg+"/cam"+str(tekcamera)+"/"+ftime.strftime("%d-%m-%Y")+"/_"+ftime.strftime("%H:%M:%S.%f")+".jpg", frame)
			print("write file = ",f)


			# extract the index of the class label from the
			# `detections`, then compute the (x, y)-coordinates of
			# the bounding box for the object
			#idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# draw the prediction on the frame
			label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
			print(confidence,"  ",idx," - ",CLASSES[idx])
			detected_objects.append(label)
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
			
	# show the output frame
	#cv2.imshow("Frame", frame)
	if args["show"] == "True":
		cv2.imshow(cameras[3][tekcamera], frame)

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	fps.update()


fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
