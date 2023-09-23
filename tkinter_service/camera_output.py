import customtkinter as ctk
from tkinter import *
from settings import *
import cv2
from helper_functions import resize_video
from PIL import Image, ImageTk

class CameraOutput(Canvas):
    def __init__(self, parent):
        super().__init__(master = parent, background= 'black', bd = 0, highlightthickness=0, relief='ridge')
        self.grid(row = 0, column= 1, sticky = 'nsew')
        self.label = Label(self, text='text')
        self.label.pack()
        # button1 = ctk.CTkButton(self, text="Open Camera", command=self.resize_image())
        # button1.pack()


    def resize_image(self):
        cam = cv2.VideoCapture(0)

        # loop over every frame of the video stream
        ret, frame = cam.read()
        max_width = 600
        # resize only if a max_width is specified
        video_width, video_height = resize_video(frame.shape[1], frame.shape[0], max_width)
        frame = cv2.resize(frame, (video_width, video_height))


        image = Image.fromarray(frame)
        photo_image = ImageTk.PhotoImage(image=image)

        self.label.image = photo_image
        self.label.configure(image=photo_image )

        # Repeat the same process after every 10 seconds
        self.label.after(10, self.resize_image())

        # return self.camera_output.create_image(0,0,image = pic)

class CloseOutput(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(master=parent, text = 'x',
                         text_color=WHITE,
                         command=close_func,
                         fg_color= 'transparent',
                         width=40, height=40,
                         corner_radius=0,
                         hover_color=CLOSE_RED)
        self.place(relx = 0.99, rely = 0.01, anchor = 'ne')
        self.bind()

