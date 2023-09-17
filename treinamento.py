import cv2
import numpy as np
import os
from PIL import Image
import pickle

caminho_treinamento = 'dataset/'

def obterImagemTreinamento(caminho_treinamento):
  arquivos  = [os.path.join(caminho_treinamento, f) for f in os.listdir(caminho_treinamento)]

  faces = []
  ids = []

  nome_faces = {}
  id = 1
  print("Carregando rostos do conjunto de treinamento...")
  for arquivo in arquivos:
    nome = os.path.split(arquivo)[1]

    caminho_imagens = [os.path.join(arquivo, f) for f in os.listdir(arquivo)]
    for caminho in caminho_imagens:
      imagem = Image.open(caminho).convert('L')
      face = np.array(imagem, 'uint8')
      face = cv2.resize(face, (90, 120))
      print(str(id) + " <-- " + caminho)
      ids.append(id)
      faces.append(face)
      cv2.imshow("Treinando faces...", face)
      cv2.waitKey(50)

    if not nome in nome_faces:
      nome_faces[nome] = id
      id += 1

  return np.array(ids), faces, nome_faces

ids, faces, nome_faces = obterImagemTreinamento(caminho_treinamento)

for nome in nome_faces:
  print(str(nome) + " => ID " + str(nome_faces[nome]))

# armazenar nomes e ids em um arquivo pickle
with open("face_names.pickle", "wb") as f:
  pickle.dump(nome_faces, f)

print('\n')
print('Treinamento Eigenface iniciado......')
eigen_classifier = cv2.face.EigenFaceRecognizer_create()
eigen_classifier.train(faces, ids)
eigen_classifier.write('eigen_classifier.yml')
print('...... Completado!\n')

print('Treinamento Fisherface iniciado......')
fisher_classifier = cv2.face.FisherFaceRecognizer_create()
fisher_classifier.train(faces, ids)
fisher_classifier.write('fisher_classifier.yml')
print('...... Completado!\n')

print('Treinamento LBPH iniciado......')
lbph_classifier = cv2.face.LBPHFaceRecognizer_create()
lbph_classifier.train(faces, ids)
lbph_classifier.write('lbph_classifier.yml')
print('...... Completado!\n')
