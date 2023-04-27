import numpy as np
import cv2
from compare import Compare
from index import index
from image_color_descriptor import descriptor

#just to try the commit 
method='histogram_hsv'

if  method=='histogram_hsv' or method=='histogram_lab' :
  bins=(4,4,4)
elif method=='histogram_gray_scale' :
  bins=[10]

index(bins)

d=descriptor(bins)
#d=descriptor([10])

image ='C:\\Users\\Chaimaa\\Documents\\iphone\\pictures\\2022_06_05_12_27_IMG_2561.jpg'
query=cv2.imread(image)
query=cv2.resize(query,(300,400))
#perform the search
features =d.describe(query)
searcher= Compare('index2.csv')

results=searcher.search(features)

cv2.imshow("query",query)

for (score,result_image) in results :
    #load the result images and display them
    
    result=cv2.imread(result_image)
    result=cv2.resize(result,(300,400))
    cv2.imshow("result",result)
    cv2.waitKey(0)