from flask import Flask
from flask_assets import Environment, Bundle
import os
from dotenv import load_dotenv
from views import views
from extensions import db, migrate, ma

app = Flask(__name__)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username = os.environ.get('DB_USERNAME'),
    password = os.environ.get('DB_PASSWORD'),
    hostname = os.environ.get('DB_HOSTNAME'),
    databasename = os.environ.get('DB_DBNAME'),
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app)
ma.init_app(app)
assets = Environment(app)
#assets.url = app.static_url_path
# static/stylesheet/
base = Bundle('stylesheet/base-file.scss', filters='pyscss,cssmin', output='stylesheet/base-file.css')
main = Bundle('stylesheet/main.scss', filters='pyscss,cssmin', output='stylesheet/main.css')
assets.register('base_scss', base)
assets.register('main_scss', main)

app.register_blueprint(views)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run()
    #app.run(host = "0.0.0.0", port = 5000, debug = True)