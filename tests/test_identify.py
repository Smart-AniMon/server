from processing.observers import Identifier
from processing.clients import CloudVisionClient

import io, os, base64, json

image = os.path.abspath('tests/wakeupcat.jpg')

# Loads the image into memory
with io.open(image, 'rb') as image_file:
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes)

payload = {
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

payload_json = json.dumps(payload)
message = json.loads(payload_json)

observer_subject_api = Identifier()
vision_client = CloudVisionClient()
observer_subject_api.identification_api = vision_client

observer_subject_api.update(message)