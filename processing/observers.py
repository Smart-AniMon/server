"""
Módulo com implementações das classes que extendem a interface Observer.

CloudVisionClient - Classe para representar a comunicação com a API Vision do Google
MongoClient - Classe para repreesntar a comunicação com o MongoDB
"""

from .interfaces import Observer, ConnectionDB
from settings import LOGGING_CONF, VISION_KEY_FILE
from google.cloud import vision


import logging, logging.config
import io, os, base64, binascii

logging.config.fileConfig(fname=LOGGING_CONF)
logger = logging.getLogger(__name__)

class CloudVisionClient(Observer):
    """Classe que representa um Cliente para API Vision do Google.

    Args:
        Observer : Implementa a interface Observer e precisa incluir a definição dos seguintes métodos:
                   update(message: object) -> None
    """

    def __init__(self):
        logger.info("Starting observer CloudVisionClient")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = VISION_KEY_FILE
        self.__client = vision.ImageAnnotatorClient()
        self.__image_content = "" # imagem em bytes sem estar codificada em base64


    # Método da interface
    def update(self, message: object) -> None:
        logger.info("Message Received from Subject")
        logger.debug("Message Dict: %s" % message)
       
        base64 = message['image'].encode('utf-8')        # string to bytes code base64
        self.request(base64)       

    def request(self, image_base64: bytes ) -> str:
        self.__image_content =  binascii.a2b_base64(image_base64) # decode base64
        image = vision.Image(content=self.__image_content)

        # Performs label detection on the image file
        response = self.__client.label_detection(image=image)
        logger.debug("Response: \n %s" % response)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        labels = response.label_annotations

        logger.info("Possible identification")
        logger.debug("%s" % labels)

        return response




        
