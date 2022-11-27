
from kafka import KafkaConsumer
import pandas as pd
import os, json
import ast
# from cassandrautils import saveWeatherreport

if __name__ == "__main__":
    print("Starting Faker Consumer")
    TOPIC_NAME = os.environ.get("TOPIC_NAME", "faker")
    KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")
    CASSANDRA_HOST = os.environ.get("CASSANDRA_HOST", "localhost")
    CASSANDRA_KEYSPACE = os.environ.get("CASSANDRA_KEYSPACE", "kafkapipeline")

    print("Setting up Kafka consumer at {}".format(KAFKA_BROKER_URL))
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_BROKER_URL])
    
    print('Waiting for msg...')
    for msg in consumer:
        msg = msg.value.decode('ascii')
        jsonData=json.loads(msg)
        print(jsonData)
        
    print("Bye-Bye")