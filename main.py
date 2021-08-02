import os
import requests
import pyrebase
from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
from modules.Crypto.crypto import crypto
from modules.Portfolio.portfolio import portfolio
from datetime import timedelta

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.permanent_session_lifetime = timedelta(days=1)

config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "databaseURL" : os.getenv("FIREBASE_DATABASE_URL"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID")
}
try:
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    print(" * Authentication Enabled")
except:
    print(" * Failed to enable Authentication")

# Blueprints
app.register_blueprint(crypto, url_prefix="/crypto")
app.register_blueprint(portfolio, url_prefix="/portfolio")

@app.route("/")
def home():
    # Events
    URL = "https://api.coingecko.com/api/v3/events"
    events = requests.get(url = URL).json()

    API_KEY = os.getenv("NEWS_API_KEY")
    URL2 = f"https://newsapi.org/v2/everything?q=bitcoin&apiKey={API_KEY}&pageSize=9"
    news = requests.get(url = URL2).json()
    
    return render_template("home.html", events=events, news=news)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            new_user = auth.create_user_with_email_and_password(email, password)
            session["email"] = email
            session["portfolio_id"] = email.rsplit("@")[0].replace(".","")
            session.permanent = True
            return redirect("/portfolio")
        except: 
            return render_template('signup.html', status="404")
    else:
        if "email" in session:
            return redirect("/portfolio")
        return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user_info = auth.sign_in_with_email_and_password(email, password)
            session["email"] = email
            session["portfolio_id"] = email.rsplit("@")[0].replace(".","")
            session.permanent = True
            return redirect("/portfolio")
        except:
            return render_template("signin.html", status="404")
    else:
        if "email" in session:
            return redirect("/portfolio")
        return render_template("signin.html")

@app.route('/logout')
def logout():
    session.pop("email", None)
    session.pop("portfolio_id", None)
    return redirect("/signin")

if __name__ == "__main__":
    app.run(debug=True)
