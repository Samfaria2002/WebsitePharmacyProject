from extensions import db, ma
from marshmallow import fields
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
  #numero_endereco = db.Column(db.String(6))
  cep = db.Column(db.String(9)) # 8 digitos + 1 '-'
  latitude = db.Column(db.Numeric(13,10)) # vai ser 18,15 dps >:D
  longitude = db.Column(db.Numeric(13,10))
  telefone = db.Column(db.String(14)) # (10)98765-4321
  users = db.relationship('user', backref='person', lazy=True)
  remedys = db.relationship('remedy', backref='person', lazy=True)


class PharmacySchema(ma.Schema):
  
  latitude = fields.Decimal(as_string=True)
  longitude = fields.Decimal(as_string=True)
  class Meta:
    fields = ('pharmacyId', 'name', 'logo', 'pais', 'uf', 'cidade', 'bairro', 'rua', 'numero_endereco', 'cep', 'latitude', 'longitude', 'telefone')

# Init schema
#pharmacy_schema = PharmacySchema()


class User(db.Model):
  __tablename__ = "user"

  userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  userName = db.Column(db.String(99))
  password = db.Column(db.string(99))
  userType = db.Column(db.String(1))
  name = db.Column(db.String(100))
  birthDate = db.Column(db.Date)
  sex = db.Column(db.String(1))
  email = db.Column(db.String(99))
  pharmacyId = db.Column(db.Integer, db.ForeignKey('pharmacy.pharmacyId'),nullable=True)
  orders = db.relationship('order', backref='person', lazy=True)
  recipes = db.relationship('recipe', backref='person', lazy=True)

class UserSchema(ma.Schema):
  
  class Meta:
    fields = ('userId','userName','password','userType','name','birthDate','sex','email','pharmacyId')

class Inventary(db.Model):
  __tablename__ = "inventary"

  inventaryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  unitType = db.Column(db.String(1))
  quantity = db.Column(db.Numeric(20,10))
  remedyId = db.Column(db.Integer, db.ForeignKey('remedy.remedyId'),nullable=False)

class InventarySchema(ma.Schema):
  
  class Meta:
    fields = ('inventaryId' ,'unitType' ,'quantity' ,'remedyId')

class Remedy(db.Model):
  __tablename__ = "remedy"

  remedyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100))
  laboratory = db.Column(db.String(100))
  price = db.Column(db.Numeric(10,2))
  barCode = db.Column(db.String(100))
  pharmacyId = db.Column(db.Integer, db.ForeignKey('pharmacy.pharmacyId'),nullable=False)
  inventaryId = db.Column(db.Integer, db.ForeignKey('inventary.inventaryId'),nullable=False)
  inventary = db.relationship('inventary', backref='person', uselist=False, lazy=True)

class RemedySchema(ma.Schema):
  
  class Meta:
    fields = ('remedyId','name','laboratory','price','barCode','pharmacyId','inventaryId')

class Recipe(db.Model):
  __tablename__ = "recipe"

  recipeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  date = db.Column(db.Date)
  recipeType = db.Column(db.String(1))
  validity = db.Column(db.Date)
  userId = db.Column(db.Integer, db.ForeignKey('user.userId'),nullable=False)
  recipeItens = db.relationship('recipeItem', backref='person', lazy=True)
  orders = db.relationship('order', backref='person', lazy=True)

class RecipeSchema(ma.Schema):
  
  class Meta:
    fields = ('recipeId' ,'date' ,'recipeType' ,'validity','userId')

class RecipeItem(db.Model):
  __tablename__ = "recipeItem"

  recipeItemId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100))
  quantity = db.Column(db.Numeric(20,10))
  recipeId = db.Column(db.Integer, db.ForeignKey('recipe.recipeId'),nullable=False)
  OrderItens = db.relationship('OrderItem', backref='person', lazy=True)

class RecipeItemSchema(ma.Schema):
  
  class Meta:
    fields = ('recipeItemId' ,'name' ,'quantity' ,'recipeId')

class Order(db.Model):
  __tablename__ = "order"

  orderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  date = db.Column(db.Date)
  orderType = db.Column(db.String(1))
  totalValue = db.Column(db.Numeric(20,10))
  pharmacyId = db.Column(db.Integer, db.ForeignKey('pharmacy.pharmacyId'),nullable=False)
  recipeId = db.Column(db.Integer, db.ForeignKey('recipe.recipeId'),nullable=True)
  userId = db.Column(db.Integer, db.ForeignKey('user.userId'),nullable=False)
  orderItens = db.relationship('orderItem', backref='person', lazy=True)

class OrderSchema(ma.Schema):
  class Meta:
    fields = ('orderId' ,'date' ,'orderType' ,'totalValue' ,'pharmacyId' ,'recipeId' ,'userId')

class OrderItem(db.Model):
  __tablename__ = "orderItem"

  orderItemId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  quantity = db.Column(db.Numeric(20,10))
  orderId = db.Column(db.Integer, db.ForeignKey('order.orderId'),nullable=False)
  recipeItemId = db.Column(db.Integer, db.ForeignKey('recipeItem.recipeItemId'),nullable=False)
  remedyId = db.Column(db.Integer, db.ForeignKey('remedy.remedyId'),nullable=False)


class OrderItemSchema(ma.Schema):
  
  class Meta:
    fields = ('orderItemId' ,'quantity' ,'orderId' ,'recipeItemId', 'remedyId')




pharmacies_schema = PharmacySchema(many=True)
users_schema = UserSchema(many=True)
inventarys_schema = InventarySchema(many=True)
remedys_schema = RemedySchema(many=True)
recipe_schema = RecipeSchema(many=True)
recipeItem_schema = RecipeItemSchema(many=True)
order_schema = OrderSchema(many=True)
orderItem_schema = OrderItemSchema(many=True)