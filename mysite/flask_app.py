from flask import Flask
from flask import render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

'''

    * possível refatoramento/abstração da base e do index/solicitacoes --> base c/ sidebar + content --> extend p/ --> base + logo c/ table que será usado p/ index e solicitacoes
    * criar dashboard de admin p/ visualização de user/req, etc
    * definir quais campos serão necessários para as tabelas do backend
    * construir todo o banco de dados e criar os métodos via sqlAlchemy
    * setar .env p/ esconder informações sigilosas >:D
    * botar a index do Little Samuca p/ rodar (em cima da rota '/')
    * preparar o mobile via react-native
    * mudar aquele btn de delete do modal depois
    * preparar pull request pro pythonanywhere

'''

@app.route('/')
def index():
    return render_template('/app/index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('/app/cadastro.html')

@app.route('/login')
def login():
    return render_template('/app/login.html')

@app.route('/solicitacoes')
def solicitacoes():
    return render_template('/app/solicitacoes.html')


@app.route('/error')
def err():
    return jsonify({'status': 'Not found hehe'}), 404

if __name__ == '__main__':
    # db.create_all()
    app.run(debug = True)
    #app.run(host = "0.0.0.0", port = 5000, debug = True)