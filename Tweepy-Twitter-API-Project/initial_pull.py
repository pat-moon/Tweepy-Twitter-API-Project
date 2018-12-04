import twitter_credentials

from tweepy import OAuthHandler
from tweepy import API


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

from textblob import TextBlob
import re
import csv 


class TwitterConnection():

	def authenticate_twitter_app(self):
		self.auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
		self.auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
		self.twitter_connection = API(self.auth)

		return self.twitter_connection


class TweetAnalyzer(): 
	"""
	the attributes of each tweet are listed in the API documentation...
	https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
	"""	
	def tweets_to_data_frame(self, tweets):
		df = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns = ['tweets']) 
		df.index.name = 'Grouped Tweets'  				
		df['date'] = np.array([tweet.created_at for tweet in tweets]) 
		df['date'] = pd.to_datetime(df.date) 
		df['id'] = np.array([tweet.id for tweet in (tweets)])	
		return df 


	
	# a regex to clean up special characters from each tweet 
	def clean_tweet(self, tweet): 
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
	
	# TextBlob's sentiment.polarity function will tell us if the tweet is positive, neutral, or negative 
	
	def analyze_sentiment(self, tweet):
		analysis = TextBlob(self.clean_tweet(tweet)) 

		if analysis.sentiment.polarity > 0: 
			return 1
		elif analysis.sentiment.polarity == 0:
			return 0
		else: 
			return -1



if __name__ == "__main__":


	API = TwitterConnection().authenticate_twitter_app()
	tweet_analyzer = TweetAnalyzer()

	"""
	the search parameters that twitter allows are documented on https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
	-RT incorporates a standard operator that allows you exclude retweets in the query
	""" 
	tweets = API.search(q = "just saw creed 2 -RT" , result_type = 'recent', tweet_mode = 'extended', since_id = 'none', max_id='none', count=100)

	df = tweet_analyzer.tweets_to_data_frame(tweets) 
	df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']]) 
	# .expanding().mean() is panda's built in running average function 
	df['moving_average'] = df['sentiment'].sort_index(ascending=False).expanding().mean() 

# up to this point, I queried tweets with the keywords I wanted and pulled specific attributes of those tweets

# showing below how to export the dataframe and add some basic visualizations using pandas and matplotlib functions 

	df.to_csv('creed.csv', header=False, mode='w') 
		

	time_series_graph = pd.Series(data=df['moving_average'].values, index=df['date']) 
	fig = time_series_graph.plot(figsize=(5,5), color='r')
	fig.set_yticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])

	plt.show(fig)


	pie_sentiment = pd.Series(data=df['sentiment'].value_counts())
	pie_chart = pie_sentiment.plot(figsize=(5,5), kind='pie', autopct='%1.1f%%', title='Sentiment of Creed 2')
	pie_chart.legend(['Positive', 'Neutral', 'Negative'])
	
	plt.show(pie_chart)	

# so far this is all good if you are fine with the amount of tweets you pull off of one request (maximum allowed is 100)
# for data analysis purposes, it would be useful to have a larger sample size 
 