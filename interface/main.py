import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
from customtkinter import CTk
from utils import CapturaRosto
from mtcnn.mtcnn import MTCNN
import random

class CustomTkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconhecimento Facial")

        # Crie um widget Notebook para as abas
        self.notebook = ttk.Notebook(root)

        # Crie e adicione abas ao Notebook
        self.tab_treinamento = ctk.CTkFrame(self.notebook)
        self.tab_treinamento.configure(fg_color="#4a4a4a")

        self.tab_reconhecimento = ctk.CTkFrame(self.notebook)

        self.notebook.add(self.tab_treinamento, text="Treinamento")
        self.notebook.add(self.tab_reconhecimento, text="Reconhecimento")

        # Adicione widgets às abas (Treinamento)

        self.entrada_id = ctk.CTkEntry(self.tab_treinamento, placeholder_text="ID")
        self.entrada_id.pack(pady=10)

        self.entrada_nome = ctk.CTkEntry(self.tab_treinamento, placeholder_text="Nome")
        self.entrada_nome.pack(pady=10)

        self.entrada_cpf = ctk.CTkEntry(self.tab_treinamento, placeholder_text="CPF")
        self.entrada_cpf.pack(pady=10)

        self.entrada_dataNascimento = ctk.CTkEntry(self.tab_treinamento, placeholder_text="Data de Nascimento")
        self.entrada_dataNascimento.pack(pady=10)

        self.botao_capturarRosto = ctk.CTkButton(self.tab_treinamento, text="Capturar Rosto", command=self.capturarRosto)
        self.botao_capturarRosto.pack(side="left",ipadx=80, padx=10, pady=5)

        self.botao_parar = ctk.CTkButton(self.tab_treinamento, text="Parar", command=self.pararWebCam)
        self.botao_parar.pack(side="left", ipadx=75)
        self.botao_parar.configure(state="disabled")

        # Adicione widgets às abas (Reconhecimento)

        self.resposta_id = ctk.CTkEntry(self.tab_reconhecimento, placeholder_text="ID")
        self.resposta_id.pack(pady=10)

        self.resposta_nome = ctk.CTkEntry(self.tab_reconhecimento, placeholder_text="Nome")
        self.resposta_nome.pack(pady=10)

        self.resposta_cpf = ctk.CTkEntry(self.tab_reconhecimento, placeholder_text="CPF")
        self.resposta_cpf.pack(pady=10)

        self.resposta_dataNascimento = ctk.CTkEntry(self.tab_reconhecimento, placeholder_text="Data de Nascimento")
        self.resposta_dataNascimento.pack(pady=10)

        # Finalmente, coloque o Notebook na janela principal
        self.notebook.pack(padx=10, pady=10, fill="both", expand=True)

        self.canvas = ctk.CTkCanvas(root, width=640, height=480)
        self.canvas.pack()

        self.video_capture = None

        self.contador = 1

    def capturarRosto(self):
        self.video_capture = cv2.VideoCapture(0)

        if self.entrada_id.get() == "":
            messagebox.showwarning("Aviso", "O campo ID deve ser preenchido!",parent=self.root)
            return

        if self.entrada_nome.get() == "":
            messagebox.showwarning("Aviso", "O campo Nome deve ser preenchido!",parent=self.root)
            return

        if not self.video_capture.isOpened():
            messagebox.showerror("Erro", "Não foi possível abrir a webcam.")
            return

        self.botao_capturarRosto.configure(state="disabled")
        self.botao_parar.configure(state="normal")

        self.mostrarWebCam()

    def mostrarWebCam(self):
        _, frame = self.video_capture.read()

        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            detector = MTCNN()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detect_faces(frame)
            for face in faces:
                x, y, w, h = face["box"]
                caminho = f'../stash/imagemProcessada/{self.entrada_nome.get()}.{self.entrada_id.get()}.{self.contador}.jpg'
                cv2.imwrite(caminho, gray[y:y + h, x:x + w])
                self.contador+=1
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            self.display_frame(frame)
            self.root.after(10, self.mostrarWebCam)
        else:
            self.close_webcam()

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = tk.PhotoImage(data=cv2.imencode(".png", frame)[1].tostring())

        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.image = photo

    def pararWebCam(self):
        self.video_capture.release()
        self.canvas.image = None

        self.botao_capturarRosto.configure(state="normal")
        self.botao_parar.configure(state="disabled")


if __name__ == "__main__":
    root = ctk.CTk()
    root.configure(background="dark-blue")
    app = CustomTkinterApp(root)
    root.mainloop()
