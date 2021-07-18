from src.observers import Database

import io, os, base64, json

image = os.path.abspath('tests/wakeupcat.jpg')

# Loads the image into memory
with io.open(image, 'rb') as image_file:
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes)

payload = {
   'id':'module2',
   'image': 'dsdsadsasadsasa',
   'temperature':30.0,
   'humidity':80.0,
   'localization':{
      'latitude':'String',
      'longitude':'String'
   },
   'capture_date':'291029'
}

payload_json = json.dumps(payload)
message = json.loads(payload_json)

observer_db = Database()
observer_db.update(message, 'MQTTClient')
