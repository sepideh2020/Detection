
# coding: utf-8

# In[2]:


#dependencies
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from keras.utils import np_utils
from keras.models import Sequential, Model, model_from_json
from keras.layers import Conv2D, Activation, MaxPool2D, Dropout, Dense, BatchNormalization, Flatten
from keras.callbacks import ModelCheckpoint
import tarfile
from PIL import Image


# In[3]:


from keras.models import model_from_json
import numpy as np
import tensorflow as tf


class FacialExpressionModel(object):
    EMOTIONS_LIST = ["Angry", "Disgust/fear/surprise","Sad","Happy", "Neutral"]

    def __init__(self, model_json_file, model_weights_file):


        print('initialization')


        self.graph = tf.get_default_graph()


        self.face_detecor = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')

        # load model from JSON file
        with open(model_json_file, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)

        # load weights into the new model
        self.loaded_model.load_weights(model_weights_file)
        print("Model loaded from disk")
        self.loaded_model.summary()

    def predict_emotion(self, img):
        with self.graph.as_default():
            self.preds = self.loaded_model.predict(img)

        return FacialExpressionModel.EMOTIONS_LIST[np.argmax(self.preds)]

    def predict_all_faces_emotion(self, img):
        faces = self.detect_faces(img)
        result = []
        for (x, y, w, h) in faces:
            fc = img[y:y + h, x:x + w]

            roi = cv2.resize(fc, (48, 48))
            pred = self.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
            result.append(pred)
        return result

    def detect_faces(self, image):
        return self.face_detecor.detectMultiScale(image, 1.3, 5)


if __name__ == '__main__':
    pass


# In[4]:


import cv2


#get and image and detect emotion
def detect_emotion_image(image):

    # Load an color image in grayscale
    model = FacialExpressionModel("./models/model1.json", "./models/chkPt1.h5")
    #image = image.convert('LA')

    faces = model.detect_faces(image)
    result = []
    for (x, y, w, h) in faces:
            fc = image[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
            result.append( pred)
    return result
    
if __name__ == "__main__":
    img = cv2.imread('sad.jpg')
    #cv2.imshow('tt', img)
    #cv2.waitKey(2000)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    #img = Image.open('sad.jpg')
    emotion = detect_emotion_image(img)
    print(emotion)


