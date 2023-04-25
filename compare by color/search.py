import numpy as np
import cv2
from compare import Compare
from image_color_descriptor import descriptor

#cd=descriptor((4,4,4))
cd=descriptor([10])

image ='C:\\Users\\Chaimaa\\Documents\\iphone\\pictures\\2022_06_28_14_59_IMG_3199.jpg'
query=cv2.imread(image)
query=cv2.resize(query,(300,400))
#perform the search
features =cd.describe(query)
searcher= Compare('index2.csv')

results=searcher.search(features)

cv2.imshow("query",query)

for (score,result_image) in results :
    #load the result images and display them
    
    result=cv2.imread(result_image)
    result=cv2.resize(result,(300,400))
    cv2.imshow("result",result)
    cv2.waitKey(0)