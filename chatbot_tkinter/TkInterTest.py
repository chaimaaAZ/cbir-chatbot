import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
from gtts import gTTS
import os
import cv2
import numpy as np
import glob
import playsound
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math


class Chatbot:
    def __init__(self, root):
        self.root = root
        self.root.title('FarahChaimaa ChatBot')

        self.query_image_path = ""

        self.text_entry = tk.Entry(self.root, width=50)
        self.text_entry.pack()

        self.submit_button = tk.Button(self.root, text='Envoyer', command=self.process_text_query)
        self.submit_button.pack()

        self.voice_button = tk.Button(self.root, text='Parler', command=self.process_voice_query)
        self.voice_button.pack()

    def process_text_query(self):
        query = self.text_entry.get()

        if 'recherche d\'image' in query:
            self.query_image_path = filedialog.askopenfilename()
            self.search_image(self.query_image_path)

    def process_voice_query(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print('Speak Anything :')
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                print('You said : {}'.format(text))

                if 'recherche d\'image' in text:
                    self.query_image_path = filedialog.askopenfilename()
                    self.search_image(self.query_image_path)

            except:
                print('Sorry could not recognize your voice')

    def calculate_histogram(self, image_path):
        image = cv2.imread(image_path)
        histogram = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        histogram = cv2.normalize(histogram, histogram)
        return histogram

    def compare_histograms(self, histogram1, histogram2):
        return cv2.compareHist(histogram1, histogram2, cv2.HISTCMP_CORREL)
    
    
    def search_image(self, query_image_path):
        DATASET_PATH = 'database/'

        query_histogram = self.calculate_histogram(query_image_path)

        images_path = glob.glob(f'{DATASET_PATH}/*.jpg')

        results = []
        images = []
        for image_path in images_path:
            image_histogram = self.calculate_histogram(image_path)
            similarity = self.compare_histograms(query_histogram, image_histogram)
            if similarity > 0.9:
                results.append(image_path)
                images.append(mpimg.imread(image_path))

        print(f'Found {len(results)} similar images.')
        self.display_images(images)

        if len(results) == 0:
            print("No similar images found.")
            tts = gTTS(text=f"No similar images found.", lang='en')
            filename = "voice.mp3"
            tts.save(filename)
            playsound.playsound(filename, True)
            os.remove(filename)

        if len(results) > 0:
            tts = gTTS(text=f"{len(results)} similar images found.", lang='en')
            filename = "voice.mp3"
            tts.save(filename)
            playsound.playsound(filename, True)
            os.remove(filename)


    def display_images(self, images):
        sqrt = math.sqrt(len(images))
        if sqrt == int(sqrt):
            rows = cols = int(sqrt)
        else:
            rows = int(sqrt) + 1
            cols = int(sqrt)

        fig, axs = plt.subplots(rows, cols)
        for i, img in enumerate(images):
            ax = axs[i // cols, i % cols]
            ax.imshow(img)
            ax.axis('off')
        plt.show()


   
if __name__ == "__main__":
    root = tk.Tk()
    app = Chatbot(root)
    root.mainloop()







    