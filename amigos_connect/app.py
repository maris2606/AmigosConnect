from flask import Flask, app , render_template, request
from datetime import datetime
from conexao import conexao_fechar, conexao_abrir
from arquivo import obter_usuario, salvar_usuario
import sys
import os
# Adiciona o diretório pai de 'amigos_connect' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.Usuario import Usuario

app = Flask("Amigos_Connect")
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

@app.route("/feed.html")
def feed():
    return render_template("feed.html")

@app.route("/politicas.html")
def politicas():
    return render_template("politicas.html")

@app.route("/termos.html")
def termos():
    return render_template("termos.html")

@app.route("/cadastro.html", methods = ['POST'])
def cadastrar():
    nome = request.form['nome'].strip()
    usuario = request.form['usuario'].strip()
    email = request.form['email'].strip()
    # telefone = request.form['telefone'].strip()
    senha = request.form['senha'].strip()
    confirma_senha = request.form['confirma-senha'].strip()
    status = True
    if senha==confirma_senha:
        usuario = Usuario(None,email,usuario,status,senha,nome)
        salvar_usuario(con,usuario)
        return render_template("login.html")
    else: 
        #tem que arrumar aqui, pq tem que jogar mensagem falando que as senhas são !=
        return render_template("cadastro.html")

@app.route("/login.html", methods = ['POST'])
def entrar():
    #puxando do forms 
    usuario = request.form['usuario'].strip()
    senha = request.form['senha'].strip()
    #pegando do arquivo
    usuarios = obter_usuario(con)
    contem = False 

    #percorrendo a lista e comparando
    for u in usuarios: 
        if (usuario == u['email'] or usuario == u['nomeUsuario'] ) and (senha == u['senha']):
            contem = True        
    if contem: 
        return render_template ("feed.html")
    else: 
        return render_template ("login.html")

conexao_fechar(con)
app.run()