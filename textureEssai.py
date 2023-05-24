import cv2
import numpy as np
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

    return hist

# Chargement de l'image de référence
ref_image = cv2.imread("query_image.jpg")

# Extraire la texture de l'image de référence
ref_texture = extract_texture(ref_image)

# Chemin vers le dossier contenant les images du dataset
dataset_path = "textures/"

# Parcourir toutes les images du dataset
for filename in os.listdir(dataset_path):
    if filename.endswith(".jpg"):
        # Chargement de l'image du dataset
        dataset_image = cv2.imread(os.path.join(dataset_path, filename))

        # Extraire la texture de l'image du dataset
        dataset_texture = extract_texture(dataset_image)

        # Calculer la distance euclidienne entre les deux textures
        distance = np.linalg.norm(ref_texture - dataset_texture)

        # Si la distance est inférieure à un certain seuil, afficher l'image
        if distance < 0.2:
            cv2.imshow("Similar image", dataset_image)
            cv2.waitKey(0)

cv2.destroyAllWindows()
