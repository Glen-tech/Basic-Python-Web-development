from . import db # database models code
from flask_login import UserMixin # custom class for objects login reletated
from datetime import datetime
    
class User(db.Model,UserMixin): #user database
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True) # only 1 email not 5 tesame orso
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))    
    
    
class Values_IOT(db.Model): # IOT database
    id = db.Column(db.Integer, primary_key = True)
    CO2 = db.Column(db.Integer)
    tVTOC= db.Column(db.Integer)
    Humidity = db.Column(db.Float)
    Temperature = db.Column(db.Float)
    Light = db.Column(db.Integer)
    Time = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    

