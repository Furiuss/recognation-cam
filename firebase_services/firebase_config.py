import os
# import pyrebase
#
# config = {
#   "apiKey": "AIzaSyB_o_0G_UCLJIxV1HkXjm3lEQHM-Iqhaww",
#   "authDomain": "face-recognation-tcc.firebaseapp.com",
#   "databaseURL": "https://face-recognation-tcc-default-rtdb.firebaseio.com",
#   "projectId": "face-recognation-tcc",
#   "storageBucket": "face-recognation-tcc.appspot.com",
#   "messagingSenderId": "868557823973",
#   "appId": "1:868557823973:web:bfb8b19c733dc5ec6a990c",
#   "measurementId": "G-6X71JB5FNT",
#   "serviceAccount": "serviceAccount.json",
#   "databaseURL": "https://face-recognation-tcc-default-rtdb.firebaseio.com"
# }
#
# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()
# storage.child("gustavo-teste.jpg").put("User.gustavo.286.jpg")
#
#

# from firebase import



# import firebase_admin
# from firebase_admin import db, credentials
#
# cred = credentials.Certificate("serviceAccount.json")
# firebase_admin.initialize_app(cred, {"databaseURL": "https://face-recognation-tcc-default-rtdb.firebaseio.com"})
#
# ref = db.reference("/foragidos")
# ref.set({
#     "nome": "André",
#     "idade": 19,
# })
# print(ref.get())


# Import the Firebase service
import firebase_admin
from firebase_admin import credentials, db, storage

# Other Modules
# import json
#
# # Load appsettings JSON file
# with open('appsettings.json', 'r') as json_file:
#      appsettings= json.load(json_file)

# Firebase-APIKey File
API_KEY_PATH = os.path.join(os.path.dirname(__file__), '/service_account.json')  # Add your API file path

# Initialize the default firebase app
certificate = credentials.Certificate(API_KEY_PATH)
# firebaseApp = firebase_admin.initialize_app(certificate, {'databaseURL': appsettings['DatabaseURL']})
firebaseApp = firebase_admin.initialize_app(certificate, {"databaseURL": "https://face-recognation-tcc-default-rtdb.firebaseio.com",
                                                          "storageBucket": "face-recognation-tcc.appspot.com"})


class ForagidosCollections():


    """Class to perform CRUD Operations with Firebase collection TODO"""

    def __init__(self):
        """ Collection reference for ToDo """
        # self.collection = db.reference(appsettings['TodoCollection'])
        self.collection = db.reference("/foragidos")
        self.bucket = storage.bucket()
        # self.key = appsettings['TodoCollectionUniqueKey']

    def __getSnapshot(self):
        """ Private method, It can access within class object
        To get snapshot of collection """
        return self.collection.get()

    def __findItem(self, id):
        """
            To find the item
            """
        snapshot = self.__getSnapshot()
        if snapshot == None:
            return False
        item = None
        for key, val in snapshot.items():
            if val[self.key] == id:
                item = key
                break
        if (item != None):
            node = self.collection.child(item)
            return node
        else:
            return False

    def adicionarForagido(self, content):
        """ To push/add new todo items into collection """

        path = os.path.join(os.path.dirname(__file__), '/User.gustavo.286.jpg')
        blob = self.bucket.blob(path)
        blob.upload_from_filename(path)
        content['imagens'] = self.getUrl()
        self.collection.push(content)
        # if self.key in content:
        #     if not self.__findItem(content[self.key]):
        #
        #         return True
        #     else:
        #         raise Exception("Item already exists")
        # else:
        #     raise Exception("Key {0} not found".format(self.key))

    def pegarTodosForagidos(self):
        """ To get the entire todo items list """
        return self.collection.get()
        # snapshot = self.__getSnapshot()
        # if snapshot == None:
        #     return []
        # todos = []
        # for key, val in snapshot.items():
        #     todos.append(val)
        # return todos

    def getUrl(self):
        imagem_Ref = storage.bucket()\
                            .get_blob(os.path.join(os.path.dirname(__file__),
                                                   '/User.gustavo.286.jpg'))
        imagem_Ref.make_public()
        url = imagem_Ref.public_url
        return url

    def pegarFotos(self):
        colecao = self.collection.get().to_dict()
        imagem = colecao["imagens"]
        print(imagem)

    def clearAllItems(self):
        """ To clear all nodes in the collection"""
        self.collection.delete()
        return True

    def updateTodoItem(self, id, content):
        """ To update existing todo item
            Return True
            If the key is not found then return false
         """
        itemMatchedNode = self.__findItem(id)
        if (itemMatchedNode == False):
            raise Exception("Item doesn't exists")
        itemMatchedNode.set(content)
        return True

    def deleteTodoItem(self, id):
        """ To delete item from the list
            Return True
            If the key is not found then return false
         """
        itemMatchedNode = self.__findItem(id)
        if (itemMatchedNode == False):
            raise Exception("Item doesn't exists")
        itemMatchedNode.delete()
        return True
