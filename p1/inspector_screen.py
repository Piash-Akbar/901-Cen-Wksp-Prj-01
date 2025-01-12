import customtkinter as ctk
from PIL import Image, ImageTk
import Config

class InspectorScreen(ctk.CTkFrame):
    def __init__(self, master=None, onclick=None, **kw):
        super().__init__(master, **kw)
        self.create_widgets(onclick)
    

    def set_background(self, bg_image):
        bg_image = Image.open(bg_image)
        print(bg_image.width, bg_image.height)
        # bg_image = bg_image.resize((int(bg_image.width*0.4), int(bg_image.height*0.4)))
        if(bg_image.width>1024):
            bg_image = bg_image.resize((1024, int(bg_image.height*1024/bg_image.width)))
        if(bg_image.height>708):
            bg_image = bg_image.resize((int(bg_image.width*708/bg_image.height), 708))
        self.bg = bg_image
        bg_img_tk = ImageTk.PhotoImage(bg_image)
        backgroundImage = ctk.CTkLabel(self, image=bg_img_tk, text="")
        backgroundImage.grid(row=0, column=0, sticky="nsew")
    def buttonTextChange(self, text):
        self.start_button.configure(text=text)
    def create_widgets(self, onclick):
        self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.set_background(bg_image="assets/watermark_trans.png")

        self.start_button = ctk.CTkButton(self, text="Calculate", font=("Arial", 19), text_color=Config.text_color, command=onclick)
        self.start_button.grid(row=1, column=0, padx=20, pady=5, sticky="EW")