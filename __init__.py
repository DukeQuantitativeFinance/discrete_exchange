import os

from flask import Flask
from pymongo import MongoClient
from flask_login import LoginManager

from .routes import main_routes, discrete_exchange_routes

# see: https://flask-login.readthedocs.io/en/latest/
# see: https://pythonbasics.org/flask-login/

# create login manager
login_manager = LoginManager()
login_manager.login_view = 'login'

# function to create app instance
def create_app():
    
    app = Flask(__name__)
    
    # configure upload destination for submitted files
    app.config['UPLOAD_DEST'] = os.path.dirname(__file__) + '/submitted_traders'
    
    # initialize login manager
    login_manager.init_app(app)
    
    # blueprints
    app.register_blueprint(main_routes)
    app.register_blueprint(discrete_exchange_routes)
    
    return app
