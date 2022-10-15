from flask import Flask
from flask import render_template, jsonify
from flask_assets import Environment, Bundle

app = Flask(__name__)

assets = Environment(app)
#assets.url = app.static_url_path
# static/stylesheet/
base = Bundle('stylesheet/base-file.scss', filters='pyscss,cssmin', output='stylesheet/base-file.css')
main = Bundle('stylesheet/main.scss', filters='pyscss,cssmin', output='stylesheet/main.css')
assets.register('base_scss', base)
assets.register('main_scss', main)


'''

    * possível refatoramento/abstração da base e do index/solicitacoes --> base c/ sidebar + content --> extend p/ --> base + logo c/ table que será usado p/ index e solicitacoes --ok
    * criar dashboard de admin p/ visualização de user/req, etc
    * definir quais campos serão necessários para as tabelas do backend -- ok
    * construir todo o banco de dados e criar os métodos via sqlAlchemy -- templates de banco feita, falta sqlAlchemy
    * setar .env p/ esconder informações sigilosas >:D
    * botar a index do Little Samuca p/ rodar (em cima da rota '/')
    * preparar o mobile via react-native
    * mudar aquele btn de delete do modal depois
    * preparar pull request pro pythonanywhere -- mais ou menos feito
    * utilização de scss p/ facilidade de utilização de styles -- ok

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




''' Banco de dados  '''











# db routes

@app.route('/teste')
def test_url():
    #data = Teste.query.all() # considerar passar var p/ jsonify após "limpeza" do que será enviado
    #return jsonify(data = Teste.query.all())
    return jsonify({'status': 'ok'})




if __name__ == '__main__':
    # db.create_all()
    app.run(debug = True)
    #app.run(host = "0.0.0.0", port = 5000, debug = True)