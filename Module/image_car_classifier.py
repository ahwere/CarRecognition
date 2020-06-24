import cv2 as cv
import os
import sys
from scipy.spatial import distance
import numpy as np
from collections import OrderedDict
import shutil
import random
import PIL

from keras_applications.vgg16 import VGG16
from keras import models, layers
from keras import optimizers

import keras

def Rotate(src, degrees):
    if degrees == 90:
        dst = cv.transpose(src) # 행렬 변경
        dst = cv.flip(dst, 1)   # 뒤집기

    elif degrees == 180:
        dst = cv.flip(src, 0)   # 뒤집기

    elif degrees == 270:
        dst = cv.transpose(src) # 행렬 변경
        dst = cv.flip(dst, 0)   # 뒤집기
    else:
        dst = None
    return dst

def CarClassifier(npimg, model):
    try:
        npimg = npimg.astype('float32')/255.0
        pred = model.predict(npimg)
        print(pred)
        output_label = model.predict_classes(npimg)
        print(output_label)
        labelstr = car_label_strlist[int(output_label[0])][0]
        return labelstr
    except:
        print("error")

def imread(filename, flags=cv.IMREAD_COLOR, dtype=np.uint8): # code snippet for read utf-8
    try:
        n = np.fromfile(filename, dtype)
        img = cv.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def imwrite(filename, img, params=None): # code snippet for read utf-8
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
    writer = None
    car_label_strlist = np.loadtxt("car_label3.csv", delimiter=',', dtype='str')
    #load vgg16
    pre_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3), backend=keras.backend,
                      layers=keras.layers, models=keras.models, utils=keras.utils)
    pre_model.trainable = True
    pre_model.summary()

    # add output layer for VGG16 output (4096 -> 1000 => 4096 -> 1000 -> 100)
    vgg_model = models.Sequential()
    vgg_model.add(pre_model)
    vgg_model.add(layers.Flatten())
    vgg_model.add(layers.Dense(4096, activation='relu'))
    vgg_model.add(layers.Dense(1024, activation='relu'))
    vgg_model.add(layers.Dense(20, activation='softmax'))  # practical

    vgg_model.summary()
    vgg_model.compile(loss='categorical_crossentropy', optimizer=optimizers.RMSprop(lr=2e-5), metrics=['acc'])
    vgg_model.load_weights("y_seventh_weights.h5")

    #vgg_model.load_weights("CarDatabaseShare/y_up_car_weight.hdf5")'''
    # Load Yolo
    net = cv.dnn.readNet("CarDatabaseShare/yolov3.weights", "CarDatabaseShare/yolov3.cfg")

    classes = []
    with open("CarDatabaseShare/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    #print(len(classes))
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    #print(colors)

    bbox_colors = np.random.randint(0, 255, size=(len(classes), 3))
    #print(bbox_colors)

    for t in range(1, 40):
        frame = imread("captured_image/" + str(t) + ".png")

        if frame is None:
            continue

        savecnt = 31000
        framecnt = 0

        #frame = Rotate(frame, 90)

        height, width, channels = frame.shape

        # Detecting objects
        blob = cv.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)

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
        # print(indexes)
        font = cv.FONT_HERSHEY_PLAIN

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                if h > 50 and w > 50 and class_ids[i] == 2:
                    cropimg = frame.copy()
                    cropimg = frame[y:y+h, x:x+w]
                    try:
                        imwrite('car_cropped_3/' + str(car_recog) + '/' + str(savecnt) +'.jpg', cropimg)
                        savecnt += 1
                        cropimg = cv.cvtColor(cropimg, cv.COLOR_BGR2GRAY)
                        cropimg = cv.resize(cropimg, dsize=(224, 224), interpolation=cv.INTER_AREA)
                        cropimg = cv.GaussianBlur(cropimg, (3, 3), 0)
                        cannimg = cv.Canny(cropimg, 30, 100)
                        npimg = np.asarray(cannimg)
                        npimg = np.stack((cannimg,)*3, axis=-1)
                        npimg = np.expand_dims(npimg, axis=0)
                        #print(npimg.shape)
                        car_recog = CarClassifier(npimg, vgg_model)
                        imwrite('car_cropped_3/' + str(car_recog) + '/' + str(savecnt) +'.jpg', cannimg)
                        savecnt += 1
                        #print(car_recog)
                    except:
                        continue
                    color = colors[i]
                    cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv.imshow('', frame)
        #cv.waitKey(0)
    cv.destroyAllWindows()