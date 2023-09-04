import cv2
import numpy as np

def removerRuido(imagem):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    imagemSemRuido = clahe.apply(imagem)
    return imagemSemRuido

def removerRuidoPorGaussianBlur(imagem):
    imagemSemRuido = cv2.GaussianBlur(imagem, (5, 5), 0)
    return imagemSemRuido

def converterParaEscalaDeCinza(imagem):
    imagemEscalaCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    return imagemEscalaCinza

def redimensionar(imagem, largura, altura):
    imagemRedimensionada = cv2.resize(imagem, (largura, altura))
    return imagemRedimensionada

def clipping(imagem):
    valor_min = 0
    valor_max = 255
    imagem_clipped = np.clip(imagem, valor_min, valor_max)
    return imagem_clipped

def filtragemSeletiva(imagem):
    # Crie uma máscara com a mesma forma da imagem, preenchida com zeros
    mascara = np.zeros(imagem.shape[:2], dtype=np.uint8)

    # Defina as coordenadas da área que você deseja filtrar seletivamente
    x1, y1 = 0,0  # Coordenadas do canto superior esquerdo da área
    x2, y2 = 30,100  # Coordenadas do canto inferior direito da área

    # Desenhe um retângulo branco na máscara para definir a área de filtro
    cv2.rectangle(mascara, (x1, y1), (x2, y2), (255), thickness=cv2.FILLED)

    imagem_filtrada = cv2.bitwise_and(imagem, imagem, mask=mascara)
    return imagem_filtrada


