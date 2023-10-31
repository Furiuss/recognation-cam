import cv2
import numpy as np
import os
import re

# the same function we've used before
from helper_functions import resize_video

detector = "ssd"

def criar_pastas(caminho_da_imagem):
    if not os.path.exists(caminho_da_imagem):
        os.makedirs(caminho_da_imagem)

# Return the detected face using SSD
def detect_face_ssd(network, orig_frame, show_conf=True, conf_min=0.7):
    frame = orig_frame.copy()
    (h, w) = frame.shape[:2]
    # é convertido para blob
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
    # é enviado a imagem para a camda de entrada da rede neural
    network.setInput(blob)
    # é obtido as detecções
    detections = network.forward()

    face_roi = None
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_min:
            bbox = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (start_x, start_y, end_x, end_y) = bbox.astype("int")

            if (start_x<0 or start_y<0 or end_x > w or end_y > h):
                continue

            face_roi = orig_frame[start_y:end_y,start_x:end_x]
            face_roi = cv2.resize(face_roi, (90, 120))
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            if show_conf:
                text_conf = "{:.2f}%".format(confidence * 100)
                cv2.putText(frame, text_conf, (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return face_roi, frame
