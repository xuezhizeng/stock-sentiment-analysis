import sys
import tweepy
import requests
from textblob import TextBlob


def main():

    # set twitter api credentials
    consumer_key= 'TWITTER_CONSUMER_KEY'
    consumer_secret= 'TWITTER_CONSUMER_SECRET'
    access_token='TWITTER_ACCESS_TOKEN'
    access_token_secret='TWITTER_ACCESS_TOKEN_SECRET'

    # access twitter api via tweepy methods
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitter_api = tweepy.API(auth)

    # set name of csv file to save stock prices
    file_name = 'stock_prices.csv'

    # prompt user to enter a stock ticker
    ticker = input('Enter a stock ticker symbol (e.g. AAPL, FB): ').upper()

    # fetch tweets for user-entered stock ticker
    tweets = twitter_api.search(ticker, count=100)

    get_sentiment(tweets)
    get_stock_prices(ticker, file_name)


def get_sentiment(tweets):
    # checks twitter sentiment of a set of tweets
    # returns true if positive sentiment is stronger than negative sentiment

    positive_tweets, negative_tweets = 0, 0

    for tweet in tweets:
        analysis = TextBlob(tweet.text).sentiment
        if analysis.polarity > 0:
            positive_tweets +=1
        if analysis.polarity < 0:
            negative_tweets +=1

    print('Positive tweet count: %s' % positive_tweets)
    print('Negative tweet count: %s' % negative_tweets)

    if positive_tweets > negative_tweets:
        print('This stock has positive sentiment.')
    else:
        print('This stock has negative sentiment.')


def get_stock_prices(ticker, file_name):
    # download file from google finance
    url = 'http://www.google.com/finance/historical?q=NASDAQ%3A'+ticker+'&output=csv'
    r = requests.get(url, stream=True)

    if r.status_code != 400:
        with open(file_name, 'wb') as f:
            for chunk in r:
                f.write(chunk)
        f.close()

    if r.status_code == 400:
        sys.exit('Error fetching stock prices, please try again with a valid ticker symbol.')


# def predict_stock_price()
    # to do: predict price with keras neural net regression based on twitter sentiment


if __name__ == '__main__':
    main()
