import tkinter as tk
from tkinter import messagebox
from train_recognizers import *
import firestore as firestore
import datetime
from entities.Foragido import Foragido
import customtkinter as ctk
from recognition_webcam import *
from face_capture_webcam import *
import sys
import os

class CustomTkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconhecimento Facial")

        self.sample = 0
        self.starting_sample_number = 0
        self.max_width = 800

        # Crie um widget Notebook para as abas
        self.notebook = ctk.CTkTabview(root)
        self.notebook.add("Coleção")
        self.notebook.add("Reconhecimento")

        # Crie e adicione abas ao Notebook
        self.tab_treinamento = Frame(self.notebook.tab('Coleção'))
        self.tab_treinamento.configure()

        self.tab_reconhecimento = Frame(self.notebook.tab('Reconhecimento'))
        self.tab_reconhecimento.configure()

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

        self.resposta_reconhecer = ctk.CTkButton(self.tab_reconhecimento, text = 'x',
                         text_color="white",
                         command=self.pararWebCam,
                         fg_color= 'red',
                         width=40, height=40,
                         corner_radius=0)
        self.resposta_reconhecer.place(relx = 0.99, rely = 0.01, anchor = 'ne')

        # Finalmente, coloque o Notebook na janela principal
        self.notebook.pack(padx=10, pady=10, fill="both", expand=True)

        self.canvas = ctk.CTkCanvas(root, width=640, height=480, background= '#4a4a4a', bd = 0, highlightthickness=0, relief='ridge')
        self.canvas.pack()

        self.video_capture = None

        self.contador = 1

        self.max_width = 800

        self.person_name = ""
        self.folder_faces = "dataset/"
        self.final_path = ""

    def capturarRosto(self):
        self.video_capture = cv2.VideoCapture(0)

        if self.entrada_nome.get() == "":
            messagebox.showwarning("Aviso", "O campo Nome deve ser preenchido!",parent=self.root)
            return

        if not self.video_capture.isOpened():
            messagebox.showerror("Erro", "Não foi possível abrir a webcam.")
            return
        # adicionarImagensDeForagido()
        self.botao_capturarRosto.configure(state="disabled")
        self.botao_parar.configure(state="normal")
        self.person_name = self.entrada_nome.get() + "-" + self.entrada_cpf.get()
        self.final_path = os.path.sep.join([self.folder_faces, self.person_name])
        create_folders(self.final_path)
        self.mostrarWebCam()


    def treinarAlgoritmo(self):
        ids, faces, face_names = get_image_data(training_path)

        for n in face_names:
            print(str(n) + " => ID " + str(face_names[n]))

        # store names and ids in a pickle file
        with open("face_names.pickle", "wb") as f:
            pickle.dump(face_names, f)

        print('Training LBPH recognizer......')
        lbph_classifier = cv2.face.LBPHFaceRecognizer_create()
        lbph_classifier.train(faces, ids)
        lbph_classifier.write('lbph_classifier.yml')
        print('... Completed!\n')
        print("treinei")
        messagebox.showwarning("Aviso", "Para reconhecer é necessário reiniciar a aplicação")
        self.reiniciar_aplicacao()

    def configurarReconhecimento(self):
        self.video_capture = cv2.VideoCapture(0)
        self.reconhecer()

    def reconhecer(self):
        try:
            _, frame = self.video_capture.read()

            video_width, video_height = resize_video(frame.shape[1], frame.shape[0], self.max_width)
            frame = cv2.resize(frame, (video_width, video_height))

            processed_frame = recognize_faces(network,  frame, face_names)
            self.display_frame(processed_frame)
            self.root.after(1, self.reconhecer)
        except Exception as e:
            print(e)
            self.pararWebCam()

    def mostrarWebCam(self):
        try:
            _, frame = self.video_capture.read()

            if frame is not None:

                    if max_width is not None:
                        video_width, video_height = resize_video(frame.shape[1], frame.shape[0], max_width)
                        frame = cv2.resize(frame, (video_width, video_height))

                    face_roi, processed_frame = detect_face_ssd(network, frame)

                    self.sample = self.sample + 1
                    photo_sample = self.sample + starting_sample_number - 1 if starting_sample_number > 0 else self.sample
                    image_name = self.person_name + "." + str(photo_sample) + ".jpg"
                    cv2.imwrite(self.final_path + "/" + image_name, face_roi)  # save the cropped face (ROI)
                    print("=> photo " + str(self.sample))

                    cv2.imshow("face", face_roi)
                    self.display_frame(processed_frame)
                    self.root.after(1, self.mostrarWebCam)
            else:
                foragido = Foragido(
                    nome=self.entrada_nome.get(),
                    data_nascimento=self.entrada_dataNascimento.get(),
                    cpf=self.entrada_cpf.get(),
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now(),
                    eh_foragido=True
                )
                firestore.create(foragido)

                messagebox.showinfo("Ok", "Dados Cadastrados com Sucesso")
                self.entrada_nome.delete(0, 'end')
                self.entrada_cpf.delete(0, 'end')
                self.entrada_dataNascimento.delete(0, 'end')
        except:
            messagebox.showwarning("Aviso", "Por favor, mantenha o rosto mais próximo à câmera e mova-o lentamente. 📷")
            self.capturarRosto()

    def display_frame(self, frame):
        photo = tk.PhotoImage(data=cv2.imencode(".png", frame)[1].tobytes())

        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.image = photo

    def pararWebCam(self, reset_app=False):
        self.video_capture.release()
        cv2.destroyAllWindows()
        self.canvas.image = None

        self.botao_capturarRosto.configure(state="normal")
        self.botao_parar.configure(state="disabled")

    def reiniciar_aplicacao(self):
        python_executable = sys.executable
        script = os.path.abspath(__file__)
        os.execl(python_executable, python_executable, script)


class Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color = 'transparent')
        self.pack(expand=True, fill = 'both')


if __name__ == "__main__":
    root = ctk.CTk()
    root.configure(background="dark-blue")
    app = CustomTkinterApp(root)
    root.mainloop()
