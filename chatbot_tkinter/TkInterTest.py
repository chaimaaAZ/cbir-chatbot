import tkinter as tk
from tkinter import *
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


BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 "


class Chatbot:
    def __init__(self, root):
        self.root = root
        self.root.title('FarahChaimaa ChatBot')
        self._setup_main_window()
    def _setup_main_window(self):
        self.root.resizable(width=False,height=False)
        self.root.configure(width=470,height=750,bg=BG_COLOR)
              
        #head label
        head_label=Label(self.root,bg=BG_COLOR,fg=TEXT_COLOR,
                         text="Welcome to our amazing chatbot",font=FONT_BOLD,pady=10)
        head_label.place(relwidth=1)
        
        #tiny divider
        line=Label(self.root,width=450,bg=BG_COLOR)
        line.place(relwidth=1,rely=0.07,relheight=0.012)
        
        #text widget
        self.text_entry=Text(self.root,width=20,height=2,bg=BG_COLOR,
                              fg=TEXT_COLOR,font=FONT,padx=5,pady=5)
        self.text_entry.place(relheight=0.745,relwidth=1,rely=0.08)
        self.text_entry.configure(cursor="arrow",state=DISABLED)
        
        #scroll bar
        scrollbar=Scrollbar(self.text_entry)
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.configure(command=self.text_entry.yview)
        
        
        # bottom label
        bottom_label = Label(self.root, bg=BG_GRAY, height=100)
        bottom_label.place(relwidth=1, rely=0.825)

        # Add some space at the bottom
        bottom_space = Label(bottom_label, bg=BG_GRAY)
        bottom_space.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)

        # message entry box
        self.msg_entry = Entry(bottom_label, fg=BG_COLOR, font=FONT)
        self.msg_entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.msg_entry.focus()

        # Frame for the right section (30%)
        frame_right = Frame(bottom_label, bg=BG_GRAY)
        frame_right.grid(row=0, column=1, sticky="nsew")

        # sent button "Rechercher"
        send_button1 = Button(frame_right, text="Rechercher", font=FONT_BOLD, width=20, command=self.process_text_query)
        send_button1.grid(row=0, column=0, padx=10,pady=5)

        # sent button "Parler"
        send_button2 = Button(frame_right, text="Parler", font=FONT_BOLD, width=20, bg=TEXT_COLOR, command=self.process_voice_query)
        send_button2.grid(row=1, column=0, padx=10,pady=5)
        
        # bouton de sélection du dataset
        select_dataset_button = Button(frame_right, text="Sélectionner le dataset", font=FONT_BOLD, width=20, command=self.select_dataset)
        select_dataset_button.grid(row=2, column=0, padx=10, pady=5)

    def select_dataset(self):
        dataset_path = filedialog.askdirectory()
        # Effectuez ici les opérations nécessaires avec le chemin du dataset sélectionné
        print("Dataset sélectionné :", dataset_path)

   
    def process_text_query(self):
        query = self.msg_entry.get()

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







    