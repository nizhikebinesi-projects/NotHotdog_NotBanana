import tensorflow as tf
import keras

from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications import ResNet50
from keras.layers import Input, Convolution2D, GlobalAveragePooling2D, Dense, Activation, BatchNormalization, LeakyReLU
# from keras.layers.core import Dropout, BatchNormalization
from keras.layers.core import Flatten
# from keras.layers.core import Dense
# from keras.layers import Input
from keras.models import Model


# from keras.layers import Input, Convolution2D, GlobalAveragePooling2D, Dense, Activation, BatchNormalization, LeakyReLU
from keras.layers import MaxPool2D
from keras.models import Sequential

def get_model4(weights_path):
    global graph
    graph = tf.get_default_graph()

    num_classes = 2
    baseModel = MobileNetV2(
        weights=None,
        include_top=False,
        input_tensor=Input(shape=(224, 224, 3))
    )

    headModel = baseModel.output
    headModel = Flatten(name="flatten")(headModel)
    headModel = BatchNormalization()(headModel)
    headModel = Dense(100, activation="relu")(headModel)
    headModel = BatchNormalization()(headModel)
    headModel = Dense(100, activation="relu")(headModel)
    headModel = Dense(num_classes, activation="sigmoid")(headModel)

    model = Model(inputs=baseModel.input, outputs=headModel)

    model.load_weights(weights_path)

    return model


def get_model3(weights_path):
    global graph
    graph = tf.get_default_graph()

    num_classes = 2
    baseModel = ResNet50(
        weights=None,
        include_top=False,
        input_tensor=Input(shape=(224, 224, 3))
    )

    headModel = baseModel.output
    headModel = Flatten(name="flatten")(headModel)
    headModel = Dense(100, activation="relu")(headModel)
    headModel = BatchNormalization()(headModel)
    headModel = Dense(100, activation="relu")(headModel)
    headModel = Dense(num_classes, activation="sigmoid")(headModel)

    model = Model(inputs=baseModel.input, outputs=headModel)

    model.load_weights(weights_path)

    return model


def get_model1(weights_path):
    global graph
    graph = tf.get_default_graph()

    num_classes = 2
    baseModel = MobileNetV2(
        weights=None,
        include_top=False,
        input_tensor=Input(shape=(300, 300, 3))
    )
    headModel = baseModel.output
    headModel = Flatten(name="flatten")(headModel)
    headModel = Dense(16, activation="relu")(headModel)
    headModel = Dropout(0.5)(headModel)
    headModel = Dense(num_classes, activation="sigmoid")(headModel)
    model = Model(inputs=baseModel.input, outputs=headModel)

    model.load_weights(weights_path)

    return model

def get_model2(weights_path):
    global graph
    graph = tf.get_default_graph()

    model = Sequential()
    model.add(Convolution2D(8, (3, 3), strides=(2, 2), padding='same', activation='relu', input_shape=(224, 224, 3)))
    model.add(MaxPool2D(8, strides=(1, 1), padding='same'))
    model.add(BatchNormalization())
    model.add(Convolution2D(8, (3, 3), strides=(2, 2), padding='same', activation='relu'))
    model.add(MaxPool2D(16, strides=(1, 1), padding='valid'))
    model.add(BatchNormalization())
    model.add(Convolution2D(16, (3, 3), strides=(2, 2), padding='valid', activation='relu'))
    model.add(MaxPool2D(32, strides=(1, 1), padding='same'))
    model.add(BatchNormalization())
    model.add(Convolution2D(32, (3, 3), strides=(2, 2), padding='same', activation='relu'))
    model.add(MaxPool2D(64, strides=(1, 1), padding='same'))
    model.add(BatchNormalization())
    model.add(Convolution2D(64, (3, 3), strides=(1, 1), padding='same', activation='relu'))
    model.add(MaxPool2D(128, strides=(1, 1), padding='same'))
    model.add(Convolution2D(128, (3, 3), strides=(1, 1), padding='same', activation='relu'))
    model.add(GlobalAveragePooling2D())
    model.add(Dense(2, activation='sigmoid'))

    model.load_weights(weights_path)

    return model

