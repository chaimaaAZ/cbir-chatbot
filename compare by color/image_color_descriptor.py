import cv2
import numpy as np

class descriptor :
    def __init__(self,bins):
      self.bins=bins

    def histogram(self,image,mask):
       image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
       hist=cv2.calcHist([image],[0],mask,self.bins,[0,256])
       #flatten from 2D array to a 1D one 
       hist=cv2.normalize(hist,hist).flatten()
       return hist 
    
    def describe(self,image):
       #segment the image to 5 parts to be more precise 
        features=[]
        #center of image
        (w,h)=image.shape[:2]
        (cx,cy)=(int(w*0.5),int(h*0.5))
        segments=[(0,cx,0,cy),(cx,w,0,cy),(0,cx,cy,h),(cx,w,cy,h)]
        # construct an elliptical mask representing the center of the image
        #(axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
        #mask_ellipse=np.zeros(image.shape[:2],dtype='uint8')
        #cv2.ellipse(mask_ellipse,(cx,cy),(axesX,axesY),0,0,360,255,-1)
        for (startX,startY,endX,endY) in segments :
              
          rectangle_mask=np.zeros(image.shape[:2],dtype='uint8')

          cv2.rectangle(rectangle_mask,(startX,startY),(endX,endY),255,-1)

          #rectangle_mask= cv2.subtract(rectangle_mask,mask_ellipse)

          hist=self.histogram(image,rectangle_mask)
          features.extend(hist)
        #hist=self.histogram(image,mask_ellipse)
        #features.extend(hist)

        return features