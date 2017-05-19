
# coding: utf-8

# In[2]:

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from matplotlib import pyplot as plt
import numpy as np
from numpy  import array
import seaborn as sns
get_ipython().magic('matplotlib inline')


# In[18]:

class TwitterClient(object):
    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'ahCowaVjdVvO5lmJGMpigchRR'
        consumer_secret = 'o7dy5avGMI5AJutFPWjYHAeTAw5kVR8YBMt00OKXKvnUzBUvak'
        access_token = '630413671-toB4t1du9TkC3NVwfdxFzZpZKJ6kDqiIGcBIG2Bx'
        access_token_secret = 'fnTfmLeB1uiEheUPUHCEcFchcylJbBxLmvQHdrFF5wZl7'
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        #remove links and special characters from the text using regex
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        #classifying sentment of passed tweets using textblobs sentiment method
        #Utility function to classify sentiment of passed tweet
        
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        
    def get_tweet_sentiment_value(self, tweet):

        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # return sentiment value
        return analysis.sentiment.polarity
 
    def get_tweets(self, query, count = 1000):
        # tweets to getch tweets and parse them

        # empty list to store parsed tweets and tweet values
        tweets = []
        tweet_value = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
 
            #if query['user']['lang'] == 'en':
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                if (tweet.metadata['iso_language_code'] == 'en'):               
                    # saving text of tweet
                    parsed_tweet['text'] = tweet.text
                    # saving sentiment of tweet
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                    # appending parsed tweet to tweets list
                    if tweet.retweet_count > 0:
                        # if tweet has retweets, ensure that it is appended only once
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                            #tweet_value.append(self.get_tweet_sentiment_value(tweet.text))
                    else:
                        tweets.append(parsed_tweet)
                        #tweet_value.append(self.get_tweet_sentiment_value(tweet.text))
 
                tweet_value.append(self.get_tweet_sentiment_value(tweet.text))
            # return parsed tweets
            return tweets, tweet_value
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
 
def main(name):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets, tweet_value = api.get_tweets(query = name, count = 100)

    #print(tweets['text'])
    file1 = open("data1.txt","w")
    
    #print(len(tweet_value))
        
    x = np.arange(0,len(tweet_value),1)
    y = np.asarray(tweet_value)
    
    plt.plot(x,y)
    plt.ylim(-1,1)
    plt.ylabel('Sentiment value')
    plt.xlabel('Tweet Count')
    plt.title('Twitter sentiment analysis for ' + name)
    plt.show()
    
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    
    tot_tweets = [tweet for tweet in tweets]
    for tweet in tot_tweets[:]:
        file1.write("--" + tweet['text'].lower() + "\n\n") 
            
    # percentage tweets split
    if len(tweets) == 0:
        neg = 0
        pos = 0
    else:
        neg = 100*len(ntweets)/len(tweets)
        pos = 100*len(ptweets)/len(tweets)
    neut = 100 - pos - neg
    
    print("\t-->",round(pos,2),"% positive,", round(neg,2), "% negative,", round(neut,2),"% neutral tweets.")
    #print("Negative tweets percentage:",round(neg,2),"%")
    #print("Neutral tweets percentage:",round(neut,2),"%")

    print("\n\t--> Total sentiment value for ", name, " is ", round(y.sum(),2))
    
    file1.close()
    
    import re
    from collections import Counter # to generate the frequent items list

    file_ss = open("data1.txt","r")
    file_stop = open("stopwords1.txt","r")

    file1 = open("test1.txt","w")
    file2 = open("test2.txt","w")
    file3 = open("test3.txt","w")

    file1.write(str(re.sub('[^a-zA-Z]', ' ', file_ss.read().lower()))) 
    file2.write(str(re.sub('[^a-zA-Z]', ' ', file_stop.read().lower())))

    #replacing the special characters with space and converting the words to lower case as they are not case sensitive

    file_ss.close()
    file_stop.close()

    file1.close()
    file2.close()

    # closing all the open files to save memory

    stop_words = []

    file2 = open("test2.txt","r")

    for line1 in file2:
        for word1 in line1.split():
            stop_words.extend([word1]) # getting all the words from stopwords1.txt to list

    stop_words.extend([name.lower()])
    
    file1 = open("test1.txt","r")

    for line in file1:
        for word in line.split():
            if word not in stop_words:
                file3.write(word + " ") 

    file3.close()

    words = re.findall(r'\w+', open('test3.txt').read().lower()) # reading all the words from file and storing in list
    output = Counter(words).most_common(20) # finding the most frequent items using counter


    print("\n\tFrequently used words")
    i = 0 # for the ranking of the word
    for key, value in output:
        i += 1
        print("\n\t" + str(i) + ": " + key + " (" + str(value) + " times)" + "\t\t", end=" ") 
        # printing the text with the iteration number, word and number of occurances

        #for x in range (0,int(value/10),1):
        #    print("*", end=" ")
        # print the histogram using the symbol '*'

    file1.close()
    file2.close()
    file3.close()

    # close all files in case if open
    file1.close()

    from os import path
    from wordcloud import WordCloud

    d = path.dirname('__file__')

    # Read the whole text.
    text = open(path.join(d, 'test3.txt')).read()

    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    # the matplotlib way:
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # lower max_font_size
    #wordcloud = WordCloud(max_font_size=40).generate(text)
    #plt.figure()
    #plt.imshow(wordcloud, interpolation="bilinear")
    #plt.axis("off")
    plt.show()

    # The pil way (if you don't have matplotlib)
    # image = wordcloud.to_image()
    # image.show()
    print("\n--------------------------------------------------------------------------")
    
if __name__ == "__main__":
    main("Trump")
    main("Modi")
    main("Hillary")
    main("Obama")


# In[ ]:



