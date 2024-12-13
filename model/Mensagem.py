from datetime import datetime

class Mensagem: 

    def __init__(self,id_mensagem, texto_mensagem, data_envio, usuario, connect):
        self.__id_mensagem = id_mensagem
        self.__texto_mensagem = texto_mensagem
        self.__data_envio = data_envio
        self.__usuario = usuario #Objeto Usuário
        self.__connect = connect #objeto Connect 

#getters e setters
    def get_id_mensagem(self):
        return self.__id_mensagem

    def get_texto_mensagem(self):
        return self.__texto_mensagem

    def set_texto_mensagem(self, texto_mensagem):
        self.__texto_mensagem = texto_mensagem

    def get_data_envio(self):
        return self.__data_envio

    def set_data_envio(self, data_envio):
        self.__data_envio = data_envio

    def get_usuario(self):
        return self.__usuario

    def set_usuario(self, usuario):
        self.__usuario = usuario

    def get_connect(self):
        return self.__connect

    def set_connect(self, connect):
        self.__connect = connect