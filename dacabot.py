import tweepy
import boto3
from credentials import *
from awscredentials import*

def handler(event, context):
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )

    # load the text file within the s3 bucket
    s3 = session.resource('s3')
    obj = s3.Object('dacabot', 'tweets.txt')
    data = obj.get()['Body'].read().decode('UTF-8')

    # Access and authorize our Twitter credentials from credentials.py
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # query to filter out retweets and search by keyword
    query = 'daca -filter:retweets'
    max_tweets = 50

    # search and store new tweets
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=query, lang='en', count=count, max_id=str(last_id - 1))
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break

    # append every line of the s3 file to an array
    tweetsAlreadyRepliedTo = data.split()

    # initialize key words to search within tweets we want to reply to
    keywords_1 = ['education', 'uneducated', 'unemployed', 'employed', 'jobs', 'economy', 'lazy', 'ICE']
    keywords_2 = ['taxes', 'welfare', 'loans', 'aid', 'free', 'Americans']
    keywords_3 = ['illegal', 'crime', 'criminal', 'deport', 'illegals', 'aliens']

    # how many tweets we want to reply to each time the script is run
    tweet_limit = 0
    num = 1

    # initialize boto3 client in order to upload new text file of tweets
    client = boto3.client('s3',
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY,
                          region_name='us-west-1'
                          )

    # only two tweets may be sent when script runs
    # iterates through 50 searched tweets and checks if it should reply to one of them or not
    while num < 50 and tweet_limit < 2:
        tweetToCheck = searched_tweets[num]
        # executes only if tweet has not been replied to and the tweet isn't my own tweet
        if str(tweetToCheck.id) not in tweetsAlreadyRepliedTo and tweetToCheck.user.screen_name != 'thedacabot':
            if any(keyword in api.get_status(tweetToCheck.id, tweet_mode='extended')._json['full_text'] for keyword in keywords_1):
                compose = ' message to tweet'
                try:
                    api.update_status('@' + tweetToCheck.user.screen_name + compose, tweetToCheck.id)
                    file = ''
                    for x in tweetsAlreadyRepliedTo:
                        file += x + ' '
                    file += str(tweetToCheck.id)
                    client.put_object(Bucket='dacabot', Body=file.encode('utf-8'),
                                      Key='tweets.txt')
                    tweet_limit += 1
                except tweepy.TweepError as error:
                    if error.api_code == 187:
                        # Do something special
                        print('duplicate message')
                    else:
                        print(error.api_code)

            elif any(keyword in api.get_status(tweetToCheck.id, tweet_mode='extended')._json['full_text'] for keyword in keywords_2):
                compose = ' message to tweet'
                try:
                    api.update_status('@' + tweetToCheck.user.screen_name + compose, tweetToCheck.id)
                    file = ''
                    for x in tweetsAlreadyRepliedTo:
                        file += x + ' '
                    file += str(tweetToCheck.id)
                    client.put_object(Bucket='dacabot', Body=file.encode('utf-8'),
                                      Key='tweets.txt')
                    tweet_limit += 1
                except tweepy.TweepError as error:
                    if error.api_code == 187:
                        # Do something special
                        print('duplicate message')
                    else:
                        print(error.api_code)

            elif any(keyword in api.get_status(tweetToCheck.id, tweet_mode='extended')._json['full_text'] for keyword in keywords_3):
                compose = ' message to tweet'
                try:
                    api.update_status('@' + tweetToCheck.user.screen_name + compose, tweetToCheck.id)
                    file = ''
                    for x in tweetsAlreadyRepliedTo:
                        file += x + ' '
                    file += str(tweetToCheck.id)
                    client.put_object(Bucket='dacabot', Body=file.encode('utf-8'),
                                      Key='tweets.txt')
                    tweet_limit += 1
                except tweepy.TweepError as error:
                    if error.api_code == 187:
                        # Do something special
                        print('duplicate message')
                    else:
                        print(error.api_code)

        num += 1
