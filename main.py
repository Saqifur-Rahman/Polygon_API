import numpy as np
import matplotlib.pyplot as plt
import requests

def main():
    key = "9pq_4hMsbkqRCk9X7zgBlyuujMLgs6iA"
    URL = f"https://api.polygon.io/v2/aggs/ticker/X:BTCUSD/range/1/day/2021-05-01/2021-05-10?adjusted=true&sort=asc&limit=120&apiKey={key}"
    r = requests.get(url = URL)
    data = r.json()
    date = []
    high = []
    low = []

    # print(json.dumps(data, indent = 2))
    for i in range(data["resultsCount"]):
        result = data["results"][i]
        # print(i, result["h"])
        date.append(i)
        high.append(result["h"])
        low.append(result["l"])

    # print(date, high, low) 
    plt.plot(date, high, label = "highest price")
    plt.plot(date, low, label = "lowest price")
    plt.xlabel("Days (May 2021)")
    plt.ylabel("Price (USD)")
    plt.title("Range of Prices of Bitcoin for 10 days")
    plt.legend()
    plt.savefig("plot.png")

if __name__ == '__main__':
    main()

