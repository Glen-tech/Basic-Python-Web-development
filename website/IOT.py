from flask import Blueprint, render_template,request,flash,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash 
from .models import User
#from .auth import email

from flask_login import login_user, login_required, logout_user, current_user

import sqlite3 

#routes for or website

IOT = Blueprint('IOT', __name__)


@IOT.route('/handleData',methods=['GET', 'POST'])
#handles post requests, doesn't need to render anything
def handleData():
    
    conn = sqlite3.connect('database.db')
    conn.execute("CREATE TABLE IF NOT EXISTS Values_IOT (id INTEGER PRIMARY KEY, CO2 INTEGER, tVTOC INTEGER, Humidity FLOAT,Temperature FLOAT, Light INTEGER, Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
    conn.close() 
    
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
       
       conn = sqlite3.connect('database.db')
       conn.execute("CREATE TABLE IF NOT EXISTS Values_IOT (id INTEGER PRIMARY KEY, CO2 INTEGER, tVTOC INTEGER, Humidity FLOAT,Temperature FLOAT, Light INTEGER, Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
       conn.execute("INSERT INTO Values_IOT (CO2,tVTOC,Humidity,Temperature,Light) VALUES (?,?,?,?,?)",( CO2_value, tVTOC_value,humidity_value,temperature_value, light_value) )
       conn.commit()
       conn.close() 
       
       
      # new_value = Values_IOT(CO2 = CO2_value, tVTOC = tVTOC_value , Humidity = humidity_value , Temperature = temperature_value , Light = light_value)
      # db.session.add(new_value)
      # db.session.commit()
       
       
   
    return ''


@IOT.route('/show',  methods = ['GET','POST'])
@login_required
def showData():

    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Values_IOT ORDER BY Time DESC")
   
    rows = cur.fetchall(); 
            
    return render_template("show.html",rows = rows , user=current_user)


@IOT.route('/plot',  methods = ['GET','POST'])
@login_required
def plotData():
    return render_template("plot.html",user=current_user)






