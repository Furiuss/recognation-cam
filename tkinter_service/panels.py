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

        # ctk.CTkLabel(self, text=text).pack()
        self.entrada_nome = ctk.CTkEntry(self, placeholder_text="Nome")
        self.entrada_nome.pack(pady=2)

        self.entrada_cpf = ctk.CTkEntry(self, placeholder_text="CPF")
        self.entrada_cpf.pack(pady=2)

        self.entrada_dataNascimento = ctk.CTkEntry(self, placeholder_text="Data de Nascimento")
        # self.entrada_dataNascimento.pack(pady=2)

        # self.botao_capturarRosto = ctk.CTkButton(self, text="Capturar Rosto")
        # self.botao_capturarRosto.pack(side="left", ipadx=80, padx=10, pady=5)
        #
        # self.botao_parar = ctk.CTkButton(self, text="Parar")
        # self.botao_parar.pack(side="left", ipadx=75)
        # self.botao_parar.configure(state="disabled")

class Botao(ctk.CTkButton):
    def __init__(self, parent, texto, comando=None):
        super().__init__(master = parent, text = texto, command=comando)
        self.pack(side = 'bottom', pady=2)
