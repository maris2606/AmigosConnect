class Opcao:
    def __init__(self, id_opcao, num_votos, texto_opcao):
        self.__id_opcao = id_opcao
        self.__num_votos = num_votos
        self.__texto_opcao = texto_opcao
    
    #getters e setters
    def get_id_opcao(self):
        return self.__id_opcao

    def get_num_votos(self):
        return self.__num_votos
    
    def set_num_votos(self, num_votos):
        self.__num_votos = num_votos

    def get_texto_opcao(self):
        return self.__texto_opcao
    
    def set_texto_opcao(self, texto_opcao):
        self.__texto_opcao = texto_opcao