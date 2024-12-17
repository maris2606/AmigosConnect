from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_session import Session
from datetime import datetime
from conexao import conexao_fechar, conexao_abrir
from arquivo import *
import sys
import os

# Adiciona o diretório pai de 'amigos_connect' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.Usuario import Usuario
from model.Connect import Connect
from model.Mensagem import Mensagem
from model.Calendario import Calendario



app = Flask("Amigos_Connect")
app.secret_key = "uma_chave_secreta" 
con = conexao_abrir("localhost", "root", "Jossana@0308", "amigosconnect")

app.config['SESSION_TYPE'] = 'filesystem'  # Ou use 'redis' para maior escalabilidade
app.config['SESSION_FILE_DIR'] = './flask_session'  # Diretório local para sessões
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

Session(app)

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/login.html")
def login(): 
    return render_template("login.html", erro='d-none')

@app.route("/cadastro.html")
def cadastro(): 
    return render_template("cadastro.html")

@app.route("/criar-connect.html")
def cria_connect(): 
    return render_template("/criar-connect.html", usuario = session['usuario'], usuarios = obter_usuario(con))

@app.route("/info-connect.html")
def info_connect(): 
    return render_template("info-connect.html", usuario = session['usuario'])

@app.route("/participantes.html")
def mostrar_participantes(): 
    return render_template("participantes.html", usuario = session['usuario'])

@app.route("/feed.html")
def feed():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template("feed.html", usuario = session['usuario'])

@app.route("/politicas.html")
def politicas():
    return render_template("politicas.html")

@app.route("/configuracoes.html")
def configuracoes():
    return render_template("configuracoes.html", usuario = session['usuario'] )

@app.route("/meus-connects.html")
def meus_connects():
    return render_template("meus-connects.html", usuario = session['usuario'], connects = obter_connects_por_usuario(con, session['usuario']['idUsuario'] ))

@app.route("/termos.html")
def termos():
    return render_template("termos.html")

@app.route("/cadastro.html", methods=['POST'])
def cadastrar():
    nome = request.form['nome'].strip()
    print(nome)
    usuario = request.form['usuario'].strip()
    email = request.form['email'].strip()
    senha = request.form['senha'].strip()
    confirma_senha = request.form['confirma-senha'].strip()
    status = True
    if senha == confirma_senha:
        usuario = Usuario(None, email, usuario, status, senha, nome)
        salvar_usuario(con, usuario)
        return render_template("login.html", erro='d-none')
    else: 
        return render_template("cadastro.html")

@app.route("/login.html", methods=['POST'])
def entrar():
    usuario = request.form['usuario'].strip()
    senha = request.form['senha'].strip()
    usuarios = obter_usuario(con)
    contem = False

    for u in usuarios:
        if (usuario == u['email'] or usuario == u['nomeUsuario']) and (senha == u['senha']):
            contem = True
            session['usuario'] = {
                'idUsuario': u['idUsuario'],               
                'email': u['email'],         
                'nomeUsuario': u['nomeUsuario'],  
                'nome': u['nome'],            
                'status': u['status'],        
            }
            print(session['usuario'])
            break
    if contem:
        return render_template("feed.html", usuario = session['usuario'])
    else: 
        return render_template("login.html", erro = 'd-block')



@app.route("/meus-connects.html", methods=['POST'])
def entrando_connect():
    id_connect = request.form['id_connect'].strip()
    session['connect'] = obter_connect_pelo_id(con,id_connect)

    datas_indisponiveis = buscar_datas_indisponiveis(con, session['connect']['idConnect'])
    return render_template("chat.html", usuario = session['usuario'], connect = session['connect'], mensagens = obter_mensagens_do_connect(con, session['connect']['idConnect']), datas_indisponiveis = datas_indisponiveis, enquetes = obter_informacoes_enquete_do_connect(con,session['connect']['idConnect']))

@app.route("/chat.html")
def mostrar_chat(): 
    datas_indisponiveis = buscar_datas_indisponiveis(con, session['connect']['idConnect'])
    return render_template("chat.html", usuario = session['usuario'], connect = session['connect'], mensagens = obter_mensagens_do_connect(con, session['connect']['idConnect']), datas_indisponiveis= datas_indisponiveis, enquetes = obter_informacoes_enquete_do_connect(con,session['connect']['idConnect']))

