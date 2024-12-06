from datetime import datetime

class Evento:
    def __init__(self, id_evento, data, horario, local, descricao):
        self.__id_evento = id_evento
        self.__data = datetime.strptime(data, "%Y-%m-%d").date()
        self.__horario = datetime.strptime(horario, "%H:%M:%S").time()
        self.__local = local
        self.__descricao = descricao

    # GETTERS
    def get_id_evento(self):
        return self.__id_evento

    def get_data(self):
        return self.__data

    def get_horario(self):
        return self.__horario

    def get_local(self):
        return self.__local

    def get_descricao(self):
        return self.__descricao

    # SETTERS
    def set_data(self, nova_data):
        self.__data = datetime.strptime(nova_data, "%Y-%m-%d").date()

    def set_horario(self, novo_horario):
        self.__horario = datetime.strptime(novo_horario, "%H:%M:%S").time()

    def set_local(self, novo_local):
        self.__local = novo_local

    def set_descricao(self, nova_descricao):
        self.__descricao = nova_descricao
