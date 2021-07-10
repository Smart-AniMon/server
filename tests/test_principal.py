
from processing.mqtt import MQTTClient
from processing.observers import CloudVisionClient, MongoClient

consumer_test = MQTTClient()
apivision_observer = CloudVisionClient()
mongoclient_observer = MongoClient()
consumer_test.add_observer(apivision_observer)
consumer_test.add_observer(mongoclient_observer)
consumer_test.connect()