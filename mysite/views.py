from flask import Blueprint
from flask import render_template, jsonify
from extensions import db # p/ uso futuro em cenários de add/delete/update
from tables import Pharmacy, pharmacies_schema

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('/app/index.html')

@views.route('/estoque')
def estoque():
    return render_template('/app/index.html')

@views.route('/cadastro')
def cadastro():
    return render_template('/app/cadastro.html')

@views.route('/login')
def login():
    return render_template('/app/login.html')

@views.route('/solicitacoes')
def solicitacoes():
    return render_template('/app/solicitacoes.html')

@views.route('/error')
def err():
    return jsonify({'status': 'Not found hehe'}), 404


@views.route('/teste')
def test_url():
    res = pharmacies_schema.dump(Pharmacy.query.all())
    return jsonify(res)
