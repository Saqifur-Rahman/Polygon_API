import os
from flask import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
from datetime import date
import time

app = Flask(__name__)
app.secret_key = "hello_world"

# Function - returns name of the Month
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

# Function - returns no. of days in month
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

    # handling condition for february
    if int(year) % 4 == 0 and int(year) % 100 != 0:
        month_range["02"] = ["01","29"]
    elif int(year) % 100 == 0:
        month_range["02"] = ["01","28"]
    elif int(year) % 400 ==0:
        month_range["02"] = ["01","29"]
    else:
        month_range["02"] = ["01","28"]

    return month_range[str(month)]

# Function - plots chart
def plotChart(month, year):
    month_range = monthRange(month, year)

    # making API call
    key = "9pq_4hMsbkqRCk9X7zgBlyuujMLgs6iA"
    URL = f"https://api.polygon.io/v2/aggs/ticker/X:BTCUSD/range/1/day/{year}-{month}-{month_range[0]}/{year}-{month}-{month_range[1]}?adjusted=true&sort=asc&limit=120&apiKey={key}"
    r = requests.get(url = URL)
    
    # storing JSON response
    data = r.json()
    date = []
    high = []
    low = []

    for i in range(data["resultsCount"]):
        result = data["results"][i]
        date.append(i+1)
        high.append(result["h"])
        low.append(result["l"])

    # reomve image if exists
    folder_path = (r'static/')
    folder = os.listdir(folder_path)
    for image in folder:
        if image.endswith('.png'):
            os.remove(os.path.join(folder_path,image))

    # plot the line chart
    plt.plot(date, high, label = "highest price")
    plt.plot(date, low, label = "lowest price")
    plt.xlabel(f"Days [{monthName(month)} {year}]")
    plt.ylabel("Price [USD]")
    plt.title("Range of Prices of Bitcoin")
    plt.legend()
    filename = f'{int(time.time())}.png'
    plt.savefig(f"static/{filename}")
    plt.clf()
    return filename

# Route for BTC-Range
@app.route("/btc-range")
def home():
    return render_template("btc_range.html")

# Route for results page
@app.route("/result", methods=['POST'])
def result():
    if request.method == 'POST':
        month = request.form['month']
        year = request.form['year']

        # invalid date
        if int(month) > date.today().month:
            flash("Data not available for this month.")
            return render_template("home.html")

        filename = plotChart(month, year)
        return render_template("result.html", filename=filename)

# Route for prices list of coins
@app.route("/")
def coins_list():
    # making API call
    URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false"
    r = requests.get(url = URL)

    # storing JSON response
    data = r.json()
    return render_template("coins_list.html", data=data)

if __name__ == '__main__':

    app.run(debug=True)
