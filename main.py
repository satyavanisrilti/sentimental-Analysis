from flask import Flask,render_template,abort,redirect,url_for ,request ,jsonify ,json , current_app, session, flash
import tweepy
from textblob import TextBlob
from form import Login,Register
from pymongo import MongoClient
from flask_pymongo import PyMongo,pymongo
from flask_bcrypt import Bcrypt,generate_password_hash
import bcrypt
from requests.auth import HTTPBasicAuth
import requests
from functools import wraps
#---------------------------------------------------------------------------
app = Flask(__name__)
bcrypt = Bcrypt(app)
consumer_key = 'LEvMPkNl9oYPMpcVboCsk5t3i'
consumer_secret = 'zaFHcGhOX8ElmPcTFabP45AmroPh3k4u29yGluhyfw9H7pRfRc'
access_token = '1209524614084214784-kak02H07NH5YaLXSU2GZuXM9eSs3RY'
access_token_secret = 'Juv8cPmrZIISiHDdu9Z8U0MwM6SSEGbZeTXtzCBoXITEy'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
app.secret_key = 'haii'
#-------------------------------------------------------------------------
client = MongoClient('mongodb+srv://admin123:admin123@sample-tfh3q.mongodb.net/test?retryWrites=true&w=majority')

db = client['news']

Admin = client['RCE_Admin']

def authorize(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if not 'username' in session:
            flash('Please Login ! to continue ','warning')
            return redirect(url_for('login'))


        return f(*args, **kwargs)
    return decorated_func

@app.route("/")
def home():
    return render_template('landing.html')

@app.route('/HomePage')
# @authorize
def index():
    flash('Logged In Succesfully ! ','success')
    return render_template('home.html')

@app.route("/search",methods=["POST"])
@authorize
def search():
    search_tweet = request.form.get("search_query")
    
    t = []
    tweets = api.search(search_tweet, tweet_mode='extended')
    for tweet in tweets:
        polarity = TextBlob(tweet.full_text).sentiment.polarity
        subjectivity = TextBlob(tweet.full_text).sentiment.subjectivity
        t.append([tweet.full_text,polarity,subjectivity])
        # t.append(tweet.full_text)

    return jsonify({"success":True,"tweets":t})

@app.route('/AdminLogin',methods=['POST','GET'])
def admin():
    form = Login()
    if 'username' in session:
        flash('LOGIN SUCCESFULL ! ','success')
        return redirect('HomePage')
    else:
        flash("PLEASE LOGIN","warning")
        return redirect('login')

    return render_template('index.html',form = form)


@app.route('/login', methods=['POST','GET'])
def login():
    form = Login()
    if form.validate_on_submit():
        username = request.form['username']
        login_user = Admin.Users.find_one({'username' : username} )
        if login_user:
        # hashedpwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            if bcrypt.check_password_hash(login_user['password'],form.password.data):
            #if bcrypt.(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                flash('Logined Succesful ',"success")
                return redirect(url_for('index'))

    return render_template('login.html',form = form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = Register()
    if request.method == 'POST':
        password = request.form['password']
        existing_user = Admin.Users.find_one({'name' : request.form['username']})
        conf_password = request.form['conf_password']
        if existing_user is None and ( password == conf_password):
            
            hashpass = bcrypt.generate_password_hash(request.form['password'].encode('utf-8'))
            Admin.Users.insert({'username' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            flash('User Registerd successfully','success')
            return redirect(url_for('login'))
        
        return 'That username already exists!'

    return render_template('register.html',form = form)
@app.route("/logout",methods=['GET','POST'])
def logout():
    # form = Login()
    flash("Enter Admin Credentials for Logging out ! ",'danger')
    if 'username' in session:
        [session.pop(key) for key in list(session.keys())]
        flash('ADMIN , LOGGED OUT !','danger')
        return redirect(url_for('home'))
if __name__=='__main__':
    app.run(debug="True")