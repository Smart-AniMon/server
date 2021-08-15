# This is the Publisher Example

import paho.mqtt.publish as publish
import create_env
from settings import MQTT_BROKER
import json
import io, os, base64
import datetime



USER = MQTT_BROKER['USER']
PASS = MQTT_BROKER['PASS']
HOST = MQTT_BROKER['HOST']
PORT = int(MQTT_BROKER['PORT'])
TOPIC = MQTT_BROKER['TOPIC']

images = [
   'tests/zebra.jpeg',
   'tests/wakeupcat.jpg',
   'tests/l2.jpeg',
   'tests/l3.jpg',
   'tests/l.png',
   'tests/l5.jpg'
]

for img in images:
   image = os.path.abspath(img)

   # Loads the image into memory
   with io.open(image, 'rb') as image_file:
      image_bytes = image_file.read()
      image_base64 = base64.b64encode(image_bytes)

   datetime_object = datetime.datetime.now()
   message = {
      "id":"module1",
      "image": image_base64.decode('utf-8'),
      "temperature":30.0,
      "humidity":80.0,
      "localization":{
      "latitude":"String",
      "longitude":"String"
   },
   "capture_date":str(datetime_object)
   }
  
   payload_json = json.dumps(message)

   credentials = {'username': USER, 'password': PASS}
   publish.single(TOPIC, payload=payload_json, hostname=HOST, port=PORT, auth=credentials)