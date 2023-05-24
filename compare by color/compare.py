import numpy as np
import cv2
import csv
import math

class Compare :
    def __init__(self,indexpath):
        self.indexpath=indexpath
    def chi2_distance(self, histA, histB, eps = 1e-10):
        d=0.5*np.sum([((a-b)**2)/(a+b+eps) for (a,b) in zip(histA,histB)])
        return d 
    
    def eucledien_distance(self,histA,histB) :
        d=np.sqrt(np.sum([((a - b) ** 2) for (a,b) in zip(histA,histB)]))
        return d
    def search(self,query_feature) :
        image_distance={}
        with open(self.indexpath) as f:
            reader=csv.reader(f)
            for row in reader :
                features=[float(x) for x in row[1:]]
                distance=self.eucledien_distance(features,query_feature) 
                image_distance[row[0]]=distance
            f.close()
        image_distance=sorted([(v,k) for (k,v) in image_distance.items()])
        return image_distance[:10]
                      
        

        