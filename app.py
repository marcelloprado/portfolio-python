#Arquivo principal do flask

import json
from flask import Flask, render_template

app = Flask(__name__)

def carregar_projetos():
    """ Carrega a lista de projetos do JSON."""
    with open('json/projetos.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/projetos")
def projetos():
    lista_projetos = carregar_projetos()
    return render_template("projetos.html", projetos=lista_projetos)

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/projeto/<int:id>")
def projeto_detalhe(id):
    lista_projetos = carregar_projetos()
    projeto = next((p for p in lista_projetos if p['id'] == id), None)

    if not projeto:
        return "Projeto não encontrado", 404

    return render_template("projetoViews.html", projeto=projeto)

if __name__ == '__main__':
    app.run(debug=True)
    
    #^ Para inicializar o ambiente virtual - venv\Scripts\activate
#^  Arquivo principal do Flask para rodar o portfólio - python app.py
