class Connect:
    def __init__(self, id_connect, usuario, evento):
        self.__id_connect = id_connect
        self.__usuario= usuario
        self.__evento = evento

    # Getters
    def get_id_connect(self):
        return self.__id_connect

    def get_fk_usuario_id(self):
        return self.__usuario

    def get_fk_evento_id(self):
        return self.__evento

    # Setters
    def set_fk_usuario_id(self, usuario):
        self.__usuario = usuario

    def set_fk_evento_id(self, evento):
        self.__evento = evento
