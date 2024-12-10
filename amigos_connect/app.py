from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
from conexao import conexao_fechar, conexao_abrir
from arquivo import obter_usuario, salvar_usuario, salvar_connect
import sys
import os

# Adiciona o diretório pai de 'amigos_connect' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.Usuario import Usuario
from model.Connect import Connect


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
    return render_template("/criar-connect.html", usuario = session['usuario'], usuarios = obter_usuario(con))

@app.route("/info-connect.html")
def info_connect(): 
    return render_template("info-connect.html")

@app.route("/participantes.html")
def mostrar_participantes(): 
    return render_template("participantes.html", usuario = session['usuario'])

@app.route("/chat.html")
def mostrar_chat(): 
    return render_template("chat.html", usuario = session['usuario'])

@app.route("/feed.html")
def feed():
    # Verifica se o usuário está logado
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template("feed.html")

@app.route("/politicas.html")
def politicas():
    return render_template("politicas.html")

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

@app.route("/criar-connect.html", methods = ['POST'])
def criar_connect(): 
    nome_connect = request.form['nome-connect'].strip()
    print(nome_connect)
    foto = request.files['foto-connect']
    foto_conteudo = foto.read()
    #amigos_select = request.form.getlist('amigos_select')
    connect = Connect(None,nome_connect,foto_conteudo,None)
    salvar_connect(con,connect)
    return render_template("/chat.html", usuario = session['usuario'])

conexao_fechar(con)

app.run(debug=True)