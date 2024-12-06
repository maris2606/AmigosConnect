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