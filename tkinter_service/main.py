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

    def mostrarWebCam(self):
        self.video_capture = cv2.VideoCapture(0)
        _, frame = self.video_capture.read()
        max_width = 800

        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if max_width is not None:
                video_width, video_height = resize_video(frame.shape[1], frame.shape[0], max_width)
                frame = cv2.resize(frame, (video_width, video_height))

            processed_frame = detect_face_ssd(network, frame)
            self.display_frame(processed_frame)
            self.after(1, self.mostrarWebCam)
        else:
            self.close_webcam()

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = PhotoImage(data=cv2.imencode(".png", frame)[1].tostring())
        self.create_image(0, 0, image=photo, anchor=ctk.NW)
        self.image = photo


App()