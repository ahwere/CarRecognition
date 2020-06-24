from keras_applications.vgg16 import VGG16
from keras import models, layers
from keras import optimizers

import keras

class CarClassifier:
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

    output_label = vgg_model.predict_classes()

    #return output_label