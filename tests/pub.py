# This is the Publisher Example

import paho.mqtt.publish as publish
from settings import MQTT_BROKER
import json
import io, os, base64

USER = MQTT_BROKER['USER']
PASS = MQTT_BROKER['PASS']
HOST = MQTT_BROKER['HOST']
PORT = MQTT_BROKER['PORT']
TOPIC = MQTT_BROKER['TOPIC']


image = os.path.abspath('tests/wakeupcat.jpg')

# Loads the image into memory
with io.open(image, 'rb') as image_file:
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes)

message = {
   "id":"module1",
   "image": image_base64.decode('utf-8'),
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
publish.single(TOPIC, payload=payload_json, hostname=HOST, port=PORT, auth=credentials)