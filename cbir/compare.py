import numpy as np
import cv2
import json 
import scipy.spatial.distance as dist

class Compare :
    def __init__(self,indexpath) :
        self.indexpath=indexpath
    # Calculate the Euclidean distance
    def eucledien_distance(self,a,b) :
       distance = dist.euclidean(a,b)
       return distance 
    
    
    def search(self,query_feature) :
        
        with open(self.indexpath, 'r') as file:
          data = json.load(file)
          distance=dict()
          for key in data :
            distance[key]=0
            distance[key]+=0.5*self.eucledien_distance(data[key]["colors"],query_feature["colors"]) 
               
            distance[key]+=0.25*self.eucledien_distance(data[key]["texture"],query_feature["texture"]) 
            distance[key]+=0.25*self.eucledien_distance(data[key]["shape"],query_feature["shape"])
        
        similar_images = sorted(distance.items(), key=lambda x: x[1])
        return similar_images[:10]           




                
