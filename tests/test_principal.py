
from processing.mqtt import MQTTClient
from processing.observers import CloudVisionClient

consumer_test = MQTTClient()
apivision_observer = CloudVisionClient()
consumer_test.add_observer(apivision_observer)
consumer_test.connect()