import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras.applications import EfficientNetB7
from keras.callbacks import ReduceLROnPlateau
from keras.models import load_model
from keras.utils import image_dataset_from_directory
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.utils import img_to_array
import tensorflow as tf
from sklearn.metrics import confusion_matrix,accuracy_score, classification_report
import keras
import pickle

def load_models():
    stage_one = load_model('stage_one.h5')
    with open('models.pkl', 'rb') as f:
        stage_two = pickle.load(f)
    
    print("models loaded")

    return stage_one, stage_two

def results(path):
    stage_one, stage_two = load_models()
    img = image.load_img(path)
    print('image loaded')
    input_arr = np.array([img_to_array(img)])
    
    stage_one_preds = stage_one_pred(stage_one, input_arr)
    print(stage_one_preds)

    stage_two_preds = stage_two_pred(stage_two[stage_one_preds], input_arr, stage_one_preds)
    print(stage_two_preds)

    return stage_one_preds+" "+stage_two_preds

def stage_one_pred(model, input_arr):
    classes = ['apple','blueberry','cherry','corn','grape','orange','peach','pepper_bell','potato','raspberry','soybean','squash','strawberry','tomato']
    pred = model.predict(input_arr)
    # print(plant,disease)
    idx = np.argmax(pred)
    predicted_class = classes[idx]
    print(predicted_class)
    return predicted_class

def stage_two_pred(model, input_arr, plant):
    classes = {
        "apple": ["Scab",'Black Rot','Cedar Apple Rust','Healthy'],
        "blueberry":["Healthy"],
        "cherry":['Healthy','Powdery Mildew'],
        "corn":['Cercospora leaf','Common rust','Healthy','Northern Leaf Blight'],
        "grape":['Black Rot','Healthy','Leaf Blight'],
        "orange":['Citrus Greening'],
        "peach":['Bacterial_spot','Healthy'],
        "pepper_bell": ['Bacterial_spot','Healthy'],
        "potato":['Early Blight','Healthy','Late Blight'],
        "raspberry":['Healthy'],
        "soybean":['Healthy'],
        "squash":['Powdery Mildew'],
        "strawberry":['Healthy','Leaf Scorch'],
        "tomato":['Bacterial_spot','Early Blight','healthy','Late Blight','Leaf Mold','Septoria Leaf Spot','Spider mites','Target Spot','Mosaic Virus','Yellow Leaf Curl Virus']
    }
    pred = model.predict(input_arr)
    # print(plant,disease)
    idx = np.argmax(pred)
    predicted_class = classes[plant][idx]
    print(predicted_class)
    return predicted_class

if __name__ == "__main__":
    path = "data/valid/stage_two/corn/Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot/0a01cc10-3892-4311-9c48-0ac6ab3c7c43___RS_GLSp 9352_new30degFlipLR.JPG"
    print(results(path))