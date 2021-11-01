from flask import Blueprint, render_template
from flask_login import current_user
#routes for or website
views = Blueprint('views', __name__)

@views.route('/')

def home():
    return render_template("home.html", user = current_user) #user is manditory


