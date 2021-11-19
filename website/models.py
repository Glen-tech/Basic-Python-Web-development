from . import db # database models code
from flask_login import UserMixin # custom class for objects login reletated
from sqlalchemy.sql import func # date time 

    
class User(db.Model,UserMixin): #user database
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True) # only 1 email not 5 tesame orso
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))    
    
    
class Note(db.Model): # note database
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # link to user class
    notes = db.relationship('Note') # notes related to the user
    
    


