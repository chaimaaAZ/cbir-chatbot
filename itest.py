import cv2
import numpy as np
import matplotlib.pyplot as plt
# Load the image
image = cv2.imread('C:\\Users\\Chaimaa\\Documents\\iphone\\pictures\\2022_11_18_19_35_IMG_7632.jpg', cv2.IMREAD_GRAYSCALE)

image =cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
lbp_image = cv2.LBP(image, 8, 1, cv2.LBP_UNIFORM)
        # Calculate the LBP histogram using built-in function
hist = cv2.calcHist([lbp_image], [0], None, [256], [0, 256])
hist = cv2.normalize(hist, hist).flatten()
print(hist.tolist())

