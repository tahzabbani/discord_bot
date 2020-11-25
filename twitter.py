import config
import tweepy

# Setup access to API
def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_TOKEN, config.TWITTER_SECRET)

    api = tweepy.API(auth)
    return api

def trump():
    # Create API object
    api = connect_to_twitter_OAuth()

    trump_array = []

    public_tweets = api.user_timeline(screen_name='@realDonaldTrump')
    for tweet in public_tweets:
        trump_array.append(tweet.text)
    
    # return("\n".join(trump_array))

    return(trump_array[0])