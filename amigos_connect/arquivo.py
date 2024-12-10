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
