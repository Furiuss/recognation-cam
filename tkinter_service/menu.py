import customtkinter as ctk
from panels import *

class Menu(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')

        self.add('Coleção')
        self.add('Treinamento')

        ColecaoFrame(self.tab('Coleção'))
        TreinamentoFrame(self.tab('Treinamento'))

class ColecaoFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color = 'transparent')
        self.pack(expand=True, fill = 'both')
        SliderPanel(self, 'test')


class TreinamentoFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        self.login_label = ctk.CTkLabel(self, text="CustomTkinter\nLogin Page",
                                                  font=ctk.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        self.username_entry = ctk.CTkEntry(self, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = ctk.CTkEntry(self, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.login_button = ctk.CTkButton(self, text="Login", width=200)
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))