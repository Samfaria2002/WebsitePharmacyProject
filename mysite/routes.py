from flask import Blueprint, request
from flask import render_template, jsonify, redirect
from extensions import db # p/ uso futuro em cenários de add/delete/update
from tables import Pharmacy, pharmacies_schema, User, users_schema, Remedy, remedies_schema
import datetime

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


# Pharmacy routes -- add/edit via controle interno
@routes.route('/api/pharmacy', methods=['GET', 'POST'])
def generic_pharm():
    if request.method == 'GET':
        res = pharmacies_schema.dump(Pharmacy.query.all())
        return jsonify(res)
    elif request.method == 'POST':
        body = request.get_json()
        newPharmacy = Pharmacy(name=body['name'], logo=body['logo'], pais=body['pais'], uf=body['uf'], cidade=body['cidade'], bairro=body['bairro'], rua=body['rua'], 
        complemento=body['complemento'], latitude=body['latitude'], longitude=body['longitude'])

        db.session.add(newPharmacy)
        db.session.commit()
        return 'kek'
        #return jsonify(newPharmacy)
    else:
        return 'Method not found'

@routes.route('/api/pharmacy/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def specific_pharm(id):
    if request.method == 'GET':
        res = pharmacies_schema.dump(Pharmacy.query.filter_by(pharmacyId=id).one())
        return jsonify(res)
    #elif request.method == 'PUT':   
    #    body = request.get_json()
    #    pharm = Pharmacy.query.filter_by(pharmacyId=id).one()
    #    return 'upd'
    elif request.method == 'DELETE':
        toDelete = Pharmacy.query.filter_by(pharmacyId=id).one()
        db.session.delete(toDelete)
        db.session.commit()
        return 'F no chat'
    else:
        return 'Method not found'

# Users routes
@routes.route('/api/user', methods=['GET', 'POST'])
def generic_user():
    if request.method == 'GET':
        res = users_schema.dump(User.query.all())
        return jsonify(res)
    elif request.method == 'POST':
        body = request.get_json()
        print(body)

        date = datetime.datetime(body['birthYear'], body['birthMonth'], body['birthDay'])
        newUser = User(userName=body['userName'], password=body['password'], userType=body['userType'], name=body['name'], birthDate=date, sex=body['sex'], 
        email=body['email'], pharmacyId=body['pharmacyId'])

        db.session.add(newUser)
        db.session.commit()
        return jsonify('user criado com sucesso')
    else:
        return 'Method not found'

@routes.route('/api/user/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def specific_user(id):
    if request.method == 'GET':
        res = users_schema.dump(User.query.filter_by(userId=id).one())
        return jsonify(res)
    elif request.method == 'PUT':

        body = request.get_json()
        newUser = User.query.filter_by(userId=id).one()

        if('password' in body):
            newUser.password = body["password"]
        else:
            return 'senha não declarada'
        db.session.add(newUser)
        db.session.commit()
        return 'update feito com sucesso'
    elif request.method == 'DELETE':
        toDelete = User.query.filter_by(userId=id).one()
        db.session.delete(toDelete)
        db.session.commit()
        return 'F no chat'
    else:
        return 'Method not found'


# Remedy routes
@routes.route('/api/remedy', methods=['GET', 'POST'])
def generic_remedy():
    if request.method == 'GET':
        res = remedies_schema.dump(Remedy.query.all())
        return jsonify(res)
    elif request.method == 'POST':
        body = request.get_json()
        print(body)
        newRemedy = Remedy(name=body['name'], laboratory=body['laboratory'], price=body['price'], barCode=body['barCode'], pharmacyId=body['pharmacyId'], inventaryId=body['inventaryId'])
        db.session.add(newRemedy)
        db.session.commit()
        return 'criado com sucesso'
    else:
        return 'Method not found'
@routes.route('/api/remedy/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def specific_remedy(id):
    if request.method == 'GET':
        res = remedies_schema.dump(Remedy.query.filter_by(remedyId=id).one())
        return jsonify(res)
    elif request.method == 'PUT':

        body = request.get_json()
        remedy = Remedy.query.filter_by(remedyId=id).one()
        # colocar outros campos q for alterar
        if('price' in body):
            remedy.price = body["price"]
        else:
            return 'preço não declarado'
        db.session.add(remedy)
        db.session.commit()
        return 'update feito com sucesso'
    elif request.method == 'DELETE':
        toDelete = Remedy.query.filter_by(remedyId=id).one()
        db.session.delete(toDelete)
        db.session.commit()
        return 'F no chat'
    else:
        return 'Method not found'