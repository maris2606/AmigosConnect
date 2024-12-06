class Postagem:
    def __init__(self, id_postagem, titulo, descricao, anexo, editada, status, fk_usuario_id, fk_categoria_id):
        self.__id_postagem = id_postagem
        self.__titulo = titulo
        self.__descricao = descricao
        self.__anexo = anexo
        self.__editada = editada
        self.__status = status
        self.__fk_usuario_id = fk_usuario_id
        self.__fk_categoria_id = fk_categoria_id

    # Getters
    def get_id_postagem(self):
        return self.__id_postagem

    def get_titulo(self):
        return self.__titulo

    def get_descricao(self):
        return self.__descricao

    def get_anexo(self):
        return self.__anexo

    def get_editada(self):
        return self.__editada

    def get_status(self):
        return self.__status

    def get_fk_usuario_id(self):
        return self.__fk_usuario_id

    def get_fk_categoria_id(self):
        return self.__fk_categoria_id

    # Setters
    def set_titulo(self, titulo):
        self.__titulo = titulo

    def set_descricao(self, descricao):
        self.__descricao = descricao

    def set_anexo(self, anexo):
        self.__anexo = anexo

    def set_editada(self, editada):
        self.__editada = editada

    def set_status(self, status):
        self.__status = status

    def set_fk_usuario_id(self, fk_usuario_id):
        self.__fk_usuario_id = fk_usuario_id

    def set_fk_categoria_id(self, fk_categoria_id):
        self.__fk_categoria_id = fk_categoria_id
