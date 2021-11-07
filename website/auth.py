from flask import Blueprint, render_template,request,flash
#routes for or website

auth = Blueprint('auth', __name__)

#user is manditory, will crash if not

@auth.route('/')
def home():
    return render_template("home.html") 
    

@auth.route('/logout')  
def logout():
    return render_template("logout.html") 
    
@auth.route('/login',methods=['GET', 'POST']) # will now handle post and get requests
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email)
        print(password)
    return render_template("login.html")
    
        
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(email)
        print(firstName)
        print(password1)
        print(password2)
        
        if(len(email) < 3):
            flash("Email must be greater than 2 characters", category = 'error')
        elif(len(firstName) < 3):
            flash("First name must be greater than 2 characters", category = 'error')
        elif(len(password1) < 5):
            flash("password must be greater than 4 characters", category = 'error')
        elif(password1 != password2):
            flash("Passwords don\'t match, try again", category = 'error')
        else:
            flash("Account succesfully created", category = 'succes')
            
    return render_template("sign_up.html")
