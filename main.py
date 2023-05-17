import requests
import os
from dotenv import load_dotenv
import datetime


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Loads environment variables from .env local file.
load_dotenv("C:/Python/EnvironmentVariables/.env")
alpha_vantage_api_key = os.environ.get("alpha_vantage_api_key")
news_api_key = os.environ.get("news_api_key")


# Makes Telegram bot send message to specific user.
def telegram_bot_send_text(bot_message):
    bot_token = os.environ.get("rain_alert_bot_token")
    bot_chat_id = os.environ.get("rain_alert_chat_id")
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


# Gets data from stock Alpha Vantage Stock API
params_stock = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "outputsize": "compact",
    "apikey": alpha_vantage_api_key
}
response = requests.get(url=STOCK_ENDPOINT, params=params_stock)
stock_data = response.json()["Time Series (Daily)"]
yesterday = str(datetime.datetime.today() - datetime.timedelta(days=1))[:10]
# The tdby variables is an acronym for 'the day before yesterday'
tdby = str(datetime.datetime.today() - datetime.timedelta(days=2))[:10]
yesterday_close_price = float(stock_data[yesterday]["4. close"])
tdby_close_price = float(stock_data[tdby]["4. close"])

# Gets price variation from yesterday in comparison to the day before and rounds it to 4 decimals.
price_variation = round((yesterday_close_price - tdby_close_price) / tdby_close_price, 4)

# Adjust to desired minimum variation to trigger Telegram message.
minimum_variation = 0.0001
if abs(price_variation) >= minimum_variation:
    # Gets top 3 articles about company from yesterday from news API
    params_news = {
        "q": COMPANY_NAME,
        "from": yesterday,
        "sortBy": "popularity",
        "apiKey": news_api_key
    }
    response_news = requests.get(NEWS_ENDPOINT, params=params_news)
    articles = response_news.json()["articles"][:3]

    # List comprehension to extract title and article from the articles list of dictionaries.
    news = [(article["title"], article["description"]) for article in articles]

    # Sends 3 messages via Telegram containing the stock and news info
    for (headline, brief) in news:
        message = ""
        if price_variation > 0:
            message += STOCK_NAME + f":🔺{price_variation*100}%"
        else:
            message += STOCK_NAME + f":🔻{price_variation*100}%"
        message += f"\nHeadline: {headline}\nBrief: {brief}"
        print(telegram_bot_send_text(message))
