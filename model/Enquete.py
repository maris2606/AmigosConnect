class Enquete: 
    def __init__ (self, id_enquete, lista_opcoes):
        self.__id_enquete = id_enquete
        self.__lista_opcoes = lista_opcoes


#getters e setters
    def get_id_enquete(self):
        return self.__id_enquete

    def get_lista_opcoes(self):
        return self.__lista_opcoes
    
    def set_lista_opcoes(self, listaOpcoes):
        self.__lista_opcoes = listaOpcoes