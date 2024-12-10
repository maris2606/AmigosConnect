class Connect:
    def __init__(self, id_connect, nome_connect, foto_connect, evento):
        self.__id_connect = id_connect
        self.__nome_connect = nome_connect
        self.__foto_connect = foto_connect  
        self.__evento = evento

    # Getters
    def get_id_connect(self):
        return self.__id_connect

    def get_nome_connect(self):
        return self.__nome_connect

    def get_foto_connect(self):
        return self.__foto_connect

    def get_fk_evento_id(self):
        return self.__evento

    # Setters
    def set_nome_connect(self, nome_connect):
        self.__nome_connect = nome_connect

    def set_foto_connect(self, foto_connect):
        self.__foto_connect = foto_connect

    def set_fk_evento_id(self, evento):
        self.__evento = evento

