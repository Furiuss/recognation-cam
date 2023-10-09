import cv2
import numpy as np
import os
import pickle
import re
import face_recognition
from helper_functions import resize_video

# pickle_name = "face_encodings_custom.pickle"
#
# largura_maxima = 800
#
# dados_codificados = pickle.loads(open(pickle_name, "rb").read())
# lista_encodificada = dados_codificados["encodings"]
# lista_de_nomes = dados_codificados["names"]

def reconhecer_faces(imagem, lista_encodificada, lista_de_nomes, redimensionar=0.25, tolerancia=1.0):

    imagem = cv2.resize(imagem, (0, 0), fx=redimensionar, fy=redimensionar)

    img_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

    localizacoes_dos_rostos = face_recognition.face_locations(img_rgb)
    rostos_codificados = face_recognition.face_encodings(img_rgb, localizacoes_dos_rostos)

    nomes_dos_rostos = []
    valores_conf = []
    
    for rosto_codificado in rostos_codificados:

        matches = face_recognition.compare_faces(lista_encodificada, rosto_codificado, tolerance=tolerancia)
        nome = "Não identificado"

        distancia_do_rosto = face_recognition.face_distance(lista_encodificada, rosto_codificado)
        indice_melhor_match = np.argmin(distancia_do_rosto)
        
        if matches[indice_melhor_match]:
            nome = lista_de_nomes[indice_melhor_match]
            
        nomes_dos_rostos.append(nome)
        valores_conf.append(distancia_do_rosto[indice_melhor_match])

    localizacoes_dos_rostos = np.array(localizacoes_dos_rostos)
    localizacoes_dos_rostos = localizacoes_dos_rostos / redimensionar
    return localizacoes_dos_rostos.astype(int), nomes_dos_rostos, valores_conf

def show_recognition(frame, localizacoes_dos_rostos, face_names, conf_values):
    for face_loc, name, conf in zip(localizacoes_dos_rostos, face_names, conf_values):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        conf = "{:.8f}".format(conf)
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (20, 255, 0), 2, lineType=cv2.LINE_AA)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (20, 255, 0), 4)
        if name != "Não identificado":
            cv2.putText(frame, conf, (x1, y2 + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (20, 255, 0), 1, lineType=cv2.LINE_AA)

    return frame

# cam = cv2.VideoCapture(0)
#
# while True:
#     ret, frame = cam.read()
#
#     if largura_maxima != None:
#         video_width, video_height = resize_video(frame.shape[1], frame.shape[0], largura_maxima)
#         frame = cv2.resize(frame, (video_width, video_height))
#
#     localizacoes_dos_rostos, face_names, conf_values = reconhecer_faces(frame, lista_encodificada, lista_de_nomes, 0.25)
#     processed_frame = show_recognition(frame, localizacoes_dos_rostos, face_names, conf_values)
#
#     cv2.imshow("Reconhecimento de faces", frame)
#     if cv2.waitKey(1) == 27:
#         break
#
# print("Concluído!")
# cam.release()
# cv2.destroyAllWindows()
