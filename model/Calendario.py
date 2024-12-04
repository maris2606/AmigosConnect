from datetime import datetime

class Calendario: 
    def __init__(self, id_calendario, data_indisponivel): 
        self.__id_calendario = id_calendario
        self.__data_indisponivel = datetime.strptime(data_indisponivel, "%Y-%m-%d").date()

#getters e setters
    def get_id_calendario(self):
        return self.__id_calendario

    def get_data_indisponivel(self):
        return self.__data_indisponivel

    def set_data_indisponivel(self, data_indisponivel):
        self.__data_indisponivel = datetime.strptime(data_indisponivel, "%Y-%m-%d").date()