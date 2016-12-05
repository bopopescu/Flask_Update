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
import os



app = Flask(__name__)

@app.route('/apiresponse')
def apiresponse():
	url = "http://localhost:8888/MVC/index.php?action=form&execute=makeJSON"
	loadurl = urllib.urlopen(url)
	
	data = json.loads(loadurl.read().decode(loadurl.info().getparam('charset')or'utf-8'))
	# return jsonify(data1)
	return render_template('apiform2.html',pagedata=data)



if __name__ == '__main__':
	app.run(debug=True)