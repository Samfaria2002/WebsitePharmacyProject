from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow 

#Instanciador -- obg little Samuel :)
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()