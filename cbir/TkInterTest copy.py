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
import random
from search import search

from index import index 

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 "


class Chatbot:
    def __init__(self, root):
        self.root = root
        self.root.title('search assistant  ChatBot')
        self._setup_main_window()
            
    def _setup_main_window(self):
        self.root.resizable(width=False,height=False)
        self.root.configure(width=450,height=750,bg=BG_COLOR)
              
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
        scrollbar.place(relheight=0.9,relx=0.974)
        scrollbar.configure(command=self.text_entry.yview)
        
        
        # bottom label
        bottom_label = Label(self.root, bg=BG_GRAY, height=200)
        bottom_label.place(relwidth=1, rely=0.75)

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
        
        #chat button
        send_button1 = Button(frame_right, text="Chat", activebackground='black',font=FONT_BOLD, width=20, command=self.process_text_query)
        send_button1.grid(row=0, column=0, padx=10,pady=5)
        
        # sent button "Rechercher"
        send_button1 = Button(frame_right, text="Rechercher", activebackground='black',font=FONT_BOLD, width=20, command=self.process_text_query)
        send_button1.grid(row=1, column=0, padx=10,pady=5)

        # sent button "Parler"
        send_button2 = Button(frame_right, text="Parler", activebackground='black',font=FONT_BOLD, width=20, bg=TEXT_COLOR, command=self.process_voice_query)
        send_button2.grid(row=2, column=0, padx=10,pady=5)
        
        # bouton de sélection du dataset
        select_dataset_button = Button(frame_right,activebackground='black', text="Sélectionner votre dataset", font=FONT_BOLD, width=20, command=self.select_dataset)
        select_dataset_button.grid(row=3, column=0, padx=10, pady=5)

        
        
       
        
    def select_dataset(self):
        dataset_path = filedialog.askdirectory()
        #les opérations nécessaires avec le chemin du dataset sélectionné
        print("Dataset sélectionné :", dataset_path)
        index(dataset_path,(4,4,4))
        


   
    def process_text_query(self):
        query = self.msg_entry.get()

        if 'recherche d\'image' in query:
            self.query_image_path = filedialog.askopenfilename()
            search(self.query_image_path)

    def process_voice_query(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print('Parlez :')
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio, language='fr-FR')
                print('Vous avez dit : {}'.format(text))
                if 'recherche d\'image' in text:
                    self.query_image_path = filedialog.askopenfilename()
                    self.search_image(self.query_image_path)

            except:
                print('Désolé, je n\'ai pas pu reconnaître votre voix')


    
    

   
if __name__ == "__main__":
    root = tk.Tk()
    app = Chatbot(root)
    root.mainloop()







    