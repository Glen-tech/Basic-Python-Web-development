from flask import Blueprint, render_template,request
from flask_login import current_user
#routes for or website

auth = Blueprint('auth', __name__)

#user is manditory, will crash if not

@auth.route('/')
def home():
    return render_template("home.html", user = current_user) 
    

@auth.route('/logout')  
def logout():
    return render_template("logout.html",  user = current_user) 
    
    
@auth.route('/login',methods=['POST,GET']) # will now handle post and get requests
def login():
    #data = request.form
    #print(data)
    return render_template("login.html" ,  user = current_user)
    
        
@auth.route('/sign-up',methods=['POST,GET'])
def sign_up():
    return render_template("sign_up.html",user = current_user) 
