from flask import Flask
from flask_sqlalchemy import SQLAlchemy # for database useage
from os import path

db= SQLAlchemy()
DB_NAME= "database.db"

def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY'] = 'Here can you give a secret key' # secret key for the webb appilaction
    app.config['SQLALCHEMY_DATABASE_URI'] =f'SQLite:///{DB_NAME}' # f for python code as a string 
    db.init_app(app)
    
    
    from .auth import auth
    
    app.register_blueprint(auth,  url_prefix='/') # / means no prefix
    
    from .models import User,Note # file needs to be loaded before inilazing or creating database 
    
    create_database(app)
    
    return app
    
def create_database(app):
    if not path('127.0.0.1:5000/' + DB_NAME):
        db.create_all(app=app)
        print('Created database')
    
  
    
    
