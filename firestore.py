import firebase_admin
import pyrebase
from firebase_admin import firestore, credentials, storage
import uuid

myuuid = uuid.uuid4()
import datetime
import os
from datetime import date
from entities.Foragido import Foragido

cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'serviceAccount.json')) # Add your API file path)
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

credPyrebase = {
  "apiKey": "AIzaSyDgU2Z6e5CoUsOAWPMfd-bMH-DlxpApEbs",
  "authDomain": "teste-9f716.firebaseapp.com",
  "projectId": "teste-9f716",
  "storageBucket": "teste-9f716.appspot.com",
  "messagingSenderId": "57694704956",
  "appId": "1:57694704956:web:9e135f2ae64ef112db7a39",
  "measurementId": "G-WYGHFCLTTE",
  "serviceAccount": "serviceAccount.json",
  "databaseURL": "https://teste-9f716-default-rtdb.firebaseio.com/"
}

pyrebase_service = pyrebase.initialize_app(credPyrebase)
storage = pyrebase_service.storage()
collection_ref = db.collection('foragidos')

def create(foragido: Foragido):
    collection_ref.document(foragido.id).set(
      {
        'nome': foragido.nome,
        'data_nascimento': foragido.data_nascimento,
        'cpf': foragido.cpf,
        'eh_foragido': foragido.eh_foragido,
        'created_at': foragido.created_at,
        'updated_at': foragido.updated_at,
        'imagens': foragido.imagens
      }
    )

def read():
    doc = collection_ref.document('70629522146').get()
    print(doc.to_dict())

def read_collection():
    docs = collection_ref.where('nome', '==', 'André').stream()
    for doc in docs:
        stock = doc.to_dict()
        print(stock['nome'])

def add_collection():
    collection_ref.document('70629522146').update({
        'imagens': pegarTodasAsImagens()
    })

def update_collection():
    return

def pegarTodasAsImagens():
    folder_ref = storage.child("screenshots_suspeitos")
    arr_links_imagens = []
    for imagem in folder_ref.list_files():
        imagem.make_public()
        arr_links_imagens.append(imagem.public_url)
    return arr_links_imagens

def pegar_print(nome):
    folder_ref = storage.child("screenshots_suspeitos")
    for imagem in folder_ref.list_files():
        if imagem.name == nome:
            imagem.make_public()
            return imagem.public_url
    return "error"

def apagar_prints_existentes():
    folder_ref = storage.child("screenshots_suspeitos")
    for imagem in folder_ref.list_files():
        storage.delete(imagem.name)

def pegarForagidoPeloCpf(cpf):
    document = collection_ref.where('cpf', '==', cpf).get()
    snapshot = document[0]

    if snapshot == None:
        return False

    return snapshot.to_dict()

def adicionarPrintSuspeito(nome, nome_imagem):
    storage.child(nome).put(nome_imagem)

def adicionarImagensDeForagido():
    path_train = "dataset/"
    subdirs = [os.path.join(path_train, f) for f in os.listdir(path_train)]
    count = 0
    for subdir in subdirs:
        images_list = [os.path.join(subdir, f) for f in os.listdir(subdir)]
        for path in images_list:
            print(path)
            count+=1
            storage.child(f"dataset/{subdir}").put(path)