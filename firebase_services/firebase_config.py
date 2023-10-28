import os
import firebase_admin
from firebase_admin import credentials, db, storage

API_KEY_PATH = os.path.join(os.path.dirname(__file__), '../service_account.json')
certificate = credentials.Certificate(API_KEY_PATH)
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

        path = os.path.join(os.path.dirname(__file__), '../User.gustavo.286.jpg')
        blob = self.bucket.blob(path)
        blob.upload_from_filename(path)
        content['imagens'] = self.getUrl()
        self.collection.push(content)

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
                                                   '../User.gustavo.286.jpg'))
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

foragido = ForagidosCollections()
print(foragido.getUrl())