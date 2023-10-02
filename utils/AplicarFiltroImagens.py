import os
import cv2
import ProcessamentoImagem
from PIL import Image,  ImageFilter
import numpy as np

pasta_imagens = "../dataset/andre"

if not os.path.exists(pasta_imagens):
    print("A pasta especificada não existe.")
else:
    # Listar todos os arquivos na pasta
    arquivos = os.listdir(pasta_imagens)


    for arquivo in arquivos:
        # Carregue a imagem
        caminho_imagem = os.path.join(pasta_imagens, arquivo)
        imagem = cv2.imread(caminho_imagem)

        # Aplicar os filtro necessários:

        imagem_processada = ProcessamentoImagem.redimensionar(imagem)

        imagem_processada = ProcessamentoImagem.converterParaEscalaDeCinza(imagem_processada)

        imagem_processada = ProcessamentoImagem.removerRuido(imagem_processada)

        imagem_processada = ProcessamentoImagem.equalizacaoHistograma(imagem_processada)

        imagem_processada = ProcessamentoImagem.normalizar_intensidade(imagem_processada)

        # Salvar a imagem processada de volta na pasta
        caminho_imagem_processada = os.path.join("../dataset/andre", f"{arquivo}")
        cv2.imwrite(caminho_imagem_processada, imagem_processada)

        print(f"Imagem {arquivo} processada e salva como {caminho_imagem_processada}")

print("Processamento de imagens concluído.")