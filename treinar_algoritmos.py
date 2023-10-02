import cv2
import numpy as np
import os
from PIL import Image
import pickle
import yaml

training_path = 'dataset/'
yml_filename = 'training_data.yml'  # Nome do arquivo YAML que contém os dados de treinamento

def load_training_data(yml_filename):
    if os.path.exists(yml_filename):
        with open(yml_filename, 'r') as file:
            data = yaml.safe_load(file)
        return data
    else:
        return {"ids": [], "faces": [], "face_names": {}}

def save_training_data(yml_filename, data):
    with open(yml_filename, 'w') as file:
        yaml.dump(data, file)

def get_image_data(path_train, data):
    subdirs = [os.path.join(path_train, f) for f in os.listdir(path_train)]

    print("Loading faces from training set...")
    for subdir in subdirs:
        name = os.path.split(subdir)[1]

        images_list = [os.path.join(subdir, f) for f in os.listdir(subdir)]
        for path in images_list:
            image = Image.open(path).convert('L')
            face = np.array(image, 'uint8')
            print(str(data["id"]) + " <-- " + path)
            data["ids"].append(data["id"])
            data["faces"].append(face)

        if name not in data["face_names"]:
            data["face_names"][name] = data["id"]
            data["id"] += 1

    return data

# Carregue os dados de treinamento existentes (ou crie novos dados se o arquivo não existir)
training_data = load_training_data(yml_filename)

# Obtenha as novas informações de imagem de treinamento
training_data = get_image_data(training_path, training_data)

# Salve as informações atualizadas no arquivo YAML
save_training_data(yml_filename, training_data)

# Resto do seu código para treinamento e classificação
