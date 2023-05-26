import numpy as np
import cv2
import glob
from descriptors import descriptor
import json


def index(bins):

    d=descriptor(bins)

    #open the output index file for writing
    dataset=r'C:\Users\Chaimaa\Documents\iphone\pictures'
    index='index.json'

   
    database_features=dict()
    for image in glob.glob(dataset+"/*.jpg") :
            #load image
            img=cv2.imread(image)
            all_features=dict()
            all_features["index"]=image
            #describe the image 
            #color hisrogram
            colors = d.describe(img,"histogram_hsv")
            all_features['colors']=colors
            #texture histogram
            texture = d.describe(img,"histogram_lbp")
            all_features['texture']=texture
            #shape histogram
            shape = d.describe(img,"histogram_sobel")
            all_features['shape']=shape
            database_features[image]=all_features

    with open("index.json", "w") as f:
     json.dump(database_features, f)
    
index((4,4,4))
