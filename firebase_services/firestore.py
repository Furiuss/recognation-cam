import firebase_admin
import pyrebase
from firebase_admin import firestore, credentials, storage
import uuid

myuuid = uuid.uuid4()
from firebase import firebase
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
# firebase = firebase.FirebaseApplication('<DATABASE_URL>', None)
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

# def adicionar

# def pegarCollection():
#     return collection_ref.get()

def pegarForagidoPeloId(id):
    snapshot = collection_ref.document(id).get()
    if snapshot == None:
        return False

    return snapshot.to_dict()
    # item = None
    # for key, val in snapshot:
    #     if val[key] == id:
    #         item = key
    #         break
    # if (item != None):
    #     node = db.collection.child(item)
    #     return node
    # else:
    #     return False

def armazenar_imagens_foragido(id):
    nome_pasta = id
    array_imagens_links = pegarImagensForagido(id)

    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)

    for nome_arquivo in array_imagens_links:
        caminho_arquivo = os.path.join(nome_pasta, nome_arquivo)
        storage.child()

def pegarImagensForagido(id):
    foragido = pegarForagidoPeloId(id)
    imagens_foragido = foragido['imagens']
    return imagens_foragido

def adicionarPrintSuspeito():
    storage.child("screenshots_suspeitos/70629522147").put("User.gustavo.286.jpg")

def adicionarImagensDeForagido():
    imagens = 2
    for imagem in imagens:
        storage.child("screenshots_suspeitos/70629522146").put("User.gustavo.286.jpg")

# create()
# print(pegarForagidoPeloId('70629522146'))
# read_collection()
# array = pegarImagensForagido('70629522146')
# for imagem in array:
#     print(imagem)
# adicionarPrintSuspeito()
# pegarTodasAsImagens()
# add_collection()
# armazenar_imagens_foragido('70629522146')

# data = date.today().strftime('%d/%m/%Y')
# foragido = Foragido(nome='Matcholas',
#                     data_nascimento=data,
#                     cpf='70629522126',
#                     created_at=data,
#                     eh_foragido=True)
# foragido.adicionarId()
# create(foragido)
# print(pegarForagidoPeloId(foragido.id))
