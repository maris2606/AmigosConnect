from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
from conexao import conexao_fechar, conexao_abrir
from arquivo import obter_usuario, salvar_usuario, salvar_connect, obter_id_usuario_por_nome,salvar_participantes_connect,obter_connect_pelo_id, obter_nomes_usuarios_do_connect, obter_mensagens_do_connect, salvar_mensagem
import sys
import os

# Adiciona o diretório pai de 'amigos_connect' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.Usuario import Usuario
from model.Connect import Connect
from model.Mensagem import Mensagem


app = Flask("Amigos_Connect")
app.secret_key = "uma_chave_secreta" 
con = conexao_abrir("localhost", "root", "Millena03*", "amigosconnect")

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/login.html")
def login(): 
    return render_template("login.html")

@app.route("/cadastro.html")
def cadastro(): 
    return render_template("cadastro.html")

@app.route("/criar-connect.html")
def cria_connect(): 
    return render_template("/criar-connect.html", usuario = session['usuario'], usuarios = obter_usuario(con), connect = obter_connect_pelo_id(con,1))

@app.route("/info-connect.html")
def info_connect(): 
    return render_template("info-connect.html")

@app.route("/participantes.html")
def mostrar_participantes(): 
    return render_template("participantes.html", usuario = session['usuario'])

@app.route("/chat.html")
def mostrar_chat(): 
    return render_template("chat.html", usuario = session['usuario'], connect = obter_connect_pelo_id(con,1), mensagens = obter_mensagens_do_connect(con, 1))

@app.route("/feed.html")
def feed():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template("feed.html", usuario = session['usuario'],connect = obter_connect_pelo_id(con,1))

@app.route("/politicas.html")
def politicas():
    return render_template("politicas.html")

@app.route("/termos.html")
def termos():
    return render_template("termos.html")

@app.route("/templates/participantes.html")
def participantes():
    return render_template("participantes.html", usuario = session['usuario'], participantes = obter_nomes_usuarios_do_connect(con,1))

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
        return render_template("login.html")
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
        return render_template("login.html")

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
     
    return render_template("/chat.html", usuario=session['usuario'], connect = obter_connect_pelo_id(con,1))

@app.route("/chat.html", methods=['POST'] )
def salvar_chat(): 
    data = request.get_json() 
    msg = data.get('msg') 
    mensagem = Mensagem(None,msg,'2024-12-11 00:00:00', session['usuario']['idUsuario'],1)
    salvar_mensagem(con,mensagem)
    return render_template("chat.html", usuario = session['usuario'], connect = obter_connect_pelo_id(con,1), mensagens = obter_mensagens_do_connect(con, 1))

conexao_fechar(con)

app.run(debug=True)