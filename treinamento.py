import cv2
import numpy as np
import os
from PIL import Image

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
      # converte para escala de cinza
      imagem = Image.open(caminho).convert('L')
      # transforma a imagem em uma representação númerica
      face = np.array(imagem, 'uint8')
      face = cv2.resize(face, (90, 120))
      ids.append(id)
      faces.append(face)
      cv2.imshow("Treinando faces...", face)
      cv2.waitKey(50)

    if not nome in nome_faces:
      nome_faces[nome] = id
      id += 1

  return np.array(ids), faces, nome_faces
