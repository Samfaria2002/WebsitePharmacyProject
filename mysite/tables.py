from extensions import db, ma

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

class PharmacySchema(ma.Schema):
  class Meta:
    fields = ('pharmacyId', 'name', 'logo', 'pais', 'uf', 'cidade', 'bairro', 'rua', 'numero_endereco', 'cep', 'latitude', 'longitude')

# Init schema
pharmacy_schema = PharmacySchema()
pharmacies_schema = PharmacySchema(many=True)