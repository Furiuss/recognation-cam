import cv2
import dlib
import face_recognition


def main():
    # Carregar o modelo de detecção facial do dlib
    detector = dlib.get_frontal_face_detector()

    # Carregar modelos de reconhecimento facial do face_recognition
    known_faces = []
    known_names = []

    # Carregar imagens de rostos conhecidos e seus nomes
    known_faces.append(face_recognition.load_image_file("andre/andre.1.jpg"))
    known_names.append("André")

    known_faces.append(face_recognition.load_image_file("known_faces/face2.jpg"))
    known_names.append("Nome da Pessoa 2")

    # Criar embeddings para os rostos conhecidos
    known_face_embeddings = [face_recognition.face_encodings(face)[0] for face in known_faces]

    # Iniciar a captura de vídeo da webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Detectar rostos na imagem usando dlib
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            # Calcular o embedding do rosto detectado
            face_encodings = face_recognition.face_encodings(frame, [face])

            if len(face_encodings) > 0:
                face_encoding = face_encodings[0]

                # Comparar o embedding do rosto com os embeddings conhecidos
                matches = face_recognition.compare_faces(known_face_embeddings, face_encoding)
                name = "Desconhecido"

                if True in matches:
                    match_index = matches.index(True)
                    name = known_names[match_index]

                # Desenhar um retângulo em torno do rosto e exibir o nome
                top, right, bottom, left = face.top(), face.right(), face.bottom(), face.left()
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Mostrar a imagem com os rostos detectados
        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

main()