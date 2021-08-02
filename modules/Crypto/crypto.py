from logging import error
import os
from pyasn1.type.univ import Null
import pyrebase
import time
from dotenv import load_dotenv
from flask import Blueprint, render_template, request, redirect
import requests
from requests.sessions import session

crypto = Blueprint(
    "crypto",
    __name__, 
    template_folder="templates"
)

load_dotenv()

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
    db = firebase.database()
    print(" * Database Connected with Coins")
except:
    print(" * Failed to connect with Database")

def transaction(email, mode, coin, units, usd, price):
    return {
        "email": email,
        "mode": mode,
        "coin": coin,
        "units": units,
        "usd": usd,
        "price": price,
        "timestamp": time.time()
    }

def getCoinValue(portfolio_id, coin):
    found=False
    # check if portfolio exists
    for pf in db.child("portfolios").get():
        if pf.key() == portfolio_id:
            found=True
            break
    if not found:
        return 0
    # if exists 
    portfolios = db.child("portfolios").child(portfolio_id).get()
    for pf in portfolios:
        if pf.key() == coin:
            return pf.val()
    return 0

@crypto.route("/")
def coins_list():
    return render_template("coins_list.html")

@crypto.route("/coin", methods=['GET', 'POST'])
def coin():
    message=None
    if request.method == 'POST':
        email = request.form['email']
        mode = request.form['mode']
        coin = request.args.get('id')
        units = float(request.form['units'])
        usd = float(request.form['usd'])
        price = float(request.form['price'])
        portfolio_id = request.form['portfolio_id']
        data = transaction(email, mode, coin, units, usd, price)

        # check if valid transaction
        valid=False
        value = getCoinValue(portfolio_id, coin)
        if mode=='BUY':
            value = round((value + units),8)
            valid=True

        if mode=='SELL' and (value-units)>=0: 
            value = round((value - units),8)
            valid=True

        elif mode=='SELL' and (value-units)<0:
            message = "Failed to make a transcation"
            
        if valid:
            try:
                db.child("transactions").push(data)
                db.child("portfolios").child(portfolio_id).update({coin: value})
                return redirect("/portfolio")
            except:
                message = "Failed to make a transcation"
                pass

    coin_id = request.args.get('id')
    URL = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin_id}&per_page=1&page=1&sparkline=false"
    r = requests.get(url = URL)
    return render_template("coin.html", coin=r.json(), coin_id=coin_id, message=message)
