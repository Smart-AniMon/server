from processing.observers import CloudVisionClient
import io, os, base64

image = os.path.abspath('tests/wakeupcat.jpg')

# Loads the image into memory
with io.open(image, 'rb') as image_file:
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes)

apivision_observer = CloudVisionClient()
apivision_observer.request(image_base64)