import tkinter as tk
from tkinter import *
from tkinter import ttk 
from tkinter import filedialog
import speech_recognition as sr

from chat import get_response,bot_name
from search import search
from PIL import Image, ImageTk
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
         # Create a Canvas widget for displaying images
        #self.image_canvas = tk.Canvas(self.root, width=200, height=200, bg=BG_COLOR)
        #self.image_canvas.place( anchor='center')
        #self.image_canvas.configure(state=DISABLED)
        
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
        
        # sent button "search"
        send_button2 = Button(frame_right, text="search image", activebackground='black',font=FONT_BOLD, width=20, command=self.process_image_query)
        send_button2.grid(row=1, column=0, padx=10,pady=5)

        # sent button "speak"
        send_button3 = Button(frame_right, text="speak", activebackground='black',font=FONT_BOLD, width=20, bg=TEXT_COLOR, command=self.process_voice_query)
        send_button3.grid(row=2, column=0, padx=10,pady=5)
        
        # bouton de sélection du dataset
        select_dataset_button = Button(frame_right,activebackground='black', text="Select dataset", font=FONT_BOLD, width=20, command=self.select_dataset)
        select_dataset_button.grid(row=3, column=0, padx=10, pady=5)

        
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
        
        #go to end of scrollbar 
        self.text_entry.see(END)

    
    def select_dataset(self):
        dataset_path = filedialog.askdirectory()
        #les opérations nécessaires avec le chemin du dataset sélectionné
        # inform the user this could take a while 
       
        #Index dataset 
        index(dataset_path,(4,4,4))
        # end of indexation message
        self.text_entry.configure(state=NORMAL)
        self.text_entry.insert(END,"Indexation complete!!!!")
        self.text_entry.configure(state=DISABLED)
        


   
    def process_image_query(self):
        query = self.msg_entry.get()

       
        self.query_image_path = filedialog.askopenfilename()
        results = search(self.query_image_path)
        self.show_images3(results) 
    
    

    def show_images3(self,images) :
        new_frame = tk.Toplevel(self.root)  # Create a new top-level window
        # Add widgets and configure the new frame
        for (i, resultID) in enumerate(images):
              # load the result image and display it
                result = Image.open(resultID[0])
                result = result.resize((210, 210), Image.Resampling.LANCZOS)
                result = ImageTk.PhotoImage(result)
                result_preview = ttk.Label(new_frame, image=result)
                result_preview.image = result
                result_preview.grid(row=i//5, column=i%5, sticky="s", padx=10, pady=20)
                
 

        




    def process_voice_query(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print('Say something:')
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio, language='en-US')
                self._insert_message(text,"you")
                print(text)
               
            except:
                print('ERROR')


    
    

   
if __name__ == "__main__":
    root = tk.Tk()
    app = Chatbot(root)
    root.mainloop()







    