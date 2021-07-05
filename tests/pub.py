# This is the Publisher Example

import paho.mqtt.publish as publish
from settings import MQTT_BROKER
import json


USER = MQTT_BROKER['USER']
PASS = MQTT_BROKER['PASS']
HOST = MQTT_BROKER['HOST']
PORT = MQTT_BROKER['PORT']
TOPIC = MQTT_BROKER['TOPIC']



message = {
   "id":"module1",
   "image":"sdasdasdasdsadsadsad3esaa",
   "temperature":30.0,
   "humidity":80.0,
   "localization":{
      "latitude":"String",
      "longitude":"String"
   },
   "capture_date":"291029"
}
  
payload_json = json.dumps(message)

credentials = {'username': USER, 'password': PASS}
publish.single(TOPIC,payload=payload_json, hostname=HOST, port=PORT, auth=credentials)