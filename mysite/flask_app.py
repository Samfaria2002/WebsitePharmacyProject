from decimal import Decimal
from flask import Flask, Blueprint
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, jsonify
from flask_assets import Environment, Bundle
import os
from dotenv import load_dotenv
import json

from flask_marshmallow import Marshmallow 


app = Flask(__name__)
ma = Marshmallow(app)

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
    * construir todo o banco de dados e criar os métodos via sqlAlchemy
        -- templates de banco feita
        -- começo de criação das tabelas
        -- definir arquivo separado p/ templates de tables
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


load_dotenv()  # take environment variables from .env.

app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=os.environ.get('DB_USERNAME'),
    password=os.environ.get('DB_PASSWORD'),
    hostname=os.environ.get('DB_HOSTNAME'),
    databasename=os.environ.get('DB_DBNAME'),
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@dataclass
class Pharmacy(db.Model):

  __tablename__ = "pharmacy"

  pharmacyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(99))
  logo = db.Column(db.String(999))
  pais = db.Column(db.String(100))
  uf = db.Column(db.String(2))
  cidade = db.Column(db.String(100))
  bairro = db.Column(db.String(100))
  rua = db.Column(db.String(100))
  numero_endereco = db.Column(db.String(6))
  #cep = db.Column(db.Numeric(8, asdecimal=False))
  cep = db.Column(db.Integer)
  latitude = db.Column(db.String(256))
  longitude = db.Column(db.String(256))
  #telefone

  def __init__ (self, pharmacyId, name, logo, pais, uf, cidade, bairro, rua, numero_endereco, cep, latitude, longitude):
    self.pharmacyId = pharmacyId
    self.name = name
    self.logo = logo
    self.pais = pais
    self.uf = uf
    self.cidade = cidade
    self.bairro = bairro
    self.rua = rua
    self.numero_endereco = numero_endereco
    self.cep = cep
    self.latitude = latitude
    self.longitude = longitude

class ProductSchema(ma.Schema):
  class Meta:
    fields = ('pharmacyId', 'name', 'logo', 'pais', 'uf', 'cidade', 'bairro', 'rua', 'numero_endereco', 'cep', 'latitude', 'longitude')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# db routes

@app.route('/teste')
def test_url():
    res = products_schema.dump(Pharmacy.query.all())
    print(res)
    return jsonify(res)


if __name__ == '__main__':
    db.create_all()
    print(Pharmacy.query.all())
    app.run()
    #app.run(host = "0.0.0.0", port = 5000, debug = True)