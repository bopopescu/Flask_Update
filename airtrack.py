from flask import Flask, session, request, render_template, redirect, jsonify
import os,mysql.connector, json, urllib

app = Flask(__name__)

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/createJson")
def createJson():
    url = "https://api.flightstats.com/flex/airlines/rest/v1/json/active?appId=9147c5c6&appKey=8c3299af6667cf363fa580203efd4a8d"
    loadurl = urllib.urlopen(url)
    data = json.loads(loadurl.read().decode(loadurl.info().getparam('charset') or 'utf-8'))
    cleanData = data
    return render_template("result.html", cleanData=cleanData)

@app.route("/flightStatus", methods=["GET", "POST"])
def login():
	
	airline = request.form["airline"]
	number = request.form["number"]

	year = request.form["year"]
	month = request.form["month"]
	day = request.form["day"]

	url = "https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/"+airline+"/"+number+"/dep/"+year+"/"+month+"/"+day+"?appId=9147c5c6&appKey=8c3299af6667cf363fa580203efd4a8d&utc=false"
	loadurl = urllib.urlopen(url)
	data = json.loads(loadurl.read().decode(loadurl.info().getparam("charset") or 'utf-8'))
	cleanData = data
	return render_template("result.html", cleanData=cleanData)

@app.route('/team')
def team():
	return render_template('team.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

if __name__ == '__main__':
    app.debug = True
    app.run()