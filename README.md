# image search assistant 
A ChatBot capable of taking audio or text input and chat with user , it is also responsible for searching similar images from dataset based on **color , shape and texture**. 
## CBIR
CBIR stands for Content-Based Image Retrieval. It is a technique used in computer vision and image processing to retrieve images from a database based on their visual content.

The traditional approach to image retrieval relies on textual metadata associated with images, such as tags or descriptions. However, CBIR focuses on extracting visual features from images, such as color, texture, shape, or spatial arrangements, and using these features to search and retrieve similar images.
## Feature extraction 
The features of each image in dataset are extracted and stored in the ```index.json``` file based on the following features :
#### Color : 
* HSV: Hue, Saturation, Value.
#### Texture :
* LBP: Local Binary Pattern.
#### Sobel : 
* SOBEL: Sobel operator.
## Query :
The query image is the specific image we wish to find or search for within the image database. Similar to the database images, the query image undergoes the same feature extraction methods to capture its visual characteristics.
Once the features are extracted from the query image, a comparison is made between the query image and the images in the database. This comparison involves calculating the **eucledien distance**  indicating how closely the query matches each image in the dataset .The images are then sorted  and the images with the **10** lowest distance are returned as the result of the search.

## Instructions :
1. clone the repository to your machine :
```bash 
https://github.com/chaimaaAZ/cbir-chatbot.git
```
2. Install required libraries :
```bash 
pip install -r requirements.txt
```
3. Change the images in the database folder ```database``` with your own images if needed.
4.  Run the indexation script, this will extract the features of the images in the database and store them in a JSON file ```index.json```
```bash
python index.py
```
5. install nltk.tokenize.punkt: Run this once in your terminal :
```
$ python
>>> import nltk
>>> nltk.download('punkt')
```
6. Run the training script :
```bash
python train.py
```
7. Run the main script, that will open the GUI and you can load the query image and search for similar images in the database.
```bash
python main.py
```
## Exemple :
