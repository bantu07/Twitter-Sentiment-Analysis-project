# Twitter-Sentiment-Analysis-project

The business objective of this project is to Extract the tweets and perform the sentiment analysis get the insights from the visuals.

Packages Required are:
1. Tweepy
2. NLTK
3. json
4. requests
5. TextBlob
6. Flask
7. sklearn.

Project life cycle:

1. Data collection: scraping the data from the twitter 
2. Data pre-processing
3. Perform Sentiment/Emotional Analysis using NRC Lexicons
4. Visualization : Plot the graphs
5. Build Webapp by using Flask. Flask is a web framework. This means flask provides you with tools, libraries, and technologies that allow you to build a web application. This web application can be some web pages, a blog, a wiki or go as big as a web-based calendar application or a commercial website. 
6. Deployment on Heroku cloud platform.

The steps involved are:

  1. Extract the Tweets by screen_name/search keywords/#hashtags from twitter by using tweepy API.
  2. Data Preprocessing here in this phase the data which is extracted is in unstructured format need to clean the data by removing the      punctuations, special symbol, digits, emoji's, html links, whitespace, stopwords.
  3. Sentiment Analysis: After data cleaning perform Sentiment Analysis find athe polarity values for each tweet by using TextBlob        package here will get the polarity value for positive, neutral, negative.
  4. From TextBlob we can also get Subjective/Objective score, subjective defines the personal perspectives, feelings, or opinions entering the decision making process whereas Objective is goal oriented/hard facts.
  5. Need to plot the visualization of most common words, sentiment analysis, Twitter Platform, Emotional Analysis.
  6. Create the bag of words and plot the Wordcloud. It is also possible to plot both positive and negative wordcoluds.
  7. Find the frequency of the words, apply DTF/IFDTF technique which will be later useful in LDA Topic Extraction.
  8. Build Web Application by using Flask framework.
  9. Deploy the module in the cloud platform(server) by using Heroku.
  
