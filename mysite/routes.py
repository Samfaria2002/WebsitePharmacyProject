from flask import Blueprint, request, flash, session
from flask import render_template, jsonify, redirect
from extensions import db # p/ uso futuro em cenários de add/delete/update
from tables import Pharmacy, pharmacies_schema, User, users_schema, Remedy, remedies_schema, Order, orders_schema, OrderItem, pedidos_schema
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

@routes.route('/servicos')
def servicos():
    return render_template('/app/servicos.html')

@routes.route('/estoque')
@login_required
def estoque():
    return render_template('/app/estoque.html', name = current_user.userName)

@routes.route('/solicitacoes')
@login_required
def solicitacoes():
    return render_template('/app/solicitacoes.html', name = current_user.userName)

@routes.route('/error')
def err():
    return jsonify({'status': 'Not found hehe'}), 404

@routes.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('/app/cadastro.html')
    elif request.method == 'POST':

        body = request.get_json()

        if len(body['username']) <= 3:
            return jsonify('insira um nome de usuário maior')
        
        # 4 só pra ser feliz :D
        if len(body['password']) < 4:
            return jsonify('Insira uma senha com no minimo 4 caracteres')

        if body['password'] != body['password-confirm']:
            return jsonify('as senhas precisam ser iguais')
        

        body['sex'] = body['sex'][0]
        body['userType'] = body['userType'].upper()

        findUser = User.query.filter_by(userName=body['username'], userType=body['userType']).first()

        if findUser:
            return jsonify('usuário já existe'), 400

        userPharm = session.get('pharmacyId', None)
        if userPharm == None and not body['pharmacyId']: userPharm = body['pharmacyId']

        newUser = User(userName=body['username'], password=body['password'], userType=body['userType'], name=body['name'], birthDate=body['data-nascimento'], sex=body['sex'], 
        email=body['email'], pharmacyId=userPharm)

        db.session.add(newUser)
        db.session.commit()
        
        return jsonify('usuário criado com sucesso'), 200
    else :
        return jsonify('Method not found'), 400

@routes.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':

        if current_user.is_authenticated:
            return redirect('/estoque')

        return render_template('/app/login.html')
    else :

        username = request.form.get('username')
        password = request.form.get('password')

        if request.args.get('ismobile') == 'true':

            body = request.get_json()

            isMobile = True
            tipoDeUser = 'C'
            username = body['username']
            password = body['password']
        else:
            isMobile = False
            tipoDeUser = 'F'

        user = User.query.filter_by(userName=username, userType=tipoDeUser).first()

        if not user or not user.password == password:
            strErr = 'Revise suas credenciais e tente novamente'
            if isMobile:
                return jsonify(strErr), 400
            else:
                flash(strErr)
                return redirect('/login')


        session['pharmacyId'] = user.pharmacyId

        if isMobile:
            return jsonify(user.userId), 200
        else :
            login_user(user, remember=True)
            return redirect('/estoque')

@routes.route('/logout')
@login_required
def logout():
    session.pop('pharmacyId', default=None)
    logout_user()
    return redirect('/login')


# *** Pharmacy routes *** -- add/edit via controle interno

@routes.route('/api/pharmacy', methods=['GET', 'POST'])
def generic_pharm():
    if request.method == 'GET':
        res = pharmacies_schema.dump(Pharmacy.query.all())
        return jsonify(res), 200
    elif request.method == 'POST':
        body = request.get_json()
        newPharmacy = Pharmacy(name=body['name'], logo=body['logo'], pais=body['pais'], uf=body['uf'], cidade=body['cidade'], bairro=body['bairro'], rua=body['rua'], 
        complemento=body['complemento'], latitude=body['latitude'], longitude=body['longitude'])

        db.session.add(newPharmacy)
        db.session.commit()
        return jsonify('Farmácia criada'), 200
    else:
        return jsonify('Method not found'), 400

