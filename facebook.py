from flask import Flask, render_template, send_from_directory
from flask import url_for, request, session, redirect
from datetime import datetime
from flask_oauth import OAuth
import os, mysql.connector, json, urllib, string


#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)

app.secret_key = 'Yekcim'

app.config.update(
    DEBUG = True,
)

#----------------------------------------
# controllers
#----------------------------------------

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    try:
        if (session['logged_in'] == True):
            data = facebook.get('/me').data
            if 'id' in data and 'name' in data:
                session['user_id'] = data['id']
                session['user_name'] = data['name']
                # data2 = facebook.get('/'+ session['user_id'] +'/picture?redirect=false').data
                # session['picture'] = data2['url']
                # <img href={{picture}}>
        else:
            session['logged_in'] = False
            session['user_id'] = ''
            session['user_name'] = ''
            session['url'] = ''

    except:
        pass


    return render_template('form.html', username=session['user_name'], userid=session['user_id'])


@app.route("/flightStatus", methods=["GET", "POST"])
def search():

    airline = request.form["airline"]
    airlineSplit = airline.split("||")
    aita = airlineSplit[1]

    number = request.form["number"]

    year = request.form["year"]
    month = request.form["month"]
    day = request.form["day"]

    currentTime = datetime.now()
    date = str(currentTime)
    splitString = date.split()
    todaysDate = splitString[0]

    url = "https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/"+aita+"/"+number+"/dep/"+year+"/"+month+"/"+day+"?appId=9147c5c6&appKey=8c3299af6667cf363fa580203efd4a8d&utc=false"
    loadurl = urllib.urlopen(url)
    data = json.loads(loadurl.read().decode(loadurl.info().getparam('charset') or 'utf-8'))
    cleanData = data
    # departure info
    departureDate= cleanData["flightStatuses"][0]["departureDate"]["dateLocal"]
    departureTime = departureDate.split("T")
    departure=departureTime[0]
    cleanDeparture= departureTime[1][:-7]

    # arrival info
    arrivalDate= cleanData["flightStatuses"][0]["arrivalDate"]["dateLocal"]
    arrivalTime = arrivalDate.split("T")
    cleanArrival= arrivalTime[1][:-7]

    return render_template("result.html", cleanData=cleanData, cleanDeparture=cleanDeparture, cleanArrival=cleanArrival, todaysDate=todaysDate, departure=departure, username=session['user_name'])

@app.route("/save/<flightId>/<flightNumber>/<flightDate>/<flightTime>", methods=["GET", "POST"])
def save(flightId,flightNumber,flightDate,flightTime ):
    db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="ALS_Database")
    cvar = db.cursor()
    cvar.execute("INSERT INTO userFlights (userId, flightId, flightNumber, flightDate, flightTime) values (%s, %s, %s, %s, %s )" , (session['user_id'], flightId, flightNumber, flightDate, flightTime))
    db.commit()
    return render_template("/profile")



@app.route("/userProfile")
def userProfile():
    db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="ALS_Database")
    cvar = db.cursor()
    cvar.execute("SELECT flightId, userId from userFlights WHERE userId = %s", (session['user_id'], ))
    # data = cvar.fetchall()
    for (flightId, userId) in cvar:
        return str(flightId)




@app.route("/profile")
def profile():

    db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="ALS_Database")
    cvar = db.cursor()
    cvar.execute("SELECT flightId, flightNumber, flightDate, flightTime from userFlights WHERE userId = %s", (session['user_id'], ))
    data = cvar.fetchall()

    return render_template("profile.html" , data=data, username=session['user_name'])


@app.route("/savedFlight/<flightId>", methods=["GET", "POST"])
def savedFlight(flightId):

    currentTime = datetime.now()
    date = str(currentTime)
    splitString = date.split()
    todaysDate = splitString[0]

    url = "https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/"+flightId+"?appId=9147c5c6&appKey=8c3299af6667cf363fa580203efd4a8d"
    loadurl = urllib.urlopen(url)
    data = json.loads(loadurl.read().decode(loadurl.info().getparam('charset') or 'utf-8'))
    cleanData = data
    # departure info
    departureDate= cleanData["flightStatus"]["departureDate"]["dateLocal"]
    departureTime = departureDate.split("T")
    departure=departureTime[0]
    cleanDeparture= departureTime[1][:-7]

    # arrival info
    arrivalDate= cleanData["flightStatus"]["arrivalDate"]["dateLocal"]
    arrivalTime = arrivalDate.split("T")
    cleanArrival= arrivalTime[1][:-7]

    return render_template("flightIdResult.html", cleanData=cleanData, cleanDeparture=cleanDeparture, cleanArrival=cleanArrival, todaysDate=todaysDate, departure=departure, username=session['user_name'])





#----------------------------------------
# facebook authentication
#----------------------------------------

FACEBOOK_APP_ID = '290969614437361'
FACEBOOK_APP_SECRET = 'd6c48ee445f4a7766f14ad0363527b2a'

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)



@app.route("/test")
def test():
    url = "http://graph.facebook.com/v2.1/"+ session['user_id'] +"/picture?redirect=0&height=200&type=normal&width=200"
    loadurl = urllib.urlopen(url)
    picture = json.loads(loadurl.read().decode(loadurl.info().getparam('charset') or 'utf-8'))
    session['picture'] = picture["data"]['url']
    return "<img href='"+session['picture']+"'>"


@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized', next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
