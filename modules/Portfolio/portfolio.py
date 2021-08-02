import pyrebase
import os
import requests
import time
from dotenv import load_dotenv
from flask import Blueprint, render_template, session

portfolio = Blueprint(
    "portfolio",
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
    print(" * Database Connected with Portfolio")
except:
    print(" * Failed to connect with Database")

@portfolio.route("/")
def my_portfolio():
    if "email" in session:
        email = session['email']
        portfolio_id = session['portfolio_id']
        portfolio, portfolio_value = getPortfolio(portfolio_id)
        transactions, total_invested = getTransactions(email)
        return render_template("portfolio.html", portfolio=portfolio, transactions=transactions, portfolio_value=portfolio_value, total_invested=total_invested)
    else:
        return render_template("signin.html", status="401")

def getCoinDetails(coin):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}&order=market_cap_desc&per_page=100&page=1&sparkline=false"
    coin_details = requests.get(url=url).json()
    return coin_details[0]

def getPortfolio(portfolio_id):
    found=False
    # check if portfolio exists
    for pf in db.child("portfolios").get():
        if pf.key() == portfolio_id:
            found=True
            break
    if not found:
        return None, 0
    # if exists
    coins = []
    portfolio_value = 0
    portfolios = db.child("portfolios").child(portfolio_id).get()
    for pf in portfolios:
        coin_details = getCoinDetails(pf.key())
        coins.append({
            "id": str(pf.key()),
            "units": float(pf.val()),
            "symbol": coin_details["symbol"],
            "name": coin_details["name"],
            "image": coin_details["image"],
            "current_price": round(coin_details["current_price"],2)
        })
        portfolio_value += (coin_details["current_price"]*float(pf.val()))
    return coins, portfolio_value

def getTransactions(email):
    transactions=[]
    total_invested = 0
    for tsn in db.child("transactions").get():
        if tsn.val()["email"] == email:
            tsn_dict = tsn.val()
            coin_details = getCoinDetails(tsn_dict["coin"])
            tsn_dict["name"] = coin_details["name"]
            tsn_dict["symbol"] = coin_details["symbol"]
            tsn_dict["image"] = coin_details["image"]
            tsn_dict['time'] = time.ctime(tsn.val()['timestamp'])
            transactions.append(tsn_dict)
            if tsn.val()['mode'] == 'BUY':
                total_invested += tsn.val()["usd"]
            else:
                total_invested -= tsn.val()["usd"]
    if len(transactions) > 0:
        return transactions, total_invested
    else:
        return None, 0

@portfolio.route("/test")
def test():
    curr_val, value = getPortfolio("adityakotkar75")
    # curr_val = getTransactions("adityakotkar75@gmail.com")
    # curr_val = getCoinDetails("bitcoin")[0]
    # db.child("portfolios").child("xyz").update({"bitcoin": 100})
    return f"<h1>{curr_val}-{value}</h1>"