import cv2 as cv
import math
import time
import argparse
from apps.firebasee import insert_data_for_genderCharts
import threading 
from functions.timerFlags import *
from datetime import datetime


delay = 60
inpWidth = 227
inpHeight = 227

def getFaceBox(net, frame,conf_threshold = 0.75):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv.dnn.blobFromImage(frameOpencvDnn,1.0,(300,300),[104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []

    for i in range(detections.shape[2]):
        confidence = detections[0,0,i,2]
        if confidence > conf_threshold:
            x1 = int(detections[0,0,i,3]* frameWidth)
            y1 = int(detections[0,0,i,4]* frameHeight)
            x2 = int(detections[0,0,i,5]* frameWidth)
            y2 = int(detections[0,0,i,6]* frameHeight)
            bboxes.append([x1,y1,x2,y2])
            cv.rectangle(frameOpencvDnn,(x1,y1),(x2,y2),(0,255,0),int(round(frameHeight/150)),8)

    return frameOpencvDnn , bboxes



faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"

ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"

genderProto = "gender_deploy.prototxt" 
genderModel = "gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']


#load the network
ageNet = cv.dnn.readNet(ageModel,ageProto)
genderNet = cv.dnn.readNet(genderModel, genderProto)
faceNet = cv.dnn.readNet(faceModel, faceProto)

# cap = cv2.VideoCapture(0)
padding = 20

male_count = 0
female_count = 0
detected_genders = []
start_time = time.time()


def classifyGender(cap):
    global male_count
    global female_count
# while cv2.waitKey(1) < 0:
    #read frame
    t = time.time()
    hasFrame , frame = cap.read()

    small_frame = None

    if not hasFrame:
        cap.release()
        # cv2.waitKey()
    
    # print('Dimensions : ',face.shape)
    #creating a smaller frame for better optimization
    small_frame = cv.resize(frame,(0,0),None,1.0,1.0)

    

    frameFace ,bboxes = getFaceBox(faceNet, small_frame)
    # if not bboxes:
    #     print("No face Detected, Checking next frame")
    #     continue
    for bbox in bboxes:
        face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),
                max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]
        # blob = cv.dnn.blobFromImage(face, 1.0/255, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        blob = cv.dnn.blobFromImage(face, 1.0/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)

        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        #print("Gender : {}, conf = {:.3f}".format(gender, genderPreds[0].max()))

        if gender not in detected_genders:
            detected_genders.append(gender)
            if gender == 'Male':
                male_count += 1
            else:
                female_count += 1

        global start_time
        if getFlag():
            launch = threading.Timer(delay, insert_data_for_genderCharts, [datetime.timestamp(datetime.now()), male_count, female_count])
            launch.start()
            setFlag("false")
        end_time = time.time()
        if (end_time - start_time) >= delay:
            setFlag("true")
            start_time = time.time()


        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        #print("Age Output : {}".format(agePreds))
        #print("Age : {}, conf = {:.3f}".format(age, agePreds[0].max()))

        # label = "{},{}, M:{},F:{}".format(gender, age, male_count, female_count)
        label = "{}".format(gender)
        cv.putText(frameFace, label, (bbox[0], bbox[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv.LINE_AA)
        # frameFace = cv.resize(frame,(0,0),None,0.8,0.7)

        # cv2.imshow("Age Gender Demo", frameFace)
        success, jpg = cv.imencode('.jpg', frameFace)
        return jpg.tobytes()


    # print("time : {:.3f}".format(time.time() - t))
