class Usuario:
    def __init__(self, id_usuario, email, nome_usuario, status, senha, nome):
        self.__id_usuario = id_usuario
        self.__email = email
        self.__nome_usuario = nome_usuario
        self.__status = status
        self.__senha = senha
        self.__nome = nome

    # Getters
    def get_id_usuario(self):
        return self.__id_usuario

    def get_email(self):
        return self.__email

    def get_nome_usuario(self):
        return self.__nome_usuario

    def get_status(self):
        return self.__status

    def get_senha(self):
        return self.__senha

    def get_nome(self):
        return self.__nome

    # Setters
    def set_email(self, email):
        self.__email = email

    def set_nome_usuario(self, nome_usuario):
        self.__nome_usuario = nome_usuario

    def set_status(self, status):
        self.__status = status

    def set_senha(self, senha):
        self.__senha = senha

    def set_nome(self, nome):
        self.__nome = nome
