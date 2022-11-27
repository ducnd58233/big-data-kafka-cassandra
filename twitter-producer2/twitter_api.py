import json
import os
from datetime import datetime
import tweepy
from kafka import KafkaProducer
import configparser

TWIITER_API_GEOBOX_FILTER = [-123.371556, 49.009125, -122.264683, 49.375294]
TWITTER_API_LANGS_FILTER = ['en']

# Twitter API Keys
config = configparser.ConfigParser()
config.read('twitter_service.cfg')
api_credential = config['twitter_api_credential']
access_tkn = api_credential['access_token']
access_tkn_secret = api_credential['access_token_secret']
consumer_key = api_credential['consumer_key']
consumer_secret = api_credential['consumer_secret']
bearer_tkn = api_credential['bearer_token']


# Kafka settings
KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL") if os.environ.get(
    "KAFKA_BROKER_URL") else 'localhost:9092'
TOPIC_NAME = os.environ.get("TOPIC_NAME") if os.environ.get(
    "TOPIC_NAME") else 'twitter2'

# a static location is used for now as a
# geolocation filter is imposed on twitter API
# TWEET_LOCATION = 'MetroVancouver'
TWEET_LOCATION = ['GB', 'SG']

client = tweepy.Client(
    bearer_token=bearer_tkn, 
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_tkn, 
    access_token_secret=access_tkn_secret,
    return_type=dict
)

# auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_tkn, access_tkn_secret)
# api = tweepy.API(auth)

class stream_listener(tweepy.StreamingClient):
    def __init__(self, bearer_tkn):
        print("Setting up Twitter API 2.0 producer at {}".format(KAFKA_BROKER_URL))
        super(stream_listener, self).__init__(bearer_token=bearer_tkn)
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            value_serializer=lambda x: json.dumps(x).encode('utf8')
        )
          
    def on_connect(self):
       
        print("Connected")
    
    def on_data(self, raw_data):
        json_data = json.loads(raw_data)
        data = json_data['data']
        includes = json_data['includes']
        
        if ('referenced_tweets' not in data) and ('places' in includes): # original tweet not replies tweet
            places = includes['places'][0]
            twitter_df = {
                'tweet': data['text'],
                'datetime': datetime.utcnow().timestamp(),
                'location': places['country']
            }
            
            print('-----------------------------------------------')
            print(data['text'])
            self.producer.send(TOPIC_NAME, value=twitter_df)
            self.producer.flush()
        return True
        
    def on_errors(errors):
        print(f'Streaming Error: {errors}')
        
    def disconnect():
        print('Disconnect')

class twitter_stream():
    def __init__(self):
        # self.auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_tkn, access_tkn_secret)
        # self.api = tweepy.API(self.auth)
        self.stream_listener = stream_listener(bearer_tkn)
        
    def twitter_listener(self):
        stream = self.stream_listener
        # stream.filter(locations=TWIITER_API_GEOBOX_FILTER,
        #               languages=TWITTER_API_LANGS_FILTER)

        for location in TWEET_LOCATION:
            stream.add_rules(tweepy.StreamRule(f'place_country:{location}'))
        for lang in TWITTER_API_LANGS_FILTER:
            stream.add_rules(tweepy.StreamRule(f'lang:{lang}'))
        
        stream.filter(
            tweet_fields = ['referenced_tweets', 'lang'], 
            user_fields = ['name','username','location'],
            expansions = ['geo.place_id', 'author_id'],
            place_fields = ['country','country_code']
        )

        
if __name__ == '__main__':
    ts = twitter_stream()
    ts.twitter_listener()
    
   