
import keras

from keras_applications.vgg16 import VGG16
from keras.callbacks import ModelCheckpoint, EarlyStopping

from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator

from keras import models, layers
from keras import optimizers, initializers, regularizers, metrics

import keras
import matplotlib.pyplot as plt
#import cv2 as cv
#import numpy as np
#import pandas as pd

import os
import random
import math

#from keras import backend as K
#K.tensorflow_backend._get_available_gpus()

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

print(os.getcwd())

train_dir = "CarDatabaseShare/kcar_miniset_y_new/train_set/"
test_dir = "CarDatabaseShare/kcar_miniset_y_new/test_set/"
val_dir = "CarDatabaseShare/kcar_miniset_y_new/valid_set/"

train_datagen = ImageDataGenerator(rescale=1. / 255,
                                   zoom_range=[0.9, 1.1],
                                   rotation_range=10,
                                   shear_range=5.0,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   horizontal_flip=True
                                   )
val_datagen = ImageDataGenerator(rescale=1. / 255,
                                   zoom_range=[0.9, 1.1],
                                   rotation_range=10,
                                   shear_range=5.0,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   horizontal_flip=True
                                   )
test_datagen = ImageDataGenerator(rescale=1. / 255,
                                   zoom_range=[0.9, 1.1],
                                   rotation_range=10,
                                   shear_range=5.0,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   horizontal_flip=True
                                   )
 # batchsize 64->256
train_generator = train_datagen.flow_from_directory(train_dir, batch_size=32, target_size=(224, 224), color_mode='rgb')
val_generator = val_datagen.flow_from_directory(val_dir, batch_size=32, target_size=(224, 224), color_mode='rgb')

#vgg_model.load_weights("y_fifth_weights.h5")

early_stopping = EarlyStopping(patience = 5)

checkpoint = ModelCheckpoint(filepath="CarDatabaseShare/y_eighth_car_weight.hdf5",
                             monitor='loss',
                             mode='min',
                             save_best_only=True
                             )

history = vgg_model.fit_generator(train_generator,
                                  steps_per_epoch=math.ceil(train_generator.n / train_generator.batch_size),
                                  epochs = 25, # first 30
                                  validation_data=val_generator,
                                  validation_steps=math.ceil(val_generator.n / val_generator.batch_size),
                                  callbacks=[checkpoint, early_stopping],
                                  verbose=1)
#

vgg_model.save_weights("y_eighth_weights.h5")
print("Saved model to disk")

test_generator = test_datagen.flow_from_directory(test_dir, batch_size=32, target_size=(224, 224), color_mode='rgb')

scores = vgg_model.evaluate_generator(test_generator, steps=math.ceil(test_generator.n / test_generator.batch_size))
print("%s: %.2f%%" %(vgg_model.metrics_names[1], scores[1]*100))

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Accuracy')
plt.legend()
plt.figure()

plt.plot(epochs, loss, 'ro', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Loss')
plt.legend()

plt.show()