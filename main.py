import tkinter as tk
from tkinter import messagebox

import cv2.face

# from train_recognizers import *
from treinamento import obterImagemTreinamento
import helper_functions as hf
import datetime
from entities.Foragido import Foragido
import customtkinter as ctk
from recognition_webcam import *
from face_capture_webcam import *
import os

class CustomTkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconhecimento Facial")

        self.sample = 0
        self.starting_sample_number = 0
        self.max_width = 800

        # Crie um widget Notebook para as abas
        # self.notebook = ttk.Notebook(root)
        self.notebook = ctk.CTkTabview(root)
        self.notebook.add("Cadastro")
        self.notebook.add("Reconhecimento")

        # Crie e adicione abas ao Notebook
        self.tab_treinamento = Frame(self.notebook.tab('Cadastro'))
        self.tab_treinamento.configure()

        self.tab_reconhecimento = Frame(self.notebook.tab('Reconhecimento'))
        self.tab_reconhecimento.configure()

        # Adicione widgets às abas (Treinamento)

        self.entrada_nome = ctk.CTkEntry(self.tab_treinamento, placeholder_text="Nome")
        self.entrada_nome.pack()

        self.entrada_cpf = ctk.CTkEntry(self.tab_treinamento, placeholder_text="CPF")
        self.entrada_cpf.pack()

        self.entrada_dataNascimento = ctk.CTkEntry(self.tab_treinamento, placeholder_text="Data de Nascimento")
        self.entrada_dataNascimento.pack()

        self.botao_capturarRosto = ctk.CTkButton(self.tab_treinamento, text="Capturar Rosto", command=self.capturarRosto)
        self.botao_capturarRosto.pack(side="left",ipadx=80, padx=10, pady=5)

        self.botao_parar = ctk.CTkButton(self.tab_treinamento, text="Parar", command=self.pararWebCam)
        self.botao_parar.pack(side="left", ipadx=75)
        self.botao_parar.configure(state="disabled")

        # Adicione widgets às abas (Reconhecimento)

        self.resposta_treinar = ctk.CTkButton(self.tab_reconhecimento, text="Aplicar Treinamento", command=self.treinarAlgoritmo)
        self.resposta_treinar.pack(side="left", ipadx=80, padx=10, pady=5)

        self.resposta_reconhecer = ctk.CTkButton(self.tab_reconhecimento, text="Reconhecer", command=self.configurarReconhecimento)
        self.resposta_reconhecer.pack(side="left", ipadx=75)

        self.botao_parar_rec = ctk.CTkButton(self.tab_reconhecimento, text = '',
                         text_color="white",
                         fg_color='transparent',
                         command=self.pararWebCam,
                         width=40, height=40,
                         corner_radius=0,
                         state="disabled")
        self.botao_parar_rec.place(relx = 0.99, rely =0.80, anchor = 'ne')

        # Finalmente, coloque o Notebook na janela principal
        self.notebook.pack(padx=10, pady=10, fill="both", expand=True)

        self.canvas = ctk.CTkCanvas(root, width=640, height=480, background= '#4a4a4a', bd = 0, highlightthickness=0, relief='ridge')
        self.canvas.pack()

        self.video_capture = None

        self.contador = 1

        self.max_width = 800

        self.person_name = ""
        self.pasta_rostos = "dataset/"
        self.caminho_imagem = ""
        self.network = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")

    # CADASTRO
    def capturarRosto(self):
        self.video_capture = cv2.VideoCapture(0)

        if self.entrada_nome.get() == "":
            messagebox.showwarning("Aviso", "O campo Nome deve ser preenchido!",parent=self.root)
            return

        if not self.video_capture.isOpened():
            messagebox.showerror("Erro", "Não foi possível abrir a webcam.")
            return

        self.botao_capturarRosto.configure(state="disabled")
        self.botao_parar.configure(state="normal")
        self.person_name = hf.remover_caracteres_especiais(self.entrada_nome.get()) + "-" + hf.remover_caracteres_especiais(self.entrada_cpf.get())
        self.caminho_imagem = os.path.sep.join([self.pasta_rostos, self.person_name])
        criar_pastas(caminho_da_imagem=self.caminho_imagem)
        self.mostrarWebCam()

    # TREINAMENTO
    def treinarAlgoritmo(self):
        ids, rostos, nomes_rostos = obterImagemTreinamento('dataset/')

        # store names and ids in a pickle file
        # armazena nomes e ids em um pickle file
        with open("face_names.pickle", "wb") as f:
            pickle.dump(nomes_rostos, f)

        lbph_classifier = cv2.face.LBPHFaceRecognizer().create()
        lbph_classifier.train(rostos, ids)
        lbph_classifier.write('lbph_classifier.yml')
        messagebox.showwarning("Aviso", "Para reconhecer é necessário reiniciar a aplicação")
        cv2.destroyAllWindows()

    def configurarReconhecimento(self):
        self.video_capture = cv2.VideoCapture(0)
        self.reconhecer()
        self.aplicar_configuracoes_botoes()

    # RECONHECIMENTO
    def reconhecer(self):
        try:
            _, frame = self.video_capture.read()

            video_width, video_height = resize_video(frame.shape[1], frame.shape[0], self.max_width)
            frame = cv2.resize(frame, (video_width, video_height))

            processed_frame = recognize_faces(self.network,  frame, face_names)
            self.display_frame(processed_frame)
            self.root.after(1, self.reconhecer)
        except Exception as e:
            print(e)
            self.resetar_configuracoes_botoes()
            self.pararWebCam()

    #
    def mostrarWebCam(self):
        try:
            _, frame = self.video_capture.read()

            if frame is not None:

                    if max_width is not None:
                        video_width, video_height = resize_video(frame.shape[1], frame.shape[0], max_width)
                        frame = cv2.resize(frame, (video_width, video_height))

                    face_roi, processed_frame = detect_face_ssd(self.network, frame)

                    self.sample = self.sample + 1
                    photo_sample = self.sample + starting_sample_number - 1 if starting_sample_number > 0 else self.sample
                    image_name = self.person_name + "." + str(photo_sample) + ".jpg"
                    cv2.imwrite(self.caminho_imagem + "/" + image_name, face_roi)
                    print("=> photo " + str(self.sample))

                    cv2.imshow("face", face_roi)
                    self.display_frame(processed_frame)
                    self.root.after(1, self.mostrarWebCam)
            else:
                self.cadastrar_no_banco()
                messagebox.showinfo("Ok", "Dados Cadastrados com Sucesso")
                self.entrada_nome.delete(0, 'end')
                self.entrada_cpf.delete(0, 'end')
                self.entrada_dataNascimento.delete(0, 'end')
        except cv2.error:
            messagebox.showwarning("Aviso", "Por favor, mantenha o rosto mais próximo à câmera e mova-o lentamente. 📷")
            self.capturarRosto()

    def cadastrar_no_banco(self):
        foragido = Foragido(
            nome=self.entrada_nome.get(),
            data_nascimento=self.entrada_dataNascimento.get(),
            cpf=hf.remover_caracteres_especiais(self.entrada_cpf.get()),
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            eh_foragido=True
        )
        firestore.create(foragido)

    def display_frame(self, frame):
        photo = tk.PhotoImage(data=cv2.imencode(".png", frame)[1].tobytes())
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.image = photo

    def pararWebCam(self):
        self.video_capture.release()
        cv2.destroyAllWindows()
        self.canvas.image = None

        self.botao_capturarRosto.configure(state="normal")
        self.botao_parar.configure(state="disabled")

    def aplicar_configuracoes_botoes(self):
        self.botao_parar_rec.configure(state="normal", text="x", fg_color="red")
        self.resposta_reconhecer.configure(state="disabled")
        self.resposta_treinar.configure(state="disabled")

    def resetar_configuracoes_botoes(self):
        self.botao_parar_rec.configure(state="disabled", text="", fg_color='transparent')
        self.resposta_reconhecer.configure(state="normal")
        self.resposta_treinar.configure(state="normal")

class Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color = 'transparent')
        self.pack(expand=True, fill = 'both')


if __name__ == "__main__":
    root = ctk.CTk()
    root.configure(background="dark-blue")
    app = CustomTkinterApp(root)
    root.mainloop()
