from flask import Flask
from flask import redirect
from flask import render_template
from flask import session
from flask import request
from flask import escape
from flask import url_for
import mysql.connector

from flask import jsonify
import json
import urllib

app = Flask(__name__)

app.secret_key = 'Yekcim'

@app.route('/')
def index():
	username = request.form["username"]
	password = request.form["password"]
	
	db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="fruits")
	cvar = db.cursor()
	cvar.execute("select username from users where username = %s and password = %s",(username,password))
	data = cvar.fetchall()
	
	if(cvar.rowcount > 0):
		session["loggedin"] = 1
		return redirect("/addform")
	else:
		session["loggedin"] = 0
		return redirect("/loginform")

@app.route('/loginform')
def loginform():
	return render_template("loginform.html")
	#go get the html and include
	
	
@app.route('/loginaction', methods= ["POST", "GET"])
def loginaction():
	username = request.form["username"]
	password = request.form["password"]
	
	db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="fruits")
	cvar = db.cursor()
	cvar.execute("select username from users where username = %s and password = %s",(username,password))
	data = cvar.fetchall()
	
	if(cvar.rowcount > 0):
		session["loggedin"] = 1
		return redirect("/addform")
	else:
		session["loggedin"] = 0
		return redirect("/loginform")


@app.route('/apiform')
def apiform():
	return render_template('apiform.html')

@app.route('/apiresponse', methods=['POST','GET'])
def apiresponse():
	city = request.form['city']
	state = request.form['state']
	url = "http://maps.googleapis.com/maps/api/geocode/json?address="+city+','+state
	url2 = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "," + state
	url3 = "https://www.eventbrite.com/json/event_search?app_key=MWOII4MCOEL2TRLZVN&keywords="+ city + "," + state
	loadurl = urllib.urlopen(url)
	loadurl2 = urllib.urlopen(url2)
	loadurl3 = urllib.urlopen(url3)

	data1 = json.loads(loadurl.read().decode(loadurl.info().getparam('charset')or'utf-8'))
	data2 = json.loads(loadurl2.read().decode(loadurl2.info().getparam('charset')or'utf-8'))
	data3 = json.loads(loadurl3.read().decode(loadurl3.info().getparam('charset')or'utf-8'))
	data = (data1,data2,data3)

	# return jsonify(data1)
	return render_template('apiform.html',pagedata=data)

if __name__ == '__main__':
	app.run(debug=True)