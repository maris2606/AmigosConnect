from datetime import datetime

class Calendario: 
    def __init__(self, id_calendario, id_connect): 
        self.__id_calendario = id_calendario
        self.__id_connect = id_connect

#getters e setters
    def get_id_calendario(self):
        return self.__id_calendario

    def get_id_connect(self):
        return self.__id_connect

    