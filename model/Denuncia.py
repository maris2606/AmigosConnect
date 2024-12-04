class Denuncia:
    def __init__(self, id_denuncia, descricao):
        self.__id_denuncia = id_denuncia
        self.__descricao = descricao

    # Métodos GETTERS
    def get_id_denuncia(self):
        return self.__id_denuncia

    def get_descricao(self):
       return self.__descricao

    # Métodos SETTERS
    def set_id_denuncia(self, novo_id_denuncia):
       self.__id_denuncia = novo_id_denuncia

    def set_descricao(self, nova_descricao):
        self.__descricao = nova_descricao
