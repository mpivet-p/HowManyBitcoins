import tweepy
import time
from datetime import datetime
import random
import requests

def auth():
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def get_random_date():
    start = 1367193601
    yesterday = time.time() - 86400
    random_date = random.randrange(start, int(yesterday))
    return random_date

def get_historical_btc_price(date):
    response = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/history?date=" + date.strftime("%d-%m-%Y"))
    json = response.json()
    return(json["market_data"]["current_price"]["usd"])

def get_current_btc_price():
    response = requests.get("https://www.blockchain.info/ticker")
    json = response.json()
    return(json["USD"]["last"])

def date_extention(number): 
    if number % 10 == 1: 
        return 'st'
    if number % 10 == 2: 
        return 'nd'
    if number % 10 == 3 and number != 13: 
        return 'rd'
    return "th"

def check_mentions(api, date, current_price, historical_price):
    tweet = "If you had bought $1,000 worth of bitcoin on " + date.strftime("%B %d" + date_extention(date.day) + ", %Y")
    tweet += ", you would have " + str(round(1000 / historical_price, 2))
    tweet += str(" bitcoins or $")
    comma = "{:,}".format(int(current_price * 1000 / historical_price))
    tweet += str(comma) + str(" today :)")
    api.update_status(status = tweet)

def main():
    api = auth()
    date = get_random_date()
    current_price = get_current_btc_price()
    historical_price = get_historical_btc_price(datetime.fromtimestamp(date))
    check_mentions(api, datetime.fromtimestamp(date), current_price, historical_price)

if __name__ == "__main__":
    main()
