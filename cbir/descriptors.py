import cv2
import numpy as np
class descriptor:
    def __init__(self,bins):
      self.bins=bins
    #color histogram
    def histogram_hsv(self,image) :
          image =cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
          hist =cv2.calcHist([image],[0,1,2],None,self.bins,[0,256]*3)
          hist=cv2.normalize(hist,hist).flatten()
          return hist.tolist()
    #texture histogram
    def histogram_lbp(self,image) :
        image =cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        lbp_image = cv2.LBP(image, 8, 1, cv2.LBP_UNIFORM)
        # Calculate the LBP histogram using built-in function
        hist = cv2.calcHist([lbp_image], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist.tolist()
    #shape histogram
    def histogram_sobel(self,image):
        # Apply the Sobel operator
         sobel = cv2.Sobel(image, cv2.CV_8UC1, 1, 0, ksize=3)
         hist, _ = np.histogram(sobel, density=True, bins=10, range=(0, 10))
         hist = cv2.normalize(hist, dst=hist.shape)
         hist = cv2.normalize(hist, hist).flatten()
         return hist.tolist()
    
    def describe(self,image,method):
          features=[]
          if(method=="histogram_hsv") :
              hist=self.histogram_hsv(image)
          elif(method=="histogram_lbp") :
              hist=self.histogram_hsv(image)
          elif(method=="histogram_sobel") :
              hist=self.histogram_sobel(image)
          
          features.extend(hist)
          return features
    
