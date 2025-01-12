import customtkinter as ctk
import tkinter as tk
from settings_screen import SettingsWindow
from shooter_screen import ShooterScreen
from inspector_screen import InspectorScreen
from backend.detectionModule import main as detectModule
import threading
from time import time
from saveImage import saveImage, saveImageAllpoints
from threading import Event
from create_image import createImage
from resultProcess import DataProcess
import cv2

ctk.set_appearance_mode("Dark")	 

ctk.set_default_color_theme("green") 
root = ctk.CTk()
root.withdraw()  # Hide the root window
event = Event()
# Get the screen width and height
main_screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# main screen 1366
screen_width = 1366
screen_height = 768
# shooter view screen
shooter_screen_width = 1024
shooter_screen_height = 768
root.destroy()
print(screen_height, screen_width)
worker_thread = None

points = []

# Create App class
class App(ctk.CTk):
	started = False
	lastTime = time()
	calculateDone = False
	def calculate(self):
		if self.calculateDone:
			self.calculateDone = False
			self.started = False
			event.clear()
			self.destroy()
			self.__init__()
			self.mainloop()
		else:
			print(points)
			event.set()
			res_points = saveImageAllpoints(points[-10:])
			res_img,left_side, right_side = DataProcess("main_gray.png", res_points)
			cv2.imwrite("result_data.png",res_img)
			self.settingsWindow.set_background("result_data.png")
			self.calculateDone = True
			self.settingsWindow.buttonTextChange("Start Again")

# Layout of the GUI will be written in the init itself
	def startClick(self):
		print("Start Clicked")
		global shooterScreen
		global points
		points = []
		if self.shooterScreen is not None:
			print("bg_path", SettingsWindow.bg_path)
			createImage(SettingsWindow.bg_path)
			self.shooterScreen.set_background("result.png")
			self.started = True
			self.settingsWindow.pack_forget()
			self.settingsWindow = InspectorScreen(self, self.calculate)
			self.settingsWindow.pack(fill="both", expand=True)
			self.settingsWindow.set_background("main.png")



	def callBack(self, rx, ry):
		if(self.started):
			ct = time()
			if (ct - self.lastTime) > 1:
				self.lastTime = ct
				print("GUI -> ", rx, ry)
				saveImage(rx, ry)
				self.settingsWindow.set_background("result_data.png")
				points.append((rx,ry))

				
	def __init__(self, *args, **kwargs):
		global worker_thread
		super().__init__(*args, **kwargs)
		self.title("Settings")
		self.geometry(f"{screen_width}x{screen_height}")
		self.shooterView = ctk.CTkToplevel(self)
		self.shooterView.title("Shooter View")
		# (f"{screen_width}x{screen_height}+{screen_width}+0")
		self.shooterView.geometry(f"{shooter_screen_width}x{shooter_screen_height}+{-shooter_screen_width+main_screen_width}+0")
		
		self.settingsWindow = SettingsWindow(self,onclick=self.startClick)
		self.settingsWindow.pack(fill="both", expand=True)
		
		self.shooterScreen = ShooterScreen(self.shooterView)
		self.shooterScreen.pack(fill="both", expand=True)
		worker_thread = threading.Thread(target=detectModule, args=(event, self.callBack,))
		worker_thread.start()
		
if __name__ == "__main__":
	app = App()
	# Runs the app
	app.mainloop()
	event.set()

