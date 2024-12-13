import base64

def obter_usuario(con):
    cursor = con.cursor()
    sql = "SELECT * FROM Usuario"
    cursor = con.cursor(dictionary=True)
    cursor.execute(sql)

    usuarios = []

    for (registro) in cursor:
        usuarios.append(registro)

    return usuarios

def salvar_usuario(con, usuario):
    cursor = con.cursor()

    sql = 'INSERT INTO Usuario (nome, email, nomeUsuario, status, senha) VALUES (%s, %s, %s, %s, %s)'
    
    valores = (
        usuario.get_nome(),
        usuario.get_email(),
        usuario.get_nome_usuario(),
        usuario.get_status(),
        usuario.get_senha()
    )

    cursor.execute(sql, valores)

    con.commit()

    cursor.close()

def obter_id_usuario_por_nome(con, nome_usuario):
    cursor = con.cursor(dictionary=True)
  
    sql = "SELECT idUsuario FROM Usuario WHERE nomeUsuario = %s"
    cursor.execute(sql, (nome_usuario,))

    usuario = cursor.fetchone()  

    if usuario:
        return usuario['idUsuario']
    else:
        return None  

def salvar_connect(con, connect):
    cursor = con.cursor()

    sql = 'INSERT INTO Connect (nomeConnect, fotoConnect) VALUES (%s, %s)'
    
    valores = (
        connect.get_nome_connect(),
        connect.get_foto_connect()
    )

    cursor.execute(sql, valores)

    con.commit()

    cursor.close()

def salvar_mensagem(con, mensagem):
    cursor = con.cursor()

    sql = 'INSERT INTO Mensagem (textoMensagem, dataEnvio, fk_Usuario_idUsuario, fk_Connect_idConnect) VALUES (%s, %s, %s, %s)'
    
    valores = (
        mensagem.get_texto_mensagem(),
        mensagem.get_data_envio(),
        mensagem.get_usuario(),
        mensagem.get_connect()
    )

    cursor.execute(sql, valores)

    con.commit()

    cursor.close()


def obter_ultimo_connect(con):
    cursor = con.cursor(dictionary=True)
    sql = "SELECT * FROM Connect ORDER BY idConnect DESC LIMIT 1"
    cursor.execute(sql)

    ultimo_connect = cursor.fetchone()

    return ultimo_connect['idConnect']

def salvar_participantes_connect(con, participante):
    cursor = con.cursor()
    id_connect = obter_ultimo_connect(con)
    sql = 'INSERT INTO Connect_Usuario (fk_Connect_idConnect, fk_Usuario_idUsuario) VALUES (%s, %s)'
    valores = (id_connect, participante,)
    cursor.execute(sql, valores)

    cursor.close()
    con.commit()

def obter_nome_connect(con, id_usuario):
    cursor = con.cursor(dictionary=True)  
    sql = """
        SELECT C.nomeConnect
        FROM Connect_Usuario CU
        JOIN Connect C ON CU.fk_Connect_idConnect = C.idConnect
        WHERE CU.fk_Usuario_idUsuario = %s
    """
    cursor.execute(sql, (id_usuario,))  
    nomes_connect = []

    for registro in cursor:
        nomes_connect.append(registro['nomeConnect'])  

    return nomes_connect

def obter_connect_pelo_id(con, id_connect):
    cursor = con.cursor(dictionary=True)  
    sql = """
        SELECT *
        FROM Connect
        WHERE idConnect = %s
    """
    cursor.execute(sql, (id_connect,))  
    connect = cursor.fetchone()  

    connect['fotoConnect'] = base64.b64encode(connect['fotoConnect'])

    return connect

def obter_nomes_usuarios_do_connect(con, id_connect):
    cursor = con.cursor(dictionary=True) 
    sql = """
        SELECT U.nomeUsuario
        FROM Connect_Usuario CU
        JOIN Usuario U ON CU.fk_Usuario_idUsuario = U.idUsuario
        WHERE CU.fk_Connect_idConnect = %s
    """
    cursor.execute(sql, (id_connect,))  
    
    nomes_usuarios = []

    for registro in cursor:
        nomes_usuarios.append(registro['nomeUsuario'])  

    return nomes_usuarios

def obter_mensagens_do_connect(con, id_connect):
    cursor = con.cursor(dictionary=True)  
    sql = """
        SELECT M.idMensagem, M.textoMensagem, M.dataEnvio, U.nomeUsuario
        FROM Mensagem M
        JOIN Usuario U ON M.fk_Usuario_idUsuario = U.idUsuario
        WHERE M.fk_Connect_idConnect = %s
        ORDER BY M.dataEnvio
    """
    cursor.execute(sql, (id_connect,))  
    mensagens = []

    for registro in cursor:
        mensagens.append({
            'idMensagem': registro['idMensagem'],
            'textoMensagem': registro['textoMensagem'],
            'dataEnvio': registro['dataEnvio'],
            'nomeUsuario': registro['nomeUsuario']
        })

    return mensagens