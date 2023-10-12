import cv2
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
'6 '

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

def redimensionar(imagem, largura=140, altura=140):
    imagemRedimensionada = cv2.resize(imagem, (largura, altura))
    return imagemRedimensionada

def detectorDeBordasCanny(imagem):
    suave = cv2.GaussianBlur(imagem, (7, 7), 0)
    canny1 = cv2.Canny(suave, 5, 80)
    canny2 = cv2.Canny(suave, 80, 200)
    resultado = np.vstack([
        np.hstack([imagem, suave]),
        np.hstack([canny1, canny2])
    ])
    return resultado

def detectorDeBordasSobel(imagem):
    sobelX = cv2.Sobel(imagem, cv2.CV_64F, 1, 0)
    sobelY = cv2.Sobel(imagem, cv2.CV_64F, 0, 1)
    sobelX = np.uint8(np.absolute(sobelX))
    sobelY = np.uint8(np.absolute(sobelY))
    sobel = cv2.bitwise_or(sobelX, sobelY)
    resultado = np.vstack([
        np.hstack([imagem, sobelX]),
        np.hstack([sobelY, sobel])
    ])
    return resultado

def reduzirDimensao_PCA(imagem, var_exp=0.99):
    pca = PCA(var_exp)  # variância explicada de 0.99
    lower_dimension_data = pca.fit_transform(imagem)
    print(lower_dimension_data.shape)
    approximation = pca.inverse_transform(
        lower_dimension_data)

    return approximation

def equalizacaoHistograma(imagem):
    imagemEqualizada = cv2.equalizeHist(imagem)
    return imagemEqualizada

def normalizar_intensidade(imagem):
    return cv2.normalize(imagem, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)


