
from keras_applications.vgg16 import VGG16
from keras.preprocessing.image import ImageDataGenerator

from keras import models, layers
from keras import optimizers

import keras
import math

import numpy as np

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

test_dir = "CarDatabaseShare/kcar_miniset_y_new/test_set/"
test_datagen = ImageDataGenerator(rescale=1. / 255)
vgg_model.load_weights("CarDatabaseShare/y_up_car_weight.hdf5")

test_generator = test_datagen.flow_from_directory(test_dir, batch_size=32, target_size=(224, 224), color_mode='rgb')

scores = vgg_model.evaluate_generator(test_generator, steps=math.ceil(test_generator.n / test_generator.batch_size))
print("%s: %.2f%%" %(vgg_model.metrics_names[1], scores[1]*100))

output = vgg_model.predict_generator(test_generator, steps=math.ceil(test_generator.n / test_generator.batch_size), verbose=1)
np.set_printoptions(formatter={'float':lambda x: "{0:0.3f}".format(x)})
print(test_generator.class_indices)
print(output)
#vgg_model.save_weights("final_weights.h5", )