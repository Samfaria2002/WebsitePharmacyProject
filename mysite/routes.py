from flask import Blueprint, request
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


# Pharmacy routes

# setar crud

@routes.route('/teste', methods=['GET', 'POST'])
def test_url():
    print('bla', request.method)
    if request.method == 'GET':
        res = pharmacies_schema.dump(Pharmacy.query.all())
        return jsonify(res)
    elif request.method == 'POST':
        body = request.get_json()
        print(body)
        newPharmacy = Pharmacy(name='teste 2', logo='https://analise-tecnica.vercel.app/vercel.svg', pais='Brasil', uf='MG', cidade='Contagem')
        return jsonify(newPharmacy)
    else:
        return 'Method not found'

@routes.route('/teste/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def crud_pharmacy(id):
    if request.method == 'GET':
        res = pharmacies_schema.dump(Pharmacy.query.filter_by(pharmacyId=id).one())
        return jsonify(res)
    elif request.method == 'PUT':

        body = request.get_json()
        pharm = Pharmacy.query.filter_by(name='teste').one()

        if('nome' in body):
            pharm.nome = body["nome"]
        if ('email' in body):
            pharm.email = body["email"]
        if('empresa' in body):
            pharm.empresa = body["empresa"]
        
        return 'upd'
    elif request.method == 'DELETE':
        return 'delet'
    else:
        return 'Method not found'


# p /teste

@routes.route('/teste-add')
def add_url():
    newPharmacy = Pharmacy(name='teste 2', logo='https://analise-tecnica.vercel.app/vercel.svg', pais='Brasil', uf='MG', cidade='Contagem')
    #me = User('admin', 'admin@example.com')
    db.session.add(newPharmacy)
    db.session.commit()
    return 'o pai é bom'

@routes.route('/teste-update')
def update_url():
    thisPharm = Pharmacy.query.filter_by(name='teste').one()
    thisPharm.cidade = 'Ibirité'
    db.session.add(thisPharm)
    db.session.commit()
    return 'dale'

@routes.route('/teste-delete')
def delete_url():
    toDelete = Pharmacy.query.filter_by(name='teste 2').one()
    db.session.delete(toDelete)
    db.session.commit()
    return 'F no chat'
