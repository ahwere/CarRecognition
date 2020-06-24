import cv2 as cv
import os
import sys
from scipy.spatial import distance
import numpy as np
from collections import OrderedDict
import shutil
import random

def imread(filename, flags=cv.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv.imencode(ext, img, params)
        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

if __name__ =="__main__":
    # Load Yolo
    net = cv.dnn.readNet("CarDatabaseShare/yolov3.weights", "CarDatabaseShare/yolov3.cfg")
    classes = []
    with open("CarDatabaseShare/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    print(len(classes))
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    print(colors)

    bbox_colors = np.random.randint(0, 255, size=(len(classes), 3))
    print(bbox_colors)

    ddir = "CarDatabaseShare/kcar_miniset_raw/"
    sdir = "CarDatabaseShare/kcar_miniset_y_new/"
    setlist = os.listdir(sdir)
    klist = os.listdir(ddir) #modified
    kklist = []

    print(klist)
    print(setlist)

    testcnt = 0
    # 모닝2017, 아반떼AD, 스포티지2017
    for ii in klist: #modified
        listdirr = []
        listdirr = os.listdir(ddir + "/" + ii)
        random.shuffle(listdirr)
        totalfilecnt = len(listdirr)
        print(totalfilecnt)
        savefilecnt = 0
        for j in listdirr:
            stra = ddir + ii + "/" + j
            print(stra)
            img = imread(stra)
            height, width, channels = img.shape
            # Detecting objects
            blob = cv.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

            net.setInput(blob)
            outs = net.forward(output_layers)

            # Showing informations on the screen
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            #print(indexes)
            font = cv.FONT_HERSHEY_PLAIN

            cropcnt = 0

            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    if h > 250 and w > 450:
                        label = str(classes[class_ids[i]])
                        imgcpy = img.copy()
                        imgcpy = img[y:y+h, x:x+w]
                        cropcnt += 1
                        #cv2_imshow(imgcpy)
                        try:
                            imgcpy = cv.cvtColor(imgcpy, cv.COLOR_BGR2GRAY)
                            imgcpy = cv.resize(imgcpy, dsize=(224, 224), interpolation=cv.INTER_AREA)
                            imgcpy = cv.GaussianBlur(imgcpy, (3,3), 0)
                            #cv2_imshow(imgcpy)
                            #cv.imwrite("ddir + '/' + kklist[ii] + '/' + j ,imgcpy)
                            cannimg = cv.Canny(imgcpy, 25, 50)
                            #cv.imshow('', cannimg)
                            if savefilecnt <= int(totalfilecnt * 0.2):
                                imwrite(sdir + setlist[0] + '/' + ii + '/' + j, cannimg)
                            elif savefilecnt <= int(totalfilecnt * 0.8):
                                imwrite(sdir + setlist[1] + '/' + ii + '/' + j, cannimg)
                            else:
                                imwrite(sdir + setlist[2] + '/' + ii + '/' + j, cannimg)
                            savefilecnt += 1
                        except:
                            continue
        print("finish" + str(ii))
