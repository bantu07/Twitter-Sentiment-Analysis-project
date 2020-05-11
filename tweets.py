from __future__ import print_function

import re
import string
from collections import Counter

import pandas as pd
import tweepy
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob


def make_maps(tweetsDataframe, ldda):
    subjective_plot = []
    sentiment_pie = []
    retweet_table = []
    source_plot = []
    lda_table = []

    ########################################
    # for the Sentiment plot :: pie chart
    sentiment_pie.append(["Sentiment", "Tweets"])
    sentiment_count = tweetsDataframe["sentiments_group"].value_counts()
    sentiment_count = sentiment_count.to_dict()
    for key, value in sentiment_count.items():
        temp = [key, value]
        sentiment_pie.append(temp)
    ########################################
    ########################################
    # for the sources plot ::
    source_plot.append(["Twitter Client", "Users"])
    source_count = tweetsDataframe["source"].value_counts()[:5][::-1]
    source_count = source_count.to_dict()
    for key, value in source_count.items():
        temp = [key, value]
        source_plot.append(temp)
    #######################################
    ########################################
    # Most Famous Tweet Table :: Table_Chart
    retweet_table.append(["Tweet Text", "ReTweets"])
    df = tweetsDataframe[['translate', 'retweet_count']].drop_duplicates().sort_values(['retweet_count'],
                                                                                       ascending=False)[:15]
    for key, value in zip(df['translate'], df['retweet_count']):
        temp = [key, value]
        retweet_table.append(temp)

    new_list = []
    for item in tweetsDataframe['translate']:
        new_item = [item]
        new_list.append(new_item)

    text = ""
    text_tweets = new_list
    length = len(text_tweets)

    for i in range(0, length):
        text = text_tweets[i][0] + " " + text

    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    tokenized_words = cleaned_text.split()

    final_words = [word for word in tokenized_words if word not in stopwords.words('english')]
    emotion_list = []
    # Emotion- plot
    d = pd.read_csv('emo_lex.csv', encoding='UTF-8')
    d1 = d[d.association == 1]

    emoji1, emo_word = [], []
    for i, j in zip(d1.word, d1.emotion):
        if i in final_words:
            emo_word.append(i)
            emoji1.append(j)

    coun = Counter(emoji1)
    keys, values, emotion_table = [], [], []
    for k, y in coun.items():
        keys.append(k)
        values.append(y)

    emotion_table.append(['Emotion', 'counts'])
    for kk, vv in zip(keys, values):
        emotion_table.append([kk, vv])

    #######################################
    # Subjective Plot
    subjective_plot.append(["Subjective", "Tweets"])
    subjective_count = tweetsDataframe["subjectivity_group"].value_counts()
    subjective_count = subjective_count.to_dict()
    for key, value in subjective_count.items():
        temp = [key, value]
        subjective_plot.append(temp)

    # LDA Table
    lda_table.append(["Topic Nos", "Topics"])
    df = ldda
    for key, value in zip(df['Topic Nos'], df['Topics']):
        temp = [key, value]
        lda_table.append(temp)

    return emotion_table[:], source_plot, sentiment_pie, retweet_table, subjective_plot, lda_table


def QueryTwitter(search_string):
    consumer_key = 'QOVUHBw7FQzmYmBSYhyiSQpWA'
    consumer_secret = 'eXPIoug0STIGZvudBn4gtpoEfo7rPKCi2fUTFxzrVVEV4uje2d'
    access_token = '2892126056-rfTFA19Obtwkkr2o8z8oL520T2zoL4GdWQRI4c7'
    access_secret = 'gm1fa52Kvu2XzkaKU1Sp4rGqAlnQPmd2pwosrYOsFCn1y'

    auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    tweet_list = []
    search_string = search_string + ' -filter:retweets -#tgif'
    for tweet in api.search(q=search_string, count=100, lang="en"):
        tweet_list.append(tweet)

    (word_freqs_js, max_freq, all_sentence, tweet_Data, ldda) = filter_tweets(tweet_list)

    (emotion_plot, sources_plot, sentiment_pie, retweet_table, subjective_plot, lda_table) = make_maps(tweet_Data,ldda)

    return emotion_plot, word_freqs_js, max_freq, sources_plot, sentiment_pie, retweet_table, subjective_plot, lda_table



