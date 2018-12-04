I made this project to compare the public sentiment (Twitter users) of any particular movie showing with the score that is aggregated by Rotten Tomatoes.

The application of this code is used more as an educational tool to practice pulling real life functional data and making a practical analysis out of it. I used scientific computing tools such as NumPy, Pandas, and matplotlib to provide a clean structure for the aggregated data and visuals.

There are 3 python files and 5 images attached to this project.

1.	twitter_credentials.py
•	holds your own unique access tokens to the Twitter API
•	must sign up for developer access on Twitter website

2.	initial_pull.py
•	how to execute a search query on Twitter and how to aggregate specific attributes
•	twitter allows a maximum of 100 search results per request

3.	appending_tweets_and_visuals.py
•	how to append additional 100-search batches and specific step by step instructions to make sure the structure of the table is correct
•	how to visualize your data (pie charts, bar graphs, line graphs, annotations) by using important matplotlib functions
•	at the conclusion, you will see that I calculated the raw sentiment score of Twitter users over its total possible score to compare to the audience score provided by Rotten Tomatoes

4,5,6: bar_graph.png, pie_graph.png, time_series.png
•	bar graph shows difference between Rotten Tomatoes audience score and the sentiment score calculation of Twitter users
•	pie graph shows distribution of positive, neutral, and negative tweets
•	line graph(time-series chart) shows the moving average of the sentiment score between the first and last tweet I collected (November 19-November 30)

7,8: whole_screen.jpg, example.jpg
•	screenshotted some examples from my table to show what the output looks like and how the TextBlob engine works
