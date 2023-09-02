import cv2
from ultralytics import YOLO
import winsound
import threading
from PIL import Image
import whatsapp

video = cv2.VideoCapture("ex01.mp4")

modelo = YOLO("yolov8n.pt")

area = [510,210,900,600]

tocarAlarme = False

def alarme():
    global tocarAlarme
    for _ in range(5):
        winsound.Beep(2500, 500)

    tocarAlarme = False

def salvarImagemBandido(img):
    image_pil = Image.fromarray(img)

    image_pil.thumbnail((400, 400))

    image_pil.save("imagem-bandido/imagem.png")

enviado = False

while True:
    check, img = video.read()

    img = cv2.resize(img, (1270, 720))

    img2 = img.copy()
    cv2.rectangle(img2, (area[0], area[1]), (area[2], area[3]), (0, 255,0), -1)

    resultado = modelo(img)

    for objetos in resultado:
        obj = objetos.boxes
        for dados in obj:
            x, y, w, h = dados.xyxy[0]
            x,y,w,h = int(x), int(y), int(w), int(h)
            pessoa = 0
            classe = int(dados.cls[0])
            if(classe == pessoa):
                cx, cy = (x + w) // 2, (y + h) // 2
                cv2.circle(img, (cx, cy), 5, (0, 0, 0), 5)
                cv2.rectangle(img, (x,y), (w, h), (255,0,0), 5)

                estaAreaDelimitada = cx >= area[0] and cx <= area[2] and cy >= area[1] and cy <= area[3]
                if estaAreaDelimitada:
                    cv2.rectangle(img2, (area[0], area[1]), (area[2], area[3]), (0, 0,255), -1)
                    cv2.rectangle(img, (100,30), (470,80), (0, 0,255), -1)
                    cv2.putText(img, "INVASOR DETECTADO", (105,65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),3)

                    if(enviado == False):

                        # Converte porque a imagem está em BGR e vai passar para RGB :
                        imagem_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                        salvarImagemBandido(imagem_RGB)

                        whatsapp.enviar_mensagem()

                        enviado = True


                    if not tocarAlarme:
                        tocarAlarme = True
                        threading.Thread(target=alarme()).start()

    imgFinal = cv2.addWeighted(img2, 0.5, img, 0.5, 0)

    cv2.imshow("img", imgFinal)
    tecla = cv2.waitKey(1)
    tecla_Enter = 13
    if tecla == tecla_Enter:
        break

