import cv2
import csv
import numpy as np
import glob
import os

# Fonction pour extraire la texture d'une image
def extract_texture(image):
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculer le gradient horizontal et vertical
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)

    # Calculer la magnitude et la direction du gradient
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    direction = np.arctan2(sobely, sobelx)

    # Diviser la direction du gradient en 8 bins
    bins = np.int32(direction/(np.pi/4)) % 8

    # Calculer l'histogramme des magnitudes pour chaque bin
    hist = np.zeros(8)
    for i in range(8):
        hist[i] = np.sum(magnitude[bins==i])

    # Normaliser l'histogramme
    hist /= np.sum(hist)

    return hist.flatten()

def describe(image):
    features=[]
    
    features.extend(extract_texture(image))
    return features 


def index():

    #open the output index file for writing
    dataset=r'C:\Users\Chaimaa\Documents\iphone\pictures'
    index='index_texture.csv'

    file=open(index,"w")

    for image in glob.glob(dataset+"/*.jpg") :
        #load image
        img=cv2.imread(image)
        #describe the image 
        features = describe(img)
        features=[str(f) for f in features]
        file.write("%s,%s\n" % (image,",".join(features)))
    file.close()


def eucledien_distance(self,histA,histB) :
        d=np.sqrt(np.sum([((a - b) ** 2) for (a,b) in zip(histA,histB)]))
        return d
def compare(indexpath,queryfeature):
     
        image_distance={}
        with open(indexpath) as f:
            reader=csv.reader(f)
            for row in reader :
                features=[float(x) for x in row[1:]]
                distance=eucledien_distance(features,queryfeature) 
                image_distance[row[0]]=distance
            f.close()
        image_distance=sorted([(v,k) for (k,v) in image_distance.items()])
        return image_distance[:10]



#index()
image ='C:\\Users\\Chaimaa\\Documents\\iphone\\pictures\\2022_11_18_19_35_IMG_7632.jpg'
query=cv2.imread(image)
query=cv2.resize(query,(300,400))
#perform the search
features =describe(query)
results= compare('index_texture.csv',features)


cv2.imshow("query",query)

for (score,result_image) in results :
    #load the result images and display them
    
    result=cv2.imread(result_image)
    result=cv2.resize(result,(300,400))
    cv2.imshow("result",result)
    cv2.waitKey(0)