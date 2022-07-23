import requests
import html
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
STOCK_API_key = "QDII5B2RG8C1YI48"
url = f'https://www.alphavantage.co/query'

## STEP 1: Use https://www.alphavantage.co

url_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_key,
}

response = requests.get(url, params=url_params)
response.raise_for_status()
data = response.json()
print(data)

closing_price_list = [data["Time Series (Daily)"][k]["4. close"] for k in data["Time Series (Daily)"]]
last_closing_price = float(closing_price_list[0])
previous_closing_price = float(closing_price_list[1])

percent_stock_change = (last_closing_price-previous_closing_price)/last_closing_price * 100

## STEP 2: Use https://newsapi.org
#get the first 3 news pieces for the COMPANY_NAME.
message = ""
def get_news():
    NEWS_API_KEY = "cfca006c630d4f94a352f0a7c8dcf4bd"
    NEWS_URL= "https://newsapi.org/v2/everything"

    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }

    news_response = requests.get(NEWS_URL, params=news_params)
    news_response.raise_for_status()
    articles = html.unescape(news_response.json()["articles"])

    first_3_articles = articles[:3]
    #format message
    global message
    message = f"{STOCK}: {percent_stock_change}"
    for i in range(len(first_3_articles)):
        message = message + f"\nHeadline: {first_3_articles[i]['title']}\nBrief: {first_3_articles[i]['description']}"

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
def send_text(txt_message: str):
    ACCOUNT_SID = "AC73816bd82bb4312d753a2c535bce7b1b"
    AUTH_TOKEN = "d311f0190f510a79277e54b1500e2e7b"
    MY_PHONE_NUM = "+15163101536"
    TWILIO_PHONE_NUM = "+13392175296"

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
        .create(body=f"{txt_message}",
                from_=f'{TWILIO_PHONE_NUM}',
                to=f'{MY_PHONE_NUM}')
    print(message.status)

if abs(percent_stock_change) > 5:
    if percent_stock_change > 5:
        percent_stock_change = f"🔺{round(percent_stock_change)}%"
    else:
        percent_stock_change = f"🔻{round(abs(percent_stock_change))}%"
    get_news()
    send_text(message)
