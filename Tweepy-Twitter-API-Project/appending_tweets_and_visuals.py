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

	def tweets_to_data_frame(self, tweets):
		df = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns = ['tweets']) 
		df.index.name = 'Grouped Tweets'  				
		df['date'] = np.array([tweet.created_at for tweet in tweets]) 
		df['date'] = pd.to_datetime(df.date) 
		df['id'] = np.array([tweet.id for tweet in (tweets)])	

		return df 


	def clean_tweet(self, tweet):  
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
	
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
	take the tweet id# of the oldest pulled tweet and set it as the max_id for the next batch of 100 tweets 
	(the tweet of this id will be ignored in the next set if there are actually older tweets available)
	"""
	tweets = API.search(q = "just saw creed 2 -RT" , result_type = 'recent', tweet_mode = 'extended', since_id = 'none', max_id='none', count=100)

	df = tweet_analyzer.tweets_to_data_frame(tweets) 
	df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']]) 
	df['moving_average'] = df['sentiment'].sort_index(ascending=False).expanding().mean() 

	
	"""
	since we have yet to add column names yet, it will be easy to append to the end of our previous data frame 
	"""

	#df.to_csv('creed.csv', header=False, mode='a') 

	"""
	- at this point, you have a new collection of tweets on top of the original batch you pulled
	- continue to change the max_id if you want additional older tweets
	- the only issue that is specific to my dataframe is that the running average of the tweet sentiment has to be recalculated 
	- once you are done appending your table, be sure to comment out the most recent df.to_csv appending line so we don't append anything else by accident 
	- uncomment each additional line of code (next is pd.read_csv code) to understand each step
	"""


	#df = pd.read_csv('creed.csv')
	"""
	it's important to not add column names until you are done pulling the amount of tweets you want to have in your data set
	"""

	#df.columns = ['Grouped Tweets', 'tweets', 'date', 'id', 'sentiment', 'moving_average']
	#df['moving_average'] = df['sentiment'].sort_index(ascending=False).expanding().mean()
	#df.to_csv('creed.csv', mode='w')

	"""
	- once you overwrite the file with the correctly calculated data points, I would comment out the most recent df.to_csv writing code again to avoid adding new changes
	- also comment out the df.columns line since a new index that numbers each tweet will automatically be added and will confuse the output for the headers 
	- you can now run an update on the visual tools you used previously 
	- uncomment visuals code when ready to use 
	"""


	### VISUALS
	"""
	df = pd.read_csv('creed.csv')
	df['date'] = pd.to_datetime(df.date)
	time_series_graph = pd.Series(data=df['moving_average'].values, index=df['date']) 
	fig = time_series_graph.plot(figsize=(7,7), color='r')
	fig.set_yticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
	fig.set_title('Sentiment Score of Creed 2')

	plt.show(fig)


	pie_sentiment = pd.Series(data=df['sentiment'].value_counts())
	pie_chart = pie_sentiment.plot(figsize=(5,5), kind='pie', autopct='%1.1f%%', title='Sentiment of Creed 2')
	pie_chart.legend(['Positive', 'Neutral', 'Negative'])

	plt.show(pie_chart)	

	#absolute sentiment score out of possible 2 points 	
	sentiment_score = round((df['moving_average'][0] + 1)/2*100, 2)
	sentiment_score_percent = str(sentiment_score) + '%'
	print(sentiment_score_percent)

	sources = ['Rotten Tomatoes', 'Twitter']
	#score pulled from rotten tomatoes website 
	scores = [88.00, 77.19]
	positions = [0,1]

	bar_graph = plt.bar(positions, scores, width=0.5)
	bar_graph[0].set_color('r')
	bar_graph[1].set_color('b')

	plt.xticks(positions, sources)
	plt.ylabel('Audience Score' + ' (%)')
	plt.title('Sentiment Analysis of Creed 2')
	plt.yticks(np.arange(0, 110, step=10))
	plt.annotate(('88.00%'),(-.05,94))
	plt.annotate(('77.19%'), (.95,83))
	plt.show(bar_graph)
	"""