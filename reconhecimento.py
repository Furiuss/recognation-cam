import cv2
import numpy as np
import pickle
import firestore
import threading

import whatsapp

threshold = 96

face_names = {}
with open("face_names.pickle", "rb") as f:
    original_labels = pickle.load(f)
    face_names = {v: k for k, v in original_labels.items()}

array_predicoes = []

def reconhecer_rostos(network,  orig_frame, face_names, conf_min=0.7):
    # instancia o algoritmo de reconhecimento LPBH
    face_classifier = cv2.face.LBPHFaceRecognizer_create()
    # le o arquivo com os mapeamentos de histograma
    face_classifier.read("lbph_classifier.yml")

    # cria uma cópia do frame original
    frame = orig_frame.copy()
    # converte imagem para cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # shape retorna uma tupla (300, 300, 3), logo será pegado as duas primeras posições
    (h, w) = frame.shape[:2]
    # média dos valores, pixels entre 0 e 255. Ou seja, uma normalização do rgb
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
    network.setInput(blob)

    deteccoes = network.forward()

    valores_das_deteccoes = deteccoes.shape[2]

    # EXTRAÇÃO DOS DADOS
    for i in range(0, valores_das_deteccoes):

        confianca = deteccoes[0, 0, i, 2]

        if confianca > conf_min:

            # calculo do bounding box para exibir na posicao correte, conforme o tamanho da imagem original
            # bouding box = caixa delimitadora na da face
            bbox = deteccoes[0, 0, i, 3:7] * np.array([w, h, w, h])

            # vai retornar as posições x e y do bbox convertido para inteiro
            (start_x, start_y, end_x, end_y) = bbox.astype("int")

            if (start_x<0 or start_y<0 or end_x > w or end_y > h):
                continue

            # imagem de interesse para ser analisada no lbph
            face_roi = gray[start_y:end_y,start_x:end_x]
            face_roi = cv2.resize(face_roi, (90, 120))
            predicao, conf = face_classifier.predict(face_roi)

            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

            if (conf > threshold):
                text = "Nao identificado"
            else:
                if predicao not in array_predicoes:
                    mandar_mensagem_thread(orig_frame, face_names[predicao])
                    array_predicoes.append(predicao)

                nome_formatado = face_names[predicao].split("-")[0]
                pred_name = nome_formatado
                text = "{} -> {:.4f}".format(pred_name, conf)

            cv2.putText(frame, text, (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def mandar_mensagem(frame, nome):
    nome_arquivo = f"print-{nome}.jpg"
    cv2.imwrite(nome_arquivo, frame)
    firestore.adicionarPrintSuspeito(nome, nome_arquivo)
    link_imagem = firestore.pegar_print(nome)
    cpf_foragido = nome.split("-")[1]
    foragido = pegar_foragido(cpf_foragido)
    whatsapp.enviar_mensagem(foragido, link_imagem)

def mandar_mensagem_thread(frame, nome):
    thread = threading.Thread(target=mandar_mensagem, args=(frame, nome))
    thread.start()

def pegar_foragido(cpf):
    return firestore.pegarForagidoPeloCpf(cpf)
