import sys
import os
from flask import Flask, render_template, request, flash
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
from datetime import date

app = Flask(__name__)
app.secret_key = "hello_world"

def monthName(month):
    month_name = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }
    return month_name[month]

def monthRange(month, year):
    month_range = {
        "01": ["01","31"],
        "03": ["01","31"],
        "04": ["01","30"],
        "05": ["01","31"],
        "06": ["01","30"],
        "07": ["01","31"],
        "08": ["01","31"],
        "09": ["01","30"],
        "10": ["01","31"],
        "11": ["01","30"],
        "12": ["01","31"]
    }

    if int(year) % 4 == 0 and int(year) % 100 != 0:
        month_range["02"] = ["01","29"]
    elif int(year) % 100 == 0:
        month_range["02"] = ["01","28"]
    elif int(year) % 400 ==0:
        month_range["02"] = ["01","29"]
    else:
        month_range["02"] = ["01","28"]

    return month_range[str(month)]


def plotChart(month, year):
    month_range = monthRange(month, year)

    key = "9pq_4hMsbkqRCk9X7zgBlyuujMLgs6iA"
    URL = f"https://api.polygon.io/v2/aggs/ticker/X:BTCUSD/range/1/day/{year}-{month}-{month_range[0]}/{year}-{month}-{month_range[1]}?adjusted=true&sort=asc&limit=120&apiKey={key}"
    r = requests.get(url = URL)
    data = r.json()
    date = []
    high = []
    low = []

    for i in range(data["resultsCount"]):
        result = data["results"][i]
        date.append(i+1)
        high.append(result["h"])
        low.append(result["l"])

    if os.path.exists("static/plot.png"):
        os.remove("static/plot.png")

    plt.plot(date, high, label = "highest price")
    plt.plot(date, low, label = "lowest price")
    plt.xlabel(f"Days [{monthName(month)} {year}]")
    plt.ylabel("Price [USD]")
    plt.title("Range of Prices of Bitcoin")
    plt.legend()
    plt.savefig("static/plot.png")
    plt.clf()
    return

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/result", methods=['POST'])
def result():
    if request.method == 'POST':
        month = request.form['month']
        year = request.form['year']

        # invalid date
        if int(month) > date.today().month:
            flash("Data not available for this month.")
            return render_template("home.html")

        plotChart(month, year)
        return render_template("result.html")

if __name__ == '__main__':
    app.run(debug=True)
