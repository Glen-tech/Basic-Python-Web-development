from flask import Blueprint, render_template,request,flash,redirect,url_for
from .models import Values_IOT
from werkzeug.security import generate_password_hash,check_password_hash 
from . import db
from flask_login import login_user, login_required, logout_user, current_user

import json
import sqlite3
import jmespath

#routes for or website

IOT = Blueprint('IOT', __name__)


@IOT.route('/handleData',methods=['GET', 'POST'])
#handles post requests, doesn't need to render anything
def handleData():
    
    if request.method == 'POST':
    
       request_data =request.get_json()
       
       CO2 = request_data['CSS811_sensor'][0]
       CO2_value = request_data['CSS811_sensor'][1]
       tVTOC = request_data['CSS811_sensor'][2]
       tVTOC_value = request_data['CSS811_sensor'][3]
      
       humidity = request_data['DHT11_sensor'][0]
       humidity_value = request_data['DHT11_sensor'][1]
       
       temperature = request_data['DHT11_sensor'][2]
       temperature_value = request_data['DHT11_sensor'][3]
       
       light =  request_data['Groove_light_sensor'][0]
       light_value =  request_data['Groove_light_sensor'][1]
        
       print(CO2 + ":" + CO2_value)
       print(tVTOC + ":" + tVTOC_value)
       print(humidity + ":" + humidity_value)
       print(temperature + ":" + temperature_value)
       print(light + ":" + light_value)
        
       print(request_data)
       
       new_value = Values_IOT(CO2 = CO2_value, tVTOC = tVTOC_value , Humidity = humidity_value , Temperature = temperature_value , Light = light_value)
       db.session.add(new_value)
       db.session.commit()
       
   
    return ''



@IOT.route('/show',  methods = ['GET','POST'])
@login_required
def showData():
    return render_template("show.html", user = current_user)


