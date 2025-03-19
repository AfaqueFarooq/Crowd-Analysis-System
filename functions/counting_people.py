import cv2 as cv
import sys
import numpy as np
import os.path
from utils.centroidtracker import CentroidTracker
from utils.trackableobject import TrackableObject
from apps.firebasee import insert_data_for_charts
from functions.timerFlags import *
import threading 
import time
from datetime import datetime

delay = 60
confThreshold = 0.6
nmsThreshold = 0.4
inpWidth = 416
inpHeight = 416
Rects = []
people = 0 
totalDown = 0
totalUp = 0
        
classesFile = "coco.names"
classes = None

with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

modelConfiguration = "yolov3.cfg"
modelWeights = "yolov3.weights"
ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
writer = None

W = None
H = None

# instantiate our centroid tracker, then initialize a list to store
# each of our dlib correlation trackers, followed by a dictionary to
# map each unique object ID to a TrackableObject
trackers = []
trackableObjects = {}
start_time = time.time()

# load our serialized model from disk
net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
 # Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    global Rects, people, start_time
    rects = []

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        # Class "person"
        if classIds[i] == 0:
            rects.append((left, top, left + width, top + height))
            # use the centroid tracker to associate the (1) old object
            # centroids with (2) the newly computed object centroids
            
            objects = ct.update(rects)
            counting(frame, objects)
    Rects = rects
    people = len(rects)
    if getFlag():
        launch = threading.Timer(delay,insert_data_for_charts, [datetime.timestamp(datetime.now()), people])
        launch.start()
        setFlag("false")
    end_time = time.time()
    if (end_time - start_time) >= delay:
        setFlag("true")
        start_time = time.time() 

def getOutputsNames(net):
        # Get the names of all the layers in the network
        layersNames = net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        out_layers = []
        for i in net.getUnconnectedOutLayers():
            out_layers.append(layersNames[i - 1])

        return out_layers

def counting(frame, objects):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    global totalDown
    global totalUp

    # loop over the tracked objects
    for (objectID, centroid) in objects.items():
        # check to see if a trackable object exists for the current
        # object ID
        to = trackableObjects.get(objectID, None)

        # if there is no existing trackable object, create one
        if to is None:
            to = TrackableObject(objectID, centroid)

        # otherwise, there is a trackable object so we can utilize it
        # to determine direction
        else:
            # the difference between the y-coordinate of the *current*
            # centroid and the mean of *previous* centroids will tell
            # us in which direction the object is moving (negative for
            # 'up' and positive for 'down')
            y = [c[1] for c in to.centroids]
            direction = centroid[1] - np.mean(y)
            to.centroids.append(centroid)

            # check to see if the object has been counted or not
            if not to.counted:
                # if the direction is negative (indicating the object
                # is moving up) AND the centroid is above the center
                # line, count the object

                if direction < 0 and centroid[1] in range(frameHeight//2 - 30, frameHeight//2 + 30):
                    totalUp += 1
                    to.counted = True

                # if the direction is positive (indicating the object
                # is moving down) AND the centroid is below the
                # center line, count the object
                elif direction > 0 and centroid[1] in range(frameHeight//2 - 30, frameHeight//2 + 30):
                    totalDown += 1
                    to.counted = True

        trackableObjects[objectID] = to
        
        cv.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
    info = [
        ("Up", totalUp),
        ("Down", totalDown),
    ]

    for (i, (k, v)) in enumerate(info):

        text = "{}".format(v)
        if k == 'Up':
            cv.putText(frame, f'Up : {text}', (10, 80),
                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        if k == 'Down':
            cv.putText(frame, f'Down : {text}', (10, 120),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
    cv.putText(frame, f'People: ', (10, 160), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv.putText(frame, f'{people}', (120, 160), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    for rect in Rects:
        cv.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0,255,0), 2)
    
        
def computePeople(cap):
    
    #vid_writer = cv.VideoWriter(outputFile, cv.VideoWriter_fourcc('M','J','P','G'), 30, (round(cap.get(cv.CAP_PROP_FRAME_WIDTH)),round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

        
    hasFrame, frame = cap.read()

    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    cv.line(frame, (0, frameHeight // 2), (frameWidth, frameHeight // 2), (0, 255, 255), 2)
    
    if not hasFrame:
        cap.release()
        

    blob = cv.dnn.blobFromImage(frame, 1.0/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)

    net.setInput(blob)

    outs = net.forward(getOutputsNames(net))

    postprocess(frame, outs)

    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
    cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5/2, (0, 0, 255))
    #vid_writer.write(frame.astype(np.uint8))
    frame = cv.resize(frame,(0,0),None,1.2,1.0)

    success, jpg = cv.imencode('.jpg', frame)
    return jpg.tobytes()
