# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 17:06:47 2018

@author: Robert Schuldt
@email: rfschuldt@uams.edu

Sentiment Analysis Twitter
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#Import collected tweets from CSV file

tweets = pd.read_csv('20180728-132743.csv', header = None, encoding = 'utf-8')

display(tweets.head(10))



#rename my columbs with relevant titles
tweets.columns =['id', 'tweet', 'date' , 'source']

"""

Tested with single tweet to remove garbage hashtags and @ symbols


import re
review = re.sub('[^a-zA-Z]', ' ', tweets['tweet'][0])
review = review.lower()

Sucess

"""
import re

#Create vector of length
tweet_length = []
    
for i in range(0, 14457):
    length = len(tweets['tweet'][i])
    tweet_length.append(length)
    
#Converting list to a data frame so I can append to existing database
    
tweet_length = pd.DataFrame(tweet_length)
tweet_length.columns= ['length']

#Join on outer side the two dataframes so I have the information I want in one dataframe

tweets = tweets.join(tweet_length)

mean = np.mean(tweets['length'])
print("The average length of a tweet is: {}".format(mean))

#Now we go and create a sentiment analysis

from textblob import TextBlob
#This step will remove garbage we don't want in the tweets
def clean_tweet(tweet):
    ''' This will clean out all the special characters and garbage
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
def analize_sentiment(tweet):
    
    '''
    Textblob classifies the polarity of a tweet
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

#Create a new column
tweets['SA'] = np.array([ analize_sentiment(tweet) for tweet in tweets['tweet'] ])

# How many were positive negative and neutral

positive_tweets = [tweet for index, tweet in enumerate(tweets['tweet']) if tweets['SA'][index]> 0]
neutral_tweets = [tweet for index, tweet in enumerate(tweets['tweet']) if tweets['SA'][index]== 0]
negative_tweets = [tweet for index, tweet in enumerate(tweets['tweet']) if tweets['SA'][index]< 0]

print("Percentage of positive  tweets: {}%".format(len(positive_tweets)*100/len(tweets['tweet'])))
print("Percentage of neutral  tweets: {}%".format(len(neutral_tweets)*100/len(tweets['tweet'])))
print("Percentage de negative  tweets: {}%".format(len(negative_tweets)*100/len(tweets['tweet'])))



#Before I can create a pie chart I need to make the lists a dataframe

pos = len(positive_tweets)*100/len(tweets['tweet'])
neg = len(negative_tweets)*100/len(tweets['tweet'])
neu = len(neutral_tweets)*100/len(tweets['tweet'])
#create a piechart of the tweets



slices = [ pos, neg, neu]
Sentiment = ['Positive Tweets', 'Negative Tweets', 'Neutral Tweets']
cols = ['green', 'red' , 'grey']



plt.pie(slices, labels = Sentiment, colors = cols, startangle =90, shadow = True, explode=(0.1, 0, 0), autopct ='%1.1f%%')
plt.title("Sentiment of Tweets Containing Terms XXXXXXXXX")
plt.show


#save file

writer = pd.ExcelWriter('analyze.xlsx', engine ='xlsxwriter')
tweets.to_excel(writer, sheet_name='Sheet1')
writer.save()



#save the file 
import csv
with open('analysis.csv', 'w' , newline='') as f:
    fieldnames =['id', 'tweet', 'SA']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerow({'id': :, 'tweet' : :, 'SA' : :})



