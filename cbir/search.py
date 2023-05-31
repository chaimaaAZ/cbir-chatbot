import numpy as np
import cv2
from compare import Compare
from descriptors import descriptor


def search(image): 
    d=descriptor((4,4,4))


    
    query=cv2.imread(image)
    query=cv2.resize(query,(300,400))
    #perform the search
    features = dict()
    features["colors"] = d.describe(query,"histogram_hsv")
    features["texture"] = d.describe(query,"histogram_lbp")
    features["shape"] = d.describe(query,"histogram_sobel")
    searcher= Compare('index.json')

    results=searcher.search(features)

    

    cv2.imshow("query",query)

    for (result_image,score) in results :
        #load the result images and display them
        result=cv2.imread(result_image)
        result=cv2.resize(result,(300,400))
        cv2.imshow("result",result)
        cv2.waitKey(0)

