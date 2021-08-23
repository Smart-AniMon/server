
from src.clients import MQTTClient, CloudVisionClient, MongoDBClient
from src.observers import Identifier, DataCore

subject_consumer = MQTTClient()
observer_subject_api = Identifier()
observer_database = DataCore()

vision_client = CloudVisionClient()
observer_subject_api.identification_api = vision_client

subject_consumer.add_observer(observer_subject_api)
subject_consumer.add_observer(observer_database)
observer_subject_api.add_observer(observer_database)

subject_consumer.connect()