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

#from keras import backend as K
#K.tensorflow_backend._get_available_gpus()

pre_model = VGG16(weights=None, include_top=False, input_shape=(224, 224, 3), backend=keras.backend,
                  layers=keras.layers, models=keras.models, utils=keras.utils)
pre_model.trainable = False
pre_model.summary()

# add output layer for VGG16 output (4096 -> 1000 => 4096 -> 1000 -> 100)
vgg_model = models.Sequential()
vgg_model.add(pre_model)
vgg_model.add(layers.Flatten())
vgg_model.add(layers.Dense(4096, activation='relu'))
vgg_model.add(layers.Dense(1024, activation='relu'))
vgg_model.add(layers.Dropout(0.5))
vgg_model.add(layers.Dense(20, activation='softmax'))  # practical

vgg_model.summary()

vgg_model.compile(loss='categorical_crossentropy', optimizer=optimizers.RMSprop(lr=2e-5), metrics=['acc'])

print(os.getcwd())

train_dir = "CarDatabaseShare/kcar_miniset_y/train_set/"
test_dir = "CarDatabaseShare/kcar_miniset_y/test_set/"
val_dir = "CarDatabaseShare/kcar_miniset_y/valid_set/"

train_datagen = ImageDataGenerator(rescale=1. / 255, width_shift_range=0.1, height_shift_range=0.1,
                                   zoom_range=[0.9, 1.0])
val_datagen = ImageDataGenerator(rescale=1. / 255, width_shift_range=0.1, height_shift_range=0.1, zoom_range=[0.9, 1.0])
test_datagen = ImageDataGenerator(rescale=1. / 255)
 # batchsize 64->256
train_generator = train_datagen.flow_from_directory(train_dir, batch_size=128, target_size=(224, 224), color_mode='rgb')
val_generator = val_datagen.flow_from_directory(val_dir, batch_size=128, target_size=(224, 224), color_mode='rgb')

vgg_model.load_weights("y_t_weights.h5")

early_stopping = EarlyStopping(patience = 20)

checkpoint = ModelCheckpoint(filepath="CarDatabaseShare/y_t_car_weight.hdf5",
                             monitor='loss',
                             mode='min',
                             save_best_only=True
                             )

history = vgg_model.fit_generator(train_generator,
                                  steps_per_epoch=1000,
                                  epochs=1, # 50 -> 100
                                  validation_data=val_generator,
                                  validation_steps=100,
                                  callbacks=[checkpoint, early_stopping],
                                  verbose=1)
#math.ceil(train_generator.n / train_generator.batch_size)

vgg_model.save_weights("y_t_weights.h5")
print("Saved model to disk")

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
plt.savefig('plot.png')