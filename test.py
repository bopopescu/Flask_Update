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
	
	#display fruits
	db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="fruits")
	cvar = db.cursor()
	cvar.execute("select name, color, id  from fruit_table")
	data = cvar.fetchall()
	return render_template("body.html", pagedata = data)

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
	

@app.route("/createJSON")
def createJSON():
	db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="fruits")
	cvar = db.cursor()
	cvar.execute("select name, color, id  from fruit_table")
	data = cvar.fetchall()

	return jsonify(fruits = data)

@app.route("/parseJSON")
def parseJSON():
	# session['']
	# url = "http://maps.googleapis.com/maps/api/geocode/json?address=winter%20park,fl"
	url = "http://api.sportsdatallc.org/nfl-t1/2014/PRE/2/schedule.json?api_key=vmb2h6tnr6bcg28hrmkq9b27"
	loadurl = urllib.urlopen(url)
	data = json.loads(loadurl.read().decode(loadurl.info().getparam('charset')or 'utf-8'))

	# return jsonify(data)
	return data['games'][0]['away'][0]['home'][0]

@app.route('/googleAPI')
def googleAPIform():
	return render_template("googleform.html")

@app.route('/googleView')
def googleView():
	url = "http://api.sportsdatallc.org/nfl-t1/teams/hierarchy.json?api_key=vmb2h6tnr6bcg28hrmkq9b27"
	loadurl = urllib.urlopen(url)
	data = json.loads(loadurl.read().decode(loadurl.info().getparam('charset')or 'utf-8'))

	return jsonify(data)

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

	return render_template('apiform.html',pagedata=data)


@app.route('/teamJSON')
def teamJSON():
	url = "http://api.sportsdatallc.org/nfl-t1/teams/hierarchy.json?api_key=vmb2h6tnr6bcg28hrmkq9b27"
	loadurl = urllib.urlopen(url)
	data = json.loads(loadurl.read().decode(loadurl.info().getparam('charset')or 'utf-8'))

	return jsonify(data)

@app.route('/logout')
def logout():
	session["loggedin"] = 0
	return redirect("/")
	

@app.route('/addform')
def showform():
	if(session["loggedin"] == 0):
		return redirect("/loginform")
	else:
		return render_template("addform.html")
		#go get the html and include
		#add fruit from

@app.route('/addaction', methods= ["POST", "GET"])
def addaction():
	name = request.form["name"]
	color = request.form["color"]
	
	db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="fruits")
	cvar = db.cursor()
	cvar.execute("insert into fruit_table (name,color) values (%s,%s)",(name,color))
	db.commit()
	return redirect("/")
	#add action
	#after add go back to the index

# @app.route('/update/<id>')	
# def updateform(id):
# 	session["quary"]=id	
# 	return render_template('updateform.html')

# @app.route('/updateaction', methods = ['GET', 'POST'])
# def updateaction():
# 	db = mysql.connector.connect(user='root',password='root',host='127.0.0.1', port='8889',database='fruits')
# 	cvar = db.cursor()
 	
#  	name = request.form["updatename"]
# 	color = request.form["updatecolor"]

# 	#return str(query)
# 	cvar.execute("update fruit_table set name=%s, color=%s where id=%s",(name,color,session["quary"]))
# 	db.commit()
# 	return redirect('/')
	
@app.route('/delete/<id>', methods = ['GET', 'POST'])
def delete(id):
	quary = id 
	db = mysql.connector.connect(user='root',password='root',host='localhost', port='8889',database='fruits')
 	cur = db.cursor()
 	cur.execute("delete from fruit_table where id=%s",(quary, ))
	db.commit()
	return redirect('/')

# @app.route('/callmamp')
# def callmamp():
# 	os.system('open /Applications/MAMP/MAMP.app')
# 	return "done"

# @app.route('/create')
# def create():
# 	os.system('touch /Applications/MAMP/htdocs/blue/text.txt')
# 	return "done"

# @app.route('/kill')
# def kill():
# 	os.system('killall -9 MAMP')
	# return "done"

if __name__ == '__main__':
	app.run(debug=True)