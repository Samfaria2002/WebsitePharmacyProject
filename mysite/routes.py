from flask import Blueprint, request, flash, session
from flask import render_template, jsonify, redirect
from extensions import db # p/ uso futuro em cenários de add/delete/update
from tables import Pharmacy, pharmacies_schema, User, users_schema, Remedy, remedies_schema
import datetime
from extensions import login_manager
from flask_login import login_user, login_required, current_user, logout_user

routes = Blueprint('routes', __name__)

@login_manager.user_loader
def load_user(userId):
    return User.query.get(int(userId))

@routes.route('/')
def index():
    return redirect('/home')

@routes.route('/home')
def home():
    return render_template('/app/home.html')

@routes.route('/estoque')
@login_required
def estoque():
    return render_template('/app/estoque.html')

@routes.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('/app/cadastro.html')
    elif request.method == 'POST':

        body = request.get_json()

        body['sex'] = body['sex'][0]
        body['userType'] = body['userType'].upper()

        #date = datetime.datetime(body['birthYear'], body['birthMonth'], body['birthDay'])
        newUser = User(userName=body['username'], password=body['password'], userType=body['userType'], name=body['name'], birthDate=body['data-nascimento'], sex=body['sex'], 
        email=body['email'], pharmacyId=body['pharmacyId'])

        db.session.add(newUser)
        db.session.commit()
        
        return jsonify('user criado com sucesso')
    else :
        return jsonify('Method not found')

@routes.route('/login')
def login():
    return render_template('/app/login.html')

@routes.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True

    user = User.query.filter_by(userName=username, userType='F').first()

    if not user or not user.password == password:
        flash('Revise suas credenciais e tente novamente')
        return redirect('/login')


    session['pharmacyId'] = user.pharmacyId
    login_user(user, remember=remember)
    return redirect('/estoque')

@routes.route('/logout')
@login_required
def logout():
    session.pop('pharmacyId', default=None)
    logout_user()
    return redirect('/login')


@routes.route('/solicitacoes')
@login_required
def solicitacoes():
    return render_template('/app/solicitacoes.html')

@routes.route('/error')
def err():
    return jsonify({'status': 'Not found hehe'}), 404


# *** Pharmacy routes *** -- add/edit via controle interno

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
        return jsonify('Farmácia criada')
    else:
        return jsonify('Method not found')

@routes.route('/api/pharmacy/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def specific_pharm(id):
    if request.method == 'GET':
        res = pharmacies_schema.dump(Pharmacy.query.filter_by(pharmacyId=id).one())
        return jsonify(res)
    elif request.method == 'DELETE':
        toDelete = Pharmacy.query.filter_by(pharmacyId=id).one()
        db.session.delete(toDelete)
        db.session.commit()
        return jsonify('F no chat')
    else:
        return jsonify('Method not found')

# *** Users routes ***
@routes.route('/api/user', methods=['GET'])
def generic_user():
    if request.method == 'GET':
        res = users_schema.dump(User.query.all())
        return jsonify(res)
    else:
        return jsonify('Method not found')

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
            return jsonify('senha não declarada')
        db.session.add(newUser)
        db.session.commit()
        return jsonify('update feito com sucesso')
    elif request.method == 'DELETE':
        toDelete = User.query.filter_by(userId=id).one()
        db.session.delete(toDelete)
        db.session.commit()
        return jsonify('F no chat')
    else:
        return jsonify('Method not found')


# *** Remedy routes *** GET -> p/ teste
@routes.route('/api/remedy', methods=['POST'])
def generic_remedy():
    #if request.method == 'GET':
    #    res = remedies_schema.dump(Remedy.query.all())
    #    return jsonify(res)
    if request.method == 'POST':
        body = request.get_json()
        print(body)
        pharmacyFromUser = session['pharmacyId']
        # barCode=body['barCode'], 
        newRemedy = Remedy(name=body['name'], laboratory=body['laboratory'], price=body['price'], pharmacyId=pharmacyFromUser, quantity=body['quantity'], unitType=body['unitType'])
        db.session.add(newRemedy)
        db.session.commit()
        return jsonify('criado com sucesso')
    else:
        return jsonify('Method not found')

@routes.route('/api/remedy/<int:id>', methods=['PUT', 'DELETE'])
def specific_remedy(id):
    if request.method == 'PUT':
        body = request.get_json()
        remedy = Remedy.query.filter_by(remedyId=id).one()
        # colocar outros campos q for alterar

        if('laboratory' in body):
            remedy.laboratory = body['laboratory']
        
        if('quantity' in body):
            remedy.quantity = body['quantity']
        
        if('price' in body):
            remedy.price = body["price"]
        #else:
        #    return jsonify('preço não declarado')
        db.session.add(remedy)
        db.session.commit()
        return jsonify('update feito com sucesso')
    elif request.method == 'DELETE':
        toDelete = Remedy.query.filter_by(remedyId=id).one()
        db.session.delete(toDelete)
        db.session.commit()
        return jsonify('F no chat')
    else:
        return jsonify('Method not found')


@routes.route('/api/remedy/<string:name>')
def filterRemedy(name):
    res = Pharmacy.query.join(Remedy, Pharmacy.pharmacyId == Remedy.pharmacyId).filter(Remedy.name.startswith(name))
    res = pharmacies_schema.dump(res)
    return jsonify(res)

# rota pra pegar tds remedy de uma pharm s/ especificar nome

# crud -> inventary, recipe, RecipeItem, Order, OrderItem

@routes.route('/api/remedy')
def teste():
    pharmacyFromUser = session['pharmacyId']
    res = remedies_schema.dump(Remedy.query.filter(Remedy.pharmacyId == pharmacyFromUser))
    return jsonify(res)