def filter_tweets(tweets):
    all_sentence = []
    id_list = [tweet.id for tweet in tweets]
    tweet_Data = pd.DataFrame(id_list, columns=['id'])
    tweet_Data["text"] = [tweet.text for tweet in tweets]
    tweet_Data["retweet_count"] = [tweet.retweet_count for tweet in tweets]

    Sentiments_list = []
    Sentiments_group = []
    Subjectivity_list = []
    Subjectivity_group = []
    tweet_text_list = []
    tweet_source = []
    tweet_translation = []
    tweet_location_list = []

    for tweet in tweets:
        raw_tweet_text = tweet.text
        message = TextBlob(tweet.text)
        location = tweet.author.location
        source = tweet.source
        tweet_source.append(source)

        message = str(message)
        new_message = ""
        for letter in range(0, len(message)):
            current_read = message[letter]
            if ord(current_read) > 126:
                continue
            else:
                new_message = new_message + current_read
        message = new_message
        tweet_translation.append(message[:120])
        message = TextBlob(message)

        sentiment = message.sentiment.polarity
        if (sentiment > 0):
            Sentiments_group.append('positive')
        elif (sentiment < 0):
            Sentiments_group.append('negative')
        else:
            Sentiments_group.append('neutral')

        subjectivity = message.sentiment.subjectivity
        if (subjectivity > 0.4):
            Subjectivity_group.append('subjective')
        else:
            Subjectivity_group.append('objective')

        Sentiments_list.append(sentiment)
        Subjectivity_list.append(subjectivity)
        tweet_text_list.append(raw_tweet_text)
        tweet_location_list.append(location)

    tweet_Data["sentiments"] = Sentiments_list
    tweet_Data["sentiments_group"] = Sentiments_group
    tweet_Data["subjectivity"] = Subjectivity_list
    tweet_Data["subjectivity_group"] = Subjectivity_group
    tweet_Data["location"] = tweet_location_list
    tweet_Data["text"] = tweet_text_list
    tweet_Data["source"] = tweet_source
    tweet_Data["translate"] = tweet_translation

    for a in tweet_Data['translate']:
        all_sentence.append(a)
    str1 = " "
    b = str1.join(all_sentence)
    b = re.sub(r"http\S+", "", b)
    b = ' '.join(re.sub("(#[A-Za-z0-9]+)|(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", b).split())
    all_sentence = b.split()

    text = b

    stripped_text = [word for word in text.split() if
                     word.isalpha() and word.lower() not in stopwords.words('english') and len(word) >= 2]
    word_freqs = Counter(stripped_text)
    word_freqs_cloud = dict(word_freqs)
    add = sorted(word_freqs_cloud.items(), key=lambda x: x[1], reverse=True)
    word_freqs = dict(add[:100])

    word_freqs_js = []

    for key, value in word_freqs.items():
        temp = {"text": key, "size": value}
        word_freqs_js.append(temp)

    max_freq = max(word_freqs.values())
    tweet_Data["Word_freq"] = tweet_source

    all_sentence_lda = [word for word in all_sentence if
                        word.isalpha() and word.lower() not in stopwords.words('english')]

    ldda = lda_process(all_sentence_lda)
    return word_freqs_js, max_freq, all_sentence, tweet_Data, ldda

def lda_process(corpuss1):
    stop = stopwords.words('english')
    cv = CountVectorizer(stop_words=stop)
    cv.fit(corpuss1)
    X = cv.fit_transform(corpuss1).toarray()
    n_components = 10
    n_top_words = 20

    lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    lda.fit(X)
    tf_feature_name = cv.get_feature_names()
    lda_tab = print_top_words(lda, tf_feature_name, n_top_words)
    return lda_tab


def print_top_words(model, feature_names, n_top_words):
    lda_comp = []
    for topic_idx, topic in enumerate(model.components_):
        message = " "
        message += "".join([feature_names[i] + ' '
                            for i in topic.argsort()[:-n_top_words - 1:-1]])
        lda_comp.append(message + '.')

    t = ["Topic %d:" % i for i in range(1, 11)]
    ld = pd.DataFrame(t, columns=['Topic Nos'])
    ld['Topics'] = lda_comp
    return ld

