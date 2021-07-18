import io, os

image = os.path.abspath('tests/wakeupcat.jpg')

# Loads the image into memory
with io.open(image, 'rb') as image_file:
    image_bytes = image_file.read()

f = io.open("teste.jpg", "wb")

f.write(image_bytes)

f.close()