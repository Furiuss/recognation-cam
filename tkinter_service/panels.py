import customtkinter as ctk
from settings import *
import cv2

class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=DARK_GREY)
        self.pack(fill = 'x', pady=4,ipady=8)

class SliderPanel(Panel):
    def __init__(self, parent, text):
        super().__init__(parent=parent)

        ctk.CTkLabel(self, text=text).pack()
