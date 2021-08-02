# Crypto_Trendalyzer

## Prerequisites
1. [Python 3.6+](https://www.python.org/downloads/)
2. [Git](https://git-scm.com/downloads)
3. [News API Key](https://newsapi.org/)

## Setup
1. Clone the git repository.
```
git clone https://github.com/Saqifur-Rahman/Crypto_Trendalyzer.git
```

2. Inside the cloned repo, make a virtual environment. (Optional)
```
pip install virtualenv
virtualenv venv
venv\Scripts\activate
```

2. Install the dependencies.
```
pip install -r requirements.txt
```

3. Generate key on News API, and update `main.py`
```
API_KEY = "YOUR_NEWS_API_KEY"
```

4. Run the server.
```
python main.py
```

## Specifications
- Framework: Flask (Python)
- Frontend: HTML, CSS, JavaScript, JQuery, Bootstrap 4
- APIs used:
  1. [CoinGecko](https://www.coingecko.com/en/api) - Cryptocurrency API
  2. [Chart.js](https://www.chartjs.org/) - For producing charts
  3. [News API](https://newsapi.org/) - News related to cryptocurrencies

## Key Featues
- **Coins**: List of coins with live prices, percentage change, market cap etc. with search and sort features.
- **Coin Chart**: Clicking on coin redirects to the coin page, where charts showing the performance of coin in intervals of a day, week, month, year, alltime are available.
- **News & Events**: Latest and Trending news, events related to cryptocurrencies.