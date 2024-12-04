class Comentario:
    def __init__(self, id_comentario, texto):
        self.__id_comentario = id_comentario
        self.__texto = texto

    # GETTERS
    def get_id_comentario(self):
        return self.__id_comentario

    def get_texto(self):
        return self.__texto

    # SETTERS
    def set_id_comentario(self, novo_id_comentario):
        self.__id_comentario = novo_id_comentario

    def set_texto(self, novo_texto):
        self.__texto = novo_texto
