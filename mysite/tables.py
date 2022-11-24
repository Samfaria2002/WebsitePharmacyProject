from extensions import db, ma
from marshmallow import fields
from flask_login import UserMixin


class User(UserMixin, db.Model):
  __tablename__ = "user"

  userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  userName = db.Column(db.String(99))
  password = db.Column(db.String(99))
  userType = db.Column(db.String(1)) # f ou c ou a
  name = db.Column(db.String(100))
  birthDate = db.Column(db.Date)
  sex = db.Column(db.String(1))
  email = db.Column(db.String(99))
  pharmacyId = db.Column(db.Integer, db.ForeignKey('pharmacy.pharmacyId'),nullable=True)
  #orders = db.relationship('order', backref='person', lazy=True)
  #recipes = db.relationship('recipe', backref='person', lazy=True)

  def get_id(self):
    return (self.userId)

class UserSchema(ma.SQLAlchemyAutoSchema):
  
  class Meta:
    model = User

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
  complemento = db.Column(db.String(200))
  cep = db.Column(db.String(9)) # 8 digitos + 1 '-'
  latitude = db.Column(db.Numeric(13,10)) # vai ser 18,15 dps >:D
  longitude = db.Column(db.Numeric(13,10))
  telefone = db.Column(db.String(14)) # (10)98765-4321
  #users = db.relationship('user', backref='person', lazy=True)
  #remedys = db.relationship('remedy', backref='person', lazy=True)

class PharmacySchema(ma.SQLAlchemyAutoSchema):
  
  latitude = fields.Decimal(as_string=True)
  longitude = fields.Decimal(as_string=True)
  class Meta:
    model = Pharmacy

# Init schema
#pharmacy_schema = PharmacySchema()
'''
class Inventary(db.Model):
  __tablename__ = "inventary"

  inventaryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  unitType = db.Column(db.String(1))
  quantity = db.Column(db.Numeric(20,10))
  remedyId = db.Column(db.Integer, db.ForeignKey('remedy.remedyId'),nullable=False)

class InventarySchema(ma.SQLAlchemyAutoSchema):
  quantity = fields.Decimal(as_string=True)
  class Meta:
    model = Inventary
'''

class Remedy(db.Model):
  __tablename__ = "remedy"

  remedyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100))
  laboratory = db.Column(db.String(100))
  price = db.Column(db.Numeric(10,2))
  barCode = db.Column(db.String(100))
  pharmacyId = db.Column(db.Integer, db.ForeignKey('pharmacy.pharmacyId'),nullable=False)
  #inventaryId = db.Column(db.Integer, db.ForeignKey('inventary.inventaryId'),nullable=False)
  unitType = db.Column(db.String(1)) # q ou p
  quantity = db.Column(db.Numeric(20,10))
  #inventary = db.relationship('inventary', backref='person', uselist=False, lazy=True)

class RemedySchema(ma.SQLAlchemyAutoSchema):
  price = fields.Decimal(as_string=True)
  quantity = fields.Decimal(as_string=True)
  class Meta:
    model = Remedy

class Recipe(db.Model):
  __tablename__ = "recipe"

  recipeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  date = db.Column(db.Date)
  recipeType = db.Column(db.String(1))
  validity = db.Column(db.Date)
  userId = db.Column(db.Integer, db.ForeignKey('user.userId'),nullable=False)
  #recipeItens = db.relationship('recipeItem', backref='person', lazy=True)
  #orders = db.relationship('order', backref='person', lazy=True)

class RecipeSchema(ma.SQLAlchemyAutoSchema):
  
  class Meta:
    model = Recipe
class RecipeItem(db.Model):
  __tablename__ = "recipeItem"

  recipeItemId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100))
  quantity = db.Column(db.Numeric(20,10))
  recipeId = db.Column(db.Integer, db.ForeignKey('recipe.recipeId'),nullable=False)
  #OrderItens = db.relationship('OrderItem', backref='person', lazy=True)

class RecipeItemSchema(ma.SQLAlchemyAutoSchema):
  quantity = fields.Decimal(as_string=True)
  class Meta:
    model = RecipeItem

class Order(db.Model):
  __tablename__ = "order"

  orderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  date = db.Column(db.Date)
  orderType = db.Column(db.String(1)) # V de venda, E de estoque
  status = db.Column(db.String(1)) # C de created D de cabo
  totalValue = db.Column(db.Numeric(20,10))
  pharmacyId = db.Column(db.Integer, db.ForeignKey('pharmacy.pharmacyId'),nullable=False)
  recipeId = db.Column(db.Integer, db.ForeignKey('recipe.recipeId'),nullable=True)
  userId = db.Column(db.Integer, db.ForeignKey('user.userId'),nullable=False)
  #orderItens = db.relationship('orderItem', backref='person', lazy=True)

class OrderSchema(ma.SQLAlchemyAutoSchema):
  totalValue = fields.Decimal(as_string=True)
  class Meta:
    model = Order

class OrderItem(db.Model):
  __tablename__ = "orderItem"

  orderItemId = db.Column(db.Integer, primary_key=True, autoincrement=True)
  quantity = db.Column(db.Numeric(20,10))
  orderId = db.Column(db.Integer, db.ForeignKey('order.orderId'),nullable=False)
  recipeItemId = db.Column(db.Integer, db.ForeignKey('recipeItem.recipeItemId'),nullable=True)
  remedyId = db.Column(db.Integer, db.ForeignKey('remedy.remedyId'),nullable=False)


class OrderItemSchema(ma.SQLAlchemyAutoSchema):
  quantity = fields.Decimal(as_string=True)
  class Meta:
    model = OrderItem


class PedidoSchema(ma.SQLAlchemySchema): 
  quantity = fields.Decimal(as_string=True)
  totalValue = fields.Decimal(as_string=True)
  price = fields.Decimal(as_string=True)
  date = fields.Date()
  class Meta:
    fields = ('orderId','date','orderType','status','totalValue','pharmacyId','userId', 'quantity', 'remedyId', 'name', 'unitType', 'price', 'laboratory')



# pro futuro: tentar fazer as relationship funcionarem

pharmacies_schema = PharmacySchema(many=True)
users_schema = UserSchema(many=True)
#inventaries_schema = InventarySchema(many=True)
remedies_schema = RemedySchema(many=True)
recipe_schema = RecipeSchema(many=True)
recipeItem_schema = RecipeItemSchema(many=True)
orders_schema = OrderSchema(many=True)
orderItem_schema = OrderItemSchema(many=True)

pedidos_schema = PedidoSchema(many=True)