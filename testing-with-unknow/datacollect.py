# pip install opencv-python==4.5.2

import cv2
from mtcnn.mtcnn import MTCNN

video=cv2.VideoCapture(0)

detector = MTCNN()

id = input("Enter Your ID: ")
# id = int(id)
count=0

while True:
    ret,frame=video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces =  detector.detect_faces(frame)
    for face in faces:
        x,y,w,h = face["box"]
        count=count+1
        cv2.imwrite('../stash/Gustavo3/User.'+str(id)+"."+str(count)+".jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)

    cv2.imshow("Frame",frame)

    k=cv2.waitKey(1)

    if count>500:
        break

video.release()
cv2.destroyAllWindows()
print("Dataset Collection Done..................")