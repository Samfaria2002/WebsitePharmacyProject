from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow 
from flask_login import LoginManager

#Instanciador -- obg little Samuel :)
#Little Samuel aqui: tmj Leo, vulgo "o mago da programação"
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
login_manager = LoginManager()
