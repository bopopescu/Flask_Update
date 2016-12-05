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
	#session has key
	if not session.has_key("loggedin"):
		session["loggedin"] = 0
		return render_template("loginform.html")

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

if __name__ == '__main__':
	app.run(debug=True)
