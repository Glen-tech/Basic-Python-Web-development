from flask import Blueprint, render_template
from flask_login import current_user
#routes for or website

auth = Blueprint('auth', __name__)



@auth.route('/login')
def login():
    return render_template("login.html" ,  user = current_user) #user is manditory, will crash if not
    
  
@auth.route('/logout')  
def logout():
    return render_template("logout.html",  user = current_user) 
    
    
@auth.route('/sign-up')
def sign_up():
     return render_template("sign_up.html",user = current_user) 
