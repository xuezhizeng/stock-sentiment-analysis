import sys
import tweepy
import requests
from textblob import TextBlob

# set twitter api credentials
consumer_key= 'TWITTER_CONSUMER_KEY'
consumer_secret= 'TWITTER_CONSUMER_SECRET'
access_token='TWITTER_ACCESS_TOKEN'
access_token_secret='TWITTER_ACCESS_TOKEN_SECRET'

# access twitter api via tweepy methods
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)

file_name = 'stock_prices.csv'


def get_sentiment(ticker, num_tweets):
    # checks twitter sentiment of user-entered ticker symbol
    # returns true if positive sentiment is stronger than negative sentiment

    tweets = twitter_api.search(ticker, count=num_tweets)
    positive_tweets, negative_tweets = 0, 0

    for tweet in tweets:
        analysis = TextBlob(tweet.text).sentiment
        if analysis.polarity > 0:
            positive_tweets +=1
            next
        if analysis.polarity < 0:
            negative_tweets +=1

    if positive_tweets > negative_tweets:
        return True


def get_stock_prices(ticker):
    # download file from google finance
    url = 'http://www.google.com/finance/historical?q=NASDAQ%3A'+ticker+'&output=csv'
    r = requests.get(url, stream=True)

    if r.status_code != 400:
        with open(file_name, 'wb') as f:
            for chunk in r:
                f.write(chunk)

        f.close()

        return True


# def predict_stock_price()
# to do: predict price with keras neural net regression based on twitter sentiment


# prompt user to enter a stock ticker
ticker = input('Enter a stock ticker symbol (e.g. AAPL, FB): ').upper()

# check whether twitter sentiment is positive
if get_sentiment(ticker, num_tweets=100):
    print('This stock has positive sentiment.')
else:
    print('This stock has negative sentiment.')

# fetch stock price data and output to csv file
if not get_stock_prices(ticker):
    print('Error fetching stock prices, please try again with a valid ticker symbol.')
    sys.exit()
