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
    con.commit()

    if ultimo_connect and ultimo_connect['fotoConnect']: 
        # Converte a imagem em base64 
        ultimo_connect['fotoConnect'] = base64.b64encode(ultimo_connect['fotoConnect']).decode('utf-8')
    
    return ultimo_connect

def salvar_participantes_connect(con, participante):
    cursor = con.cursor()
    connect = obter_ultimo_connect(con)
    sql = 'INSERT INTO Connect_Usuario (fk_Connect_idConnect, fk_Usuario_idUsuario) VALUES (%s, %s)'
    valores = (connect['idConnect'], participante,)
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

import base64

def obter_connect_pelo_id(con, id_connect):
    cursor = con.cursor(dictionary=True)
    sql = """
        SELECT *
        FROM Connect
        WHERE idConnect = %s
    """
    cursor.execute(sql, (id_connect,))
    connect = cursor.fetchone()

    if connect and 'fotoConnect' in connect and connect['fotoConnect']:
        # Convertendo para Base64 e decodificando para string
        connect['fotoConnect'] = base64.b64encode(connect['fotoConnect']).decode('utf-8')

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
        SELECT M.idMensagem, M.textoMensagem, M.dataEnvio, U.nomeUsuario, U.idUsuario
        FROM Mensagem M
        JOIN Usuario U ON M.fk_Usuario_idUsuario = U.idUsuario
        WHERE M.fk_Connect_idConnect = %s
        ORDER BY M.dataEnvio
    """
    cursor.execute(sql, (id_connect,))  
    mensagens = []

    for registro in cursor:
        data_envio = registro['dataEnvio']
        hora_formatada = data_envio.strftime('%H:%M') if data_envio else None

        mensagens.append({
            'idMensagem': registro['idMensagem'],
            'textoMensagem': registro['textoMensagem'],
            'dataEnvio': hora_formatada,
            'nomeUsuario': registro['nomeUsuario'], 
            'idUsuario': registro['idUsuario']
        })

    return mensagens

def obter_connects_por_usuario(con, id_usuario):
    cursor = con.cursor(dictionary=True)
    sql = """
        SELECT 
            C.idConnect, 
            C.nomeConnect, 
            C.fotoConnect
        FROM 
            Connect C
        JOIN 
           Connect_Usuario UC ON C.idConnect = UC.fk_Connect_idConnect
        WHERE 
            UC.fk_Usuario_idUsuario = %s
    """
    cursor.execute(sql, (id_usuario,))
    connects = []

    for registro in cursor:
        connects.append({
            'idConnect': registro['idConnect'],
            'nomeConnect': registro['nomeConnect'],
            'fotoConnect': registro['fotoConnect']
        })

    return connects

def salvar_data_indisponivel(con, data_indisponivel, id_connect):
    cursor = con.cursor()

    sql = 'INSERT INTO Datas_indisponiveis (dataIndisponivel, fk_Connect_idConnect) VALUES (%s, %s)'
    
    valores = (
        data_indisponivel,      
        id_connect,
    )

    cursor.execute(sql, valores)
    con.commit()
    cursor.close()

def buscar_datas_indisponiveis(con, id_connect):
    cursor = con.cursor()
    sql = 'SELECT dataIndisponivel FROM Datas_indisponiveis WHERE fk_Connect_idConnect = %s'
    valores = (id_connect,)
    cursor.execute(sql, valores)
    
    resultados = cursor.fetchall()
    datas_indisponiveis = [resultado[0].strftime('%Y-%m-%d') for resultado in resultados]
    cursor.close()
    
    return datas_indisponiveis

#salvar enquetes

def salvar_enquete(con, nomeEnquete, idUsuario):
    cursor = con.cursor()
    sql = 'INSERT INTO Enquete (nomeEnquete,fk_Usuario_idUsuario) VALUES (%s, %s)'
    valores = (nomeEnquete,idUsuario)
    cursor.execute(sql,valores)
    con.commit()
    cursor.close()

def obter_ultima_enquete(con):
    cursor = con.cursor(dictionary=True)
    sql = "SELECT * FROM Enquete ORDER BY idEnquete DESC LIMIT 1"
    cursor.execute(sql)

    ultima_enquete = cursor.fetchone()  
    con.commit()

    return ultima_enquete['idEnquete']

def salvar_opcao(con, texto_opcao):
    cursor = con.cursor()
    sql = 'INSERT INTO Opcao (numVotos, textoOpcao) VALUES (%s, %s)'
    valores = (0, texto_opcao)  # Inicialmente, numVotos é 0
    cursor.execute(sql, valores)
    con.commit()
    cursor.close()

def obter_ultima_opcao(con):
    cursor = con.cursor(dictionary=True)
    sql = "SELECT * FROM Opcao ORDER BY idOpcao DESC LIMIT 1"
    cursor.execute(sql)

    ultima_opcao = cursor.fetchone()  
    con.commit()

    return ultima_opcao['idOpcao']

def salvar_connect_enquete(con, id_connect, id_enquete):
    cursor = con.cursor()
    sql = 'INSERT INTO Connect_Enquete (fk_Connect_idConnect, fk_Enquete_idEnquete) VALUES (%s, %s)'
    valores = (id_connect, id_enquete)
    cursor.execute(sql, valores)
    con.commit()
    cursor.close()


def salvar_opcao_enquete(con, id_opcao, id_enquete):
    cursor = con.cursor()
    sql = 'INSERT INTO Opcao_Enquete (fk_Opcao_idOpcao, fk_Enquete_idEnquete) VALUES (%s, %s)'
    valores = (id_opcao, id_enquete)
    cursor.execute(sql, valores)
    con.commit()
    cursor.close()


def obter_opcoes_por_enquete(con, id_enquete):
    cursor = con.cursor(dictionary=True)
    sql = """
        SELECT O.idOpcao, O.textoOpcao, O.numVotos
        FROM Opcao O
        JOIN Opcao_Enquete OE ON O.idOpcao = OE.fk_Opcao_idOpcao
        WHERE OE.fk_Enquete_idEnquete = %s
    """
    cursor.execute(sql, (id_enquete,))
    opcoes = []

    for registro in cursor:
        opcoes.append({
            'idOpcao': registro['idOpcao'],
            'textoOpcao': registro['textoOpcao'],
            'numVotos': registro['numVotos']
        })
    
    cursor.close()
    return opcoes


#votos
def atualizar_voto_opcao(con, id_opcao):
    cursor = con.cursor()
    sql = 'UPDATE Opcao SET numVotos = numVotos + 1 WHERE idOpcao = %s'
    cursor.execute(sql, (id_opcao,))
    con.commit()
    cursor.close()

def obter_informacoes_enquete_do_connect(con, id_connect):
    cursor = con.cursor(dictionary=True)
    
    # Consulta para obter as informações da enquete e suas opções associadas ao id_connect
    query = """
    SELECT e.idEnquete, e.nomeEnquete, e.fk_Usuario_idUsuario, o.idOpcao, o.textoOpcao, o.numVotos
    FROM Enquete e
    INNER JOIN Connect_Enquete ce ON e.idEnquete = ce.fk_Enquete_idEnquete
    INNER JOIN Opcao_Enquete oe ON e.idEnquete = oe.fk_Enquete_idEnquete
    INNER JOIN Opcao o ON oe.fk_Opcao_idOpcao = o.idOpcao
    WHERE ce.fk_Connect_idConnect = %s
    """
    
    cursor.execute(query, (id_connect,))
    resultados = cursor.fetchall()
    
    enquetes = []
    for resultado in resultados:
        # Verifica se a enquete já foi adicionada à lista
        enquete = next((e for e in enquetes if e['idEnquete'] == resultado['idEnquete']), None)
        if not enquete:
            # Se não encontrou, adiciona uma nova enquete
            enquete = {
                'idEnquete': resultado['idEnquete'],
                'idUsuario': resultado['fk_Usuario_idUsuario'],
                'nomeEnquete': resultado['nomeEnquete'],
                'opcoes': []
            }
            enquetes.append(enquete)
        
        # Adiciona a opção à enquete
        enquete['opcoes'].append({
            'idOpcao': resultado['idOpcao'],
            'textoOpcao': resultado['textoOpcao'],
            'numVotos': resultado['numVotos']
        })
    
    cursor.close()
    
    return enquetes