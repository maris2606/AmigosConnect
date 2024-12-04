class Categoria:
    def __init__(self, id_categoria, nome):
        self.__id_categoria = id_categoria
        self.__nome = nome

    # Getters
    def get_id_categoria(self):
        return self.__id_categoria

    def get_nome(self):
        return self.__nome

    # Setters
    def set_nome(self, nome):
        self.__nome = nome
