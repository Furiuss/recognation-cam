# pip install opencv-python==4.5.2
import cv2
from mtcnn.mtcnn import MTCNN

video=cv2.VideoCapture(0)

detector = MTCNN()

id = input("Enter Your ID: ")
contador=0

def salvar_imagem(id, contador, imagem):
    caminho = f'../stash/Gustavo3/User.{id}.{contador}.jpg'
    cv2.imwrite(caminho, imagem)

while True:
    ret,frame=video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces =  detector.detect_faces(frame)
    for face in faces:
        x,y,w,h = face["box"]
        contador += 1
        salvar_imagem(id, contador, gray[y:y+h, x:x+w])
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)

    cv2.imshow("Frame",frame)

    if contador>500:
        break

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
print("Base de dados concluída..................")