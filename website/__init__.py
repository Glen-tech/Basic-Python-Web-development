from flask import Flask
from flask_sqlalchemy import SQLAlchemy # for database useage
from os import path

db = SQLAlchemy()

def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY'] = 'Here can you give a secret key' # secret key for the webb appilaction
    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
    db.init_app(app)
    
    from .auth import auth
    
    app.register_blueprint(auth,  url_prefix='/') # / means no prefix
    
    from .models import User # file needs to be loaded before inilazing or creating database 

    create_database(app)
     
    return app
    
def create_database(app):
    if not path.exists('website/database.db'):
        db.create_all(app=app)
    else:
        print('Database exist')
   
  
    
    
