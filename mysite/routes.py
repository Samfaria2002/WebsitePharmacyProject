from flask import Blueprint
from flask import render_template, jsonify, redirect
from extensions import db # p/ uso futuro em cenários de add/delete/update
from tables import Pharmacy, pharmacies_schema

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return redirect('/home')

@routes.route('/home')
def home():
    return render_template('/app/home.html')

@routes.route('/estoque')
def estoque():
    return render_template('/app/estoque.html')

@routes.route('/cadastro')
def cadastro():
    return render_template('/app/cadastro.html')

@routes.route('/login')
def login():
    return render_template('/app/login.html')

@routes.route('/solicitacoes')
def solicitacoes():
    return render_template('/app/solicitacoes.html')

@routes.route('/error')
def err():
    return jsonify({'status': 'Not found hehe'}), 404


@routes.route('/teste')
def test_url():
    res = pharmacies_schema.dump(Pharmacy.query.all())
    return jsonify(res)