@routes.route('/api/pharmacy/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def specific_pharm(id):
    if request.method == 'GET':
        res = pharmacies_schema.dump(Pharmacy.query.filter_by(pharmacyId=id).one())
        return jsonify(res), 200
    elif request.method == 'DELETE':
        toDelete = Pharmacy.query.filter_by(pharmacyId=id).one()
        db.session.delete(toDelete)
        db.session.commit()
        return jsonify('F no chat'), 200
    else:
        return jsonify('Method not found'), 400

# *** Users routes ***
@routes.route('/api/user', methods=['GET'])
def generic_user():
    if request.method == 'GET':
        res = users_schema.dump(User.query.all())
        return jsonify(res), 200
    else:
        return jsonify('Method not found'), 400

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


# *** Remedy routes ***

@routes.route('/api/remedy', methods=['POST'])
def addRemedy():
    if request.method == 'POST':
        body = request.get_json()
        #print(body)
        pharmacyFromUser = session.get('pharmacyId', False)
        if pharmacyFromUser == False: return jsonify({"msg": 'sem farmácia declarada', "error": True }), 400

        try:
            body['price'] = float(body['price'])
        except:
            return jsonify({"msg": 'o campo preço não é um número', "error": True }), 400
        
        try:
            body['quantity'] = int(body['quantity'])
        except:
            return jsonify({"msg": 'o campo quantidade não é um número', "error": True }), 400 

        # barCode=body['barCode'], 
        newRemedy = Remedy(name=body['name'], laboratory=body['laboratory'], price=body['price'], pharmacyId=pharmacyFromUser, quantity=body['quantity'], unitType=body['unitType'])
        db.session.add(newRemedy)
        db.session.commit()

        res = {
            "msg": 'produto feito com sucesso',
            "data": remedies_schema.dump(remedies_schema.dump(Remedy.query.filter(Remedy.remedyId == newRemedy.remedyId)))
        }
        return jsonify(res), 200
    else:
        return jsonify('Method not found'), 400

@routes.route('/api/remedy/<int:id>', methods=['PUT', 'DELETE'])
def specific_remedy(id):
    if request.method == 'PUT':
        body = request.get_json()
        remedy = Remedy.query.filter_by(remedyId=id).one()
        # colocar outros campos q for alterar

        try:
            body['price'] = float(body['price'])
        except:
            return jsonify({"msg": 'o campo preço não é um número', "error": True }), 400
        try:
            body['quantity'] = int(body['quantity'])
        except:
            return jsonify({"msg": 'o campo quantidade não é um número', "error": True }), 400 

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

        res = {
            "msg": 'update feito com sucesso',
            "data": remedies_schema.dump(remedies_schema.dump(Remedy.query.filter(Remedy.remedyId == id)))
        }

        return jsonify(res), 200
    elif request.method == 'DELETE':

        try:
            toDelete = Remedy.query.filter_by(remedyId=id).one()
            db.session.delete(toDelete)
            db.session.commit()
            return jsonify('F no chat'), 200
        except:
            return jsonify('Não foi possível deletar esse Item. Confira se há uma solicitação em aberto com esse item e tente novamente'), 400
    else:
        return jsonify('Method not found'), 400

@routes.route('/api/remedy')
def getRemedy():
    pharmacyFromUser = session.get('pharmacyId', False)
    if pharmacyFromUser == False: return jsonify('sem farmácia declarada'), 400
    res = remedies_schema.dump(Remedy.query.filter(Remedy.pharmacyId == pharmacyFromUser))
    return jsonify(res), 200

@routes.route('/api/remedy/<string:name>')
def filterRemedy(name):
    res = Pharmacy.query.join(Remedy, Pharmacy.pharmacyId == Remedy.pharmacyId).filter(Remedy.name.startswith(name))
    res = pharmacies_schema.dump(res)
    return jsonify(res), 200

# rota pra pegar tds remedy de uma pharm s/ especificar nome

# *** Order (vulgo pedido) ***
@routes.route('/api/order', methods=['GET', 'POST'])
def getOrder():
    if request.method == 'GET':
        pharmacyFromUser = session.get('pharmacyId', False)
        if pharmacyFromUser == False: return jsonify('sem farmácia declarada'), 400

        str = '''
            SELECT * FROM `order`
            INNER JOIN orderItem
            ON `order`.orderId = orderItem.orderId
            INNER JOIN remedy
            ON remedy.remedyId = orderItem.remedyId;
        '''

        res = db.engine.execute(str)
        res = pedidos_schema.dump(res)
        return jsonify(res), 200
    elif request.method == 'POST':
        body = request.get_json()


        # p/ dps --> validar se user existe msm; validar totalValue

        try:
            body['totalValue'] = int(body['totalValue'])
        except:
            return jsonify({"msg": 'o campo preço não é um número', "error": True }), 400
        try:
            body['quantity'] = int(body['quantity'])
        except:
            return jsonify({"msg": 'o campo quantidade não é um número', "error": True }), 400 


        body['orderType'] = body['orderType'].upper()
        body['status'] = body['status'].upper()

        dataRegistro = datetime.datetime.now()

        order = Order(orderType=body['orderType'], status=body['status'], totalValue=body['totalValue'], pharmacyId=body['pharmacyId'], userId=body['userId'],date=dataRegistro)
        db.session.add(order)
        db.session.commit()
        orderItem = OrderItem(quantity=body['quantity'], orderId=order.orderId, remedyId=body['remedyId'])
        db.session.add(orderItem)
        db.session.commit()
        return jsonify('criado com sucesso'), 200
    else :
        return jsonify('Method not found'), 400

@routes.route('/api/order/<int:id>', methods=['GET', 'PUT','DELETE'])
def specific_Order(id):
    if request.method == 'GET':
        res = orders_schema.dump(Order.query.filter_by(userId=id).one())
        return jsonify(res)
    elif 'PUT':
        body = request.get_json()

        try:
            body['totalValue'] = float(body['price'])
        except:
            return jsonify({"msg": 'o campo preço não é um número', "error": True }), 400
        try:
            body['quantity'] = int(body['quantity'])
        except:
            return jsonify({"msg": 'o campo quantidade não é um número', "error": True }), 400 

        order = Order.query.filter_by(orderId=id).one()
        orderItem = OrderItem.query.filter_by(orderId=id).one()

        body['status'] = body['status'].upper()

        order.totalValue = body['totalValue']
        order.date = body['data-pedido']
        order.status = body['status']

        orderItem.quantity = body['quantity']

        db.session.add(order)
        db.session.add(order)
        db.session.commit()
        db.session.add(orderItem)
        db.session.commit()

        # retornar obj dps
        res = {
            "msg": 'update feito com sucesso'
        }

        return jsonify(res)
    elif request.method == 'DELETE':
        toDeleteItem = OrderItem.query.filter_by(orderId=id).one()
        db.session.delete(toDeleteItem)
        toDelete = Order.query.filter_by(orderId=id).one()
        db.session.delete(toDelete)
        db.session.commit()
        return jsonify('F no chat')
    else:
        return jsonify('Method not found')