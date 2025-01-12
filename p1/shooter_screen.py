import customtkinter as ctk
from PIL import Image, ImageTk

class ShooterScreen(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.create_widgets()
    def set_background(self, bg_image):
        bg_image = Image.open(bg_image)
        print(bg_image.width, bg_image.height)
        # bg_image = bg_image.resize((int(bg_image.width*0.4), int(bg_image.height*0.4)))
        if(bg_image.width>1400):
            bg_image = bg_image.resize((1024, int(bg_image.height*1024/bg_image.width)))
        if(bg_image.height>900):
            bg_image = bg_image.resize((int(bg_image.width*768/bg_image.height), 768))
        self.bg = bg_image
        bg_img_tk = ImageTk.PhotoImage(bg_image)
        backgroundImage = ctk.CTkLabel(self, image=bg_img_tk, text="")
        backgroundImage.grid(row=0, column=0, sticky="nsew")
    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.set_background(bg_image="assets/watermark_trans.png")