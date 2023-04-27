import numpy as np
import cv2
import glob
from image_color_descriptor import descriptor

def index(bins):

    d=descriptor(bins)

    #open the output index file for writing
    dataset=r'C:\Users\Chaimaa\Documents\iphone\pictures'
    index='index2.csv'

    file=open(index,"w")

    for image in glob.glob(dataset+"/*.jpg") :
        #load image
        img=cv2.imread(image)
        #describe the image 
        features = d.describe(img)
        features=[str(f) for f in features]
        file.write("%s,%s\n" % (image,",".join(features)))
    file.close()

    
