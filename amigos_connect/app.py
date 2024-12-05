from flask import Flask, app , render_template, request
from datetime import datetime

app = Flask("Amigos_Connect") 

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/login")
def login(): 
    return render_template("login.html")

@app.route("/cadastro")
def cadastro(): 
    return render_template("cadastro.html")

app.run()
