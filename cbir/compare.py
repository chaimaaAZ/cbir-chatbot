import numpy as np
import cv2
import json 
from scipy.spatial import distance

class Compare :
    def __init__(self,indexpath) :
        self.indexpath=indexpath
    # Calculate the Euclidean distance
    def eucledien_distance(self,a,b) :
       distance = distance.euclidean(a,b)
       return distance 
    
    
    def search(self,query_feature) :
        
        with open('index.json', 'r') as file:
          data = json.load(file)
          for dictio in data :
            distance["image"]=0
            for i in range(len(data["image"]["colors"])) :
               distance["image"]+=0.5*self.eucledien_distance(data["colors"][i],query_feature["colors"][i]) 
               distance["image"]+=0.25*self.eucledien_distance(data["texture"][i],query_feature["texture"][i]) 
               distance["image"]+=0.25*self.eucledien_distance(data["shape"][i],query_feature["shape"][i])
        
        similar_images = sorted(distance.items(), key=lambda x: x[1])
        return similar_images[:10]           




                
