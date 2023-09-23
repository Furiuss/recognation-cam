import customtkinter as ctk

from tkinter_service.camera_output import *
from menu import Menu
import cv2
from helper_functions import resize_video
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self):

        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('Face Recognition')
        self.minsize(800, 500)

        #layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)

        #widgets
        self.camera_output = CameraOutput(self)
        self.close_button = CloseOutput(self, self.close_camera)
        self.menu = Menu(self)

        # self.resize_image()
        # run
        self.mainloop()

    def close_camera(self):
        print("fechei jkjkk")


App()