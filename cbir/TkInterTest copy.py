import tkinter as tk
from tkinter import *
from tkinter import ttk 
from tkinter import filedialog
import speech_recognition as sr
from PIL import ImageTk, Image

from chat import get_response,bot_name
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
        self.root.title('image search assistant  ChatBot')
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
                              fg=TEXT_COLOR,font=FONT,padx=5,pady=5,wrap=WORD)
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
        self.msg_entry.bind("<Return>",self._on_enter_pressed)

        # Frame for the right section (30%)
        frame_right = Frame(bottom_label, bg=BG_GRAY)
        frame_right.grid(row=0, column=1, sticky="nsew")
        
        #chat button
        send_button1 = Button(frame_right, text="Chat", activebackground='black',font=FONT_BOLD, width=20, command=lambda : self._on_enter_pressed(None))
        send_button1.grid(row=0, column=0, padx=10,pady=5)
        
        # sent button "Rechercher"
        send_button2 = Button(frame_right, text="search image", activebackground='black',font=FONT_BOLD, width=20, command=self.process_image_query)
        send_button2.grid(row=1, column=0, padx=10,pady=5)

        # sent button "Parler"
        send_button3 = Button(frame_right, text="speak", activebackground='black',font=FONT_BOLD, width=20, bg=TEXT_COLOR, command=self.process_voice_query)
        send_button3.grid(row=2, column=0, padx=10,pady=5)
        
        # bouton de sélection du dataset
        select_dataset_button = Button(frame_right,activebackground='black', text="Sélectionner votre dataset", font=FONT_BOLD, width=20, command=self.select_dataset)
        #select_dataset_button.grid(row=3, column=0, padx=10, pady=5)

        
    #write message sent by user to gui    
    def _on_enter_pressed(self,event) :
        msg=self.msg_entry.get()
        self._insert_message(msg,"you")
    
    def _insert_message(self,msg,sender) :
        if not msg:
            return 
        self.msg_entry.delete(0,END)
        msg1=f"{sender}:{msg}\n\n"
        self.text_entry.configure(state=NORMAL)
        self.text_entry.insert(END,msg1)
        self.text_entry.configure(state=DISABLED)

        #responce from bot 
        msg2=f"{bot_name}:{get_response(msg)}\n\n"
        self.text_entry.configure(state=NORMAL)
        self.text_entry.insert(END,msg2)
        self.text_entry.configure(state=DISABLED)

        self.text_entry.see(END)
    
    def show_images(self,images) :
        for image,_ in images :
            # display an image label
            image = Image.open(image)
            image = image.resize((100, 100))
            photo=ImageTk.PhotoImage(image)
            self.text_entry.image_create(tk.END, image=photo)
            self.text_entry.image = photo

        self.text_entry.see(END)
            

        



    def select_dataset(self):
        dataset_path = filedialog.askdirectory()
        #les opérations nécessaires avec le chemin du dataset sélectionné
        print("Dataset sélectionné :", dataset_path)
        index(dataset_path,(4,4,4))
        


   
    def process_image_query(self):
        query = self.msg_entry.get()

       
        self.query_image_path = filedialog.askopenfilename()
        results = search(self.query_image_path)
        self.show_images(results) 

    def process_voice_query(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print('Parlez :')
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio, language='en-US')
                self._insert_message(text,"you")
               
            except:
                print('ERROR')


    
    

   
if __name__ == "__main__":
    root = tk.Tk()
    app = Chatbot(root)
    root.mainloop()







    