import uuid

class Foragido:
    def __init__(self, nome, data_nascimento, cpf, created_at, updated_at=None, eh_foragido = True):
        self.id = ''
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.eh_foragido = eh_foragido
        self.created_at = created_at
        self.updated_at = updated_at
        self.imagens = []

    def adicionarImagens(self, arrayImagens):
        for imagem in arrayImagens:
            self.imagens.append(imagem)

    def adicionarId(self):
        if self.id == '':
            self.id = str(uuid.uuid4())