@app.route("/chat.html", methods=['POST'])
def salvar_chat(): 
    dados = request.get_json()  # Captura os dados JSON enviados
    msg = dados.get('msg')  # Pega a mensagem
    dataHora = dados.get('dataHora')  # Pega a data e hora

    if msg is not None: 
        mensagem = Mensagem(None,msg,dataHora, session['usuario']['idUsuario'], session['connect']['idConnect'])
        salvar_mensagem(con, mensagem)

    # Salvar calendário
    calendario = dados.get('datas')
    datas_formatadas = []
    if calendario is not None: 
        for data in calendario:
            data = data.replace(" ", "")
            data_obj = datetime.strptime(data, '%d/%m/%Y')  
            datas_formatadas.append(data_obj.strftime('%Y-%m-%d'))

    for data in datas_formatadas: 
        salvar_data_indisponivel(con, data, session['connect']['idConnect'])
    
    titulo_enquete = dados.get('titulo')
    alternativas_enquete = dados.get('alternativas')

    print(f'Título da Enquete: {titulo_enquete}')
    print(f'Alternativas da Enquete: {alternativas_enquete}')

    if(titulo_enquete is not None) and (alternativas_enquete is not None):
        salvar_enquete(con,titulo_enquete, session['usuario']['idUsuario'])
        salvar_connect_enquete(con, session['connect']['idConnect'], obter_ultima_enquete(con))
        for alternativa in alternativas_enquete: 
            ultima_enquete = obter_ultima_enquete(con)
            salvar_opcao(con,alternativa)
            salvar_opcao_enquete(con, obter_ultima_opcao(con), ultima_enquete)

    #manipulação das opções
    opcao_alterada = dados.get('idOpcaoAlterada')
    print(f'TESTE VOTOS: {opcao_alterada}')
    if opcao_alterada is not None: 
        atualizar_voto_opcao(con,opcao_alterada)

    datas_indisponiveis = buscar_datas_indisponiveis(con, session['connect']['idConnect'])
    return render_template("chat.html", usuario=session['usuario'], connect=session['connect'], mensagens=obter_mensagens_do_connect(con, session['connect']['idConnect']), datas_indisponiveis=datas_indisponiveis, enquetes = obter_informacoes_enquete_do_connect(con,session['connect']['idConnect']))

@app.route("/criar-connect.html", methods=['POST'])
def criar_connect():
    nome_connect = request.form['nome-connect'].strip()
    print(nome_connect)
    
    amigos = request.form['amigos_selecionados'].split(',')
    amigos = [amigo.replace('@', '').strip() for amigo in amigos]
    print(f"Amigos selecionados: {amigos}")
    id_participantes_connect = []
    
    for amigo in amigos:
        id_participante = obter_id_usuario_por_nome(con,amigo)
        if (id_participante is not None) and (type(id_participante) == int): 
            id_participantes_connect.append(id_participante)
    
    id_participantes_connect.append(session['usuario']['idUsuario'])
    print(f"ids: {id_participantes_connect}")
    
    foto = request.files['foto-connect']
    foto_conteudo = foto.read()
    
    connect = Connect(None, nome_connect, foto_conteudo, None)
    salvar_connect(con, connect)
    
    for id_p in id_participantes_connect:
        if type(id_p) == int:
            salvar_participantes_connect(con,id_p) 

    connect = obter_ultimo_connect(con)
    session['connect'] = connect 
    datas_indisponiveis = buscar_datas_indisponiveis(con, session['connect']['idConnect'])
    return render_template("/chat.html", usuario=session['usuario'], connect = obter_ultimo_connect(con), datas_indisponiveis = datas_indisponiveis, enquetes = obter_informacoes_enquete_do_connect(con,session['connect']['idConnect']))

@app.route("/templates/participantes.html")
def participantes():
    return render_template("participantes.html", usuario = session['usuario'], participantes = obter_nomes_usuarios_do_connect(con,session['connect']['idConnect']))

@app.route('/api/unavailable-dates', methods=['GET'])
def unavailable_dates():
    datas = buscar_datas_indisponiveis(con, session['connect']['idConnect'])
    return jsonify(datas)

conexao_fechar(con)

app.run(debug=True)