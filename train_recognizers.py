import cv2
import numpy as np
import os
from PIL import Image
import pickle


training_path = 'dataset/'

def get_image_data(path_train):
  subdirs = [os.path.join(path_train, f) for f in os.listdir(path_train)]
  #print(subdirs)
  faces = []
  ids = []

  face_names = {}
  id = 1
  print("Loading faces from training set...")
  for subdir in subdirs:
    name = os.path.split(subdir)[1]
    images_list = [os.path.join(subdir, f) for f in os.listdir(subdir)]
    for path in images_list:
      image = Image.open(path).convert('L')
      face = np.array(image, 'uint8')
      face = cv2.resize(face, (90, 120))
      print(str(id) + " <-- " + path)
      ids.append(id)
      faces.append(face)
      cv2.imshow("Training faces...", face)
      cv2.waitKey(50)

    if not name in face_names:
      face_names[name] = id
      id += 1

  return np.array(ids), faces, face_names

# get_image_data("dataset/")