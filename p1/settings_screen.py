import customtkinter as ctk
from PIL import Image, ImageTk
import Config
from functools import partial
import threading
from time import sleep
base_path = "assets/bg/"
def validate_number(char):
  if char.isdigit():
    return char
  return ""

class SettingsWindow(ctk.CTkFrame):
    bg_path = "assets/bg/grouping shooting 25m.jpg"

    def print_position_and_size(self, label):
      self.update()  # Make sure to update the root window to get the latest values
      x_offset = self.backgroundImage.winfo_x()
      y_offset = self.backgroundImage.winfo_y()

      x = label.winfo_x()
      y = label.winfo_y()
      width = label.winfo_width()
      height = label.winfo_height()
      cropBox = (x-x_offset, y-y_offset, x-x_offset+width, y-y_offset+height)
      crop = self.bg.crop(cropBox)
      imgTk = ImageTk.PhotoImage(crop)
      label.configure(image=imgTk)
      label.image = imgTk
      

    def threaded_function(self, label):
        sleep(0.5)
        self.print_position_and_size(label)
  
    def start_thread(self, label):
      thread = threading.Thread(target=partial(self.threaded_function, label=label))
      thread.start()
    def combobox_callback(self,choice, field):
        global bg_path
        print("combobox dropdown clicked:", choice, field)
        if field == "type_of_target":
           SettingsWindow.bg_path = base_path+f"{choice.lower()} shooting 25m.jpg"
           img = Image.open(f"assets/{choice}.png")
           img = img.resize((int(img.width*0.7), int(img.height*0.7)))
           img_tk = ImageTk.PhotoImage(img)
           self.img_label.configure(image=img_tk)
          #  self.img_label._image = img_tk

    def create_dd(self,field, options):
        selected_option = ctk.StringVar()
        selected_option.set(options[0])
        
        return ctk.CTkComboBox(
            self, 
            values=options, 
            variable=selected_option,
            fg_color=Config.dd_bg_color,
            border_color=Config.dd_bg_color,
            text_color="#000",
            font=ctk.CTkFont("Arial", 19),
            button_color=Config.dd_bg_color,
            button_hover_color=Config.dd_bg_hover_color,
            state="readonly",
            dropdown_font= ctk.CTkFont("Arial",19),
            command=partial(self.combobox_callback, field=field)
            )
    def onlyNumber(self, P):
      if str.isdigit(P) or P == "":
          return True
      else:
          return False
    
    def getImgTk(self, path, w = 60, h = 60):
      img = Image.open(path)
      img = img.resize((w, h))
      return ctk.CTkLabel(self, image=ImageTk.PhotoImage(img), text="")
    
    def __init__(self, master=None, onclick=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=Config.bg_color)

        # # Load the background image
        bg_image = Image.open("assets/watermark_trans.png")
        bg_image = bg_image.resize((int(bg_image.width*0.37), int(bg_image.height*0.37)))
        self.bg = bg_image
        bg_img_tk = ImageTk.PhotoImage(bg_image)

        # # self.bg_image = self.bg_image.resize((300, 200), Image.ANTIALIAS)
        # self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        
        # # Create a canvas to display the background image
        # self.canvas = ctk.CTkCanvas(self)
        # self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        # self.canvas.grid(row=0, column=0, rowspan=1, columnspan=4, sticky="EW")
        
        # Configure grid layout
        for i in range(6): 
          self.grid_columnconfigure(i, weight=1)
        backgroundImage = ctk.CTkLabel(self, image=bg_img_tk, text="")
        backgroundImage.grid(row=1, column=0, rowspan=9, columnspan=6, padx=20, pady=Config.pady, sticky="SN")
        self.backgroundImage = backgroundImage

        # left logo
        self.getImgTk("assets/eme.png").grid(row=0, column=0, padx=20, pady=5, sticky="w")
        # Center text
        center_label = ctk.CTkLabel(self, text="Container-Based Tubular Target Firing Simulator", font=ctk.CTkFont("Bernard MT Condensed",30,"bold"),text_color=Config.text_color)
        center_label.grid(row=0, column=0, columnspan=6, padx=20, pady=5)
        # right logo
        self.getImgTk("assets/log.png").grid(row=0, column=5, padx=20, pady=5,sticky="e")
        
        # Setup
        setup_label = ctk.CTkLabel(self, text="Setup", font=ctk.CTkFont("Bookman Old Style",30,"bold"),text_color=Config.text_color, bg_color="transparent")
        setup_label.grid(row=1, column=0, columnspan=6, padx=20, pady=0)

        # Exercise
        exercise_label = ctk.CTkLabel(self, text="Exercise", font=("Arial", 19),text_color=Config.text_color)
        exercise_label.grid(row=2, column=0, padx=20, pady=Config.pady, sticky="w")
        
        exercise_dropdown = self.create_dd(field="Exercise",options=Config.exercise_options)
        exercise_dropdown.grid(row=2, column=1, padx=20, pady=Config.pady,sticky="EW")

        # Type of target
        type_of_target_label = ctk.CTkLabel(self, text="Type of target", font=("Arial", 19),text_color=Config.text_color)
        type_of_target_label.grid(row=2, column=3, padx=20, pady=Config.pady, sticky="w")
        
        type_of_target_dropdown = self.create_dd(field="type_of_target",options=Config.type_of_target_options)
        type_of_target_dropdown.grid(row=2, column=4,columnspan=2, padx=20, pady=Config.pady,sticky="EW")

        # Weapon
        weapon_label = ctk.CTkLabel(self, text="Weapon", font=("Arial", 19),text_color=Config.text_color)
        weapon_label.grid(row=3, column=0, padx=20, pady=Config.pady, sticky="w")
        
        weapon_dropdown = self.create_dd(field="weapon",options=Config.weapon_options)
        weapon_dropdown.grid(row=3, column=1, columnspan=2, padx=20, pady=Config.pady,sticky="EW")

        # Type of practice
        type_of_practice_label = ctk.CTkLabel(self, text="Type of practice", font=("Arial", 19),text_color=Config.text_color, bg_color="transparent")
        type_of_practice_label.grid(row=3, column=3, padx=20, pady=Config.pady, sticky="w")

        type_of_practice_dropdown = self.create_dd(field="type_of_practice",options=Config.type_of_practice_options)
        type_of_practice_dropdown.grid(row=3, column=4, columnspan=2, padx=20, pady=Config.pady,sticky="EW")

        # Type of fire
        type_of_fire_label = ctk.CTkLabel(self, text="Type of fire", font=("Arial", 19),text_color=Config.text_color)
        type_of_fire_label.grid(row=4, column=0, padx=20, pady=Config.pady, sticky="w")

        type_of_fire_dropdown = self.create_dd(field="type_of_fire",options=Config.type_of_fire_options)
        type_of_fire_dropdown.grid(row=4, column=1, columnspan=2, padx=20, pady=Config.pady,sticky="EW")

        # Time (sec)
        time_label = ctk.CTkLabel(self, text="Time (sec)", font=("Arial", 19),text_color=Config.text_color)
        time_label.grid(row=4, column=3, padx=20, pady=Config.pady, sticky="w")

        time_entry = self.create_dd(field="time_sec", options=Config.time_sec_options)
        time_entry.grid(row=4, column=4, padx=20, pady=Config.pady,sticky="EW")

        # Range (mts)
        range_label = ctk.CTkLabel(self, text="Range (mts)", font=("Arial", 19),text_color=Config.text_color)
        range_label.grid(row=5, column=0, padx=20, pady=Config.pady, sticky="w")

        range_dropdown = self.create_dd(field="range", options=Config.range_options)
        range_dropdown.grid(row=5, column=1, padx=20, pady=Config.pady,sticky="EW")

        # Name of practice
        name_of_practice_label = ctk.CTkLabel(self, text="Name of practice", font=("Arial", 19),text_color=Config.text_color)
        name_of_practice_label.grid(row=6, column=0, padx=20, pady=Config.pady, sticky="w")

        name_of_practice_entry = ctk.CTkEntry(self, font=("Arial", 19),text_color="#000", fg_color=Config.dd_bg_color, border_color=Config.dd_bg_color)
        name_of_practice_entry.grid(row=6, column=1, columnspan=2, padx=20, pady=Config.pady,sticky="EW")

        # Exposures
        exposures_label = ctk.CTkLabel(self, text="Exposures", font=("Arial", 19),text_color=Config.text_color)
        exposures_label.grid(row=6, column=3, padx=20, pady=Config.pady, sticky="w")

        exposures_dropdown = self.create_dd(field="exposures", options=Config.exposures_options)
        exposures_dropdown.grid(row=6, column=4, padx=20, pady=Config.pady,sticky="EW")
        
        # Rounds allotted
        rounds_allotted_label = ctk.CTkLabel(self, text="Rounds allotted", font=("Arial", 19),text_color=Config.text_color)
        rounds_allotted_label.grid(row=7, column=0, padx=20, pady=Config.pady, sticky="w")

        rounds_allotted_dropdown = self.create_dd(field="rounds_allotted", options=Config.rounds_allotted_options)
        rounds_allotted_dropdown.grid(row=7, column=1, padx=20, pady=Config.pady,sticky="EW")

        # Up time (sec)
        up_time_label = ctk.CTkLabel(self, text="Up time (sec)", font=("Arial", 19),text_color=Config.text_color)
        up_time_label.grid(row=7, column=3, padx=20, pady=Config.pady, sticky="w")

        up_time_dropdown = self.create_dd(field="up_time", options=Config.up_time_sec_options)
        up_time_dropdown.grid(row=7, column=4, padx=20, pady=Config.pady,sticky="EW")

        # Firing position
        firing_position_label = ctk.CTkLabel(self, text="Firing position", font=("Arial", 19),text_color=Config.text_color)
        firing_position_label.grid(row=8, column=0, padx=20, pady=Config.pady, sticky="w")

        firing_position_dropdown = self.create_dd(field="firing_position", options=Config.firing_position_options)
        firing_position_dropdown.grid(row=8, column=1, columnspan=2, padx=20, pady=Config.pady,sticky="EW")


        # Down time (sec)
        down_time_label = ctk.CTkLabel(self, text="Down time (sec)", font=("Arial", 19),text_color=Config.text_color)
        down_time_label.grid(row=8, column=3, padx=20, pady=Config.pady, sticky="w")

        down_time_dropdown = self.create_dd(field="down_time", options=Config.down_time_sec_options)
        down_time_dropdown.grid(row=8, column=4, padx=20, pady=Config.pady,sticky="EW")

        # Time of day
        time_of_day_label = ctk.CTkLabel(self, text="Time of day", font=("Arial", 19),text_color=Config.text_color)
        time_of_day_label.grid(row=9, column=0, padx=20, pady=Config.pady, sticky="w")

        time_of_day_dropdown = self.create_dd(field="time_of_day", options=Config.time_of_day_options)
        time_of_day_dropdown.grid(row=9, column=1, columnspan=2, padx=20, pady=Config.pady,sticky="EW")

        # Terrain dropdown
        terrain_label = ctk.CTkLabel(self, text="Terrain", font=("Arial", 19),text_color=Config.text_color)
        terrain_label.grid(row=9, column=3, padx=20, pady=Config.pady, sticky="w")

        terrain_dropdown = self.create_dd(field="terrain", options=Config.terrain_options)
        terrain_dropdown.grid(row=9, column=4, columnspan=2, padx=20, pady=Config.pady,sticky="EW")

        self.start_thread(setup_label)
        self.start_thread(type_of_target_label)
        self.start_thread(time_label)
        self.start_thread(exposures_label)
        self.start_thread(up_time_label)
        
        self.start_thread(down_time_label)
        self.start_thread(type_of_practice_label)
        self.start_thread(terrain_label)
        
        # Add image "imgs_conv/Standing grouping.png"
        img = Image.open("assets/Grouping.png")
        img = img.resize((int(img.width*0.7), int(img.height*0.7)))
        img_tk = ImageTk.PhotoImage(img)
        self.img_label = ctk.CTkLabel(self, image=img_tk, text="")
        self.img_label.grid(row=4, column=5, rowspan=5, padx=20, pady=Config.pady)

        # add start button
        start_button = ctk.CTkButton(self, text="Start", font=("Arial", 19), text_color=Config.text_color, command=onclick)
        start_button.grid(row=10, column=2, columnspan=2, padx=20, pady=Config.pady, sticky="EW")

        # label2 = ctk.CTkLabel(self, text="This is theow", font=("Arial", 19),text_color=Config.text_color)
        # label2.grid(row=0, column=5 , padx=20, pady=Config.pady)
        
        
        


        
