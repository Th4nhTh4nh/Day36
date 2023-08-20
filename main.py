import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "TeslaInc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "HD3JSZF71DNKQ5TS"
NEWS_API_KEY = "099a421575de484ab8822e58e61317aa"

ACCOUNT_SID = "ACbe87d80026259f434f2544ab21b6e6fa"
AUTH_TOKEN = "7ff8e1c52061dc664626c5c4b9214418"

news_params = {
    "q": COMPANY_NAME,
    "pageSize": 3,
    "apiKey": NEWS_API_KEY,
}

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]
yesterday_closing_price = data_list[0]["4. close"]
b4yesterday_closing_price = data_list[1]["4. close"]

print(f"Yesterday closing price: {yesterday_closing_price}")
print(f"Day before yesterday closing price: {b4yesterday_closing_price}")

difference = float(yesterday_closing_price) - float(b4yesterday_closing_price)

up_down = None
if difference > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"

diff_percent = round(difference / float(b4yesterday_closing_price)) * 100
print("Diff_percent = {:.2f}%".format(diff_percent))

if diff_percent > 1:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_data = news_response.json()["articles"]
    articles = [item for item in news_data]
    format_sms = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}"
        for article in articles
    ]
    print(format_sms)
    for article in format_sms:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            body=article,
            from_="+17622494058",
            to="+33644629051",
        )
        print("Done!")
