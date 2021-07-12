"""
Módulo com implementações das classes de clientes do Sistema.

CloudVisionClient - Classe para representar a comunicação com a API Vision do Google.
MongoClient - Classe para representar a comunicação com banco de dados MongoDB.
MQTTClietn - Classe para repreentar a comunicação com o broker MQTT
"""

from .interfaces import Subject, Observer, ConnectionDB, IdentificationAPI
from .utils import ReturnCodesMQTT
from settings import LOGGING_CONF, VISION_KEY_FILE, MQTT_BROKER, MONGO_CONNECT

# bibliotecas extenas
from paho.mqtt import client as mqtt_client
from google.cloud import vision
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus

# bibliotecas default python
from threading import Thread
import logging, logging.config
import io, os, base64, binascii, json

# Logs
logging.config.fileConfig(fname=LOGGING_CONF)
logger = logging.getLogger(__name__)

class CloudVisionClient(IdentificationAPI, Thread):
    """
    Classe que representa um Cliente para API Vision do Google.

    Implementa a interface IdentificationAPI e precisa incluir a definição dos seguintes métodos:
            request(image: bytes) -> response
    Extende a classe Thread para possibilitar multiplas consultas.
    """

    def __init__(self):
        logger.info("Starting CloudVisionClient")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = VISION_KEY_FILE
        self._client = vision.ImageAnnotatorClient() 

    # Método da interface IdentificationAPI
    def request(self, image_identify: bytes ) -> str:
        image = vision.Image(content=image_identify)

        # Performs label detection on the image file
        response = self._client.label_detection(image=image, max_results=100)
        logger.debug("Response: \n %s" % response)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        labels = response.label_annotations
        logger.info('Possible identification')
        logger.info('{}'.format(labels))

        animal = False
        score = 0.0
        tipo = ""
        for label in labels:
            description = label.description.upper()
            if "ANIMAL" in description:
                animal = True
                tipo = description
                score = float(label.score)*100.0
            if "ANIMAL" == tipo:
                break
        
        if animal:       
            logger.info("Encontrou label {} com {:.2f}%".format(tipo, score))
        else:
            logger.info("Label animal não encontrada")

        response_json = vision.AnnotateImageResponse.to_json(response)

        return response_json

class MongoClientObserver(Observer, ConnectionDB):
    """Classe que representa um Cliente para o MongoDB.

    Implementa a interface Observer e precisa incluir a definição dos seguintes métodos:
        update(message: object) -> None
    Implementa a interface ConnectionDB e precisa incluir a definição dos seguintes métodos:
        create(object) -> bool
        upgrade(object) -> bool
        delete(object) -> bool
        read(filter) -> Object
    """

    def __init__(self):
        super().__init__()
        logger.info("Starting MongoClient")
        self._host = MONGO_CONNECT['HOST']
        self._port = MONGO_CONNECT['PORT']
        self._user = MONGO_CONNECT['USER']
        self._pass = MONGO_CONNECT['PASS']
        self._db_name = MONGO_CONNECT['DATABASE']
        self._client = MongoClient(host=self._host, port=self._port)
        self._database = self._client[self._db_name]
        self._database.authenticate(self._user, self._pass)
        
    #def _connect(self):

               
    # Método da interface ConnectionDB
    def create(self, obj: object, collect_name: str) -> bool:
        collection = self._database[collect_name]
        collection.insert_one(obj)

    # Método da interface ConnectionDB
    def upgrade(self, obj: object, collect_name: str) -> bool:
        pass
        #TODO
    
    # Método da interface ConnectionDB
    def delete(self, obj: object, collect_name: str) -> bool:
        pass
        #TODO

    # Método da interface ConnectionDB
    def read(self, filter: object, collect_name: str) -> object:
        pass
        #TODO

    # Método da interface Observer
    def update(self, message: object) -> None:     
        logger.info("(MongoClient) received")
        self.create(message, "teste-identification")
  
class MQTTClient(Subject):
    """Classe que representa um Client MQTT para consumir as mensagens de um tópico.
       foi construido utilizando a implementação de Client Subscribe da biblioteca paho.

    Args:
        Subject : Extende a Classe abstrata com métodos para padrão Observer.
    """

    def __init__(self):
        super().__init__()
        logger.debug("Starting MQTTClient")
        self._host = MQTT_BROKER['HOST']
        self._port = MQTT_BROKER['PORT']
        self._user = MQTT_BROKER['USER']
        self._pass = MQTT_BROKER['PASS']
        self._topic = MQTT_BROKER['TOPIC']
        self._client_name = MQTT_BROKER['CLIENT_NAME']
        self._consumer =  mqtt_client.Client(self._client_name)

    def connect(self):
        logger.info("connecting to broker {} on port {}".format(self._host, self._port))
        logger.debug("credentials {} - {}".format(self._user, self._pass))
        self._consumer.username_pw_set(self._user, self._pass)
        self._consumer.on_connect = self._connect_callback
        self._consumer.on_message = self._message_callback
        try:
            self._consumer.connect(self._host, self._port)
        except ConnectionRefusedError:
            logger.error("Não foi possível estabelecer conexão com Broker. Verifique parâmetros em settings.py")
        except Exception as e:
            logger.error(e)
            raise
        else:
            try:
                logger.info("Starting ClientMQTT")
                self._consumer.loop_forever()
            except KeyboardInterrupt:
                logger.error("Exit")
            except Exception as e:
                logger.error(e)
                raise 

    def _connect_callback(self, client, userdata, flags, rc):
        logger.debug("client = %s" % client)
        logger.debug("userdate = %s" % userdata)
        logger.debug("flags = %s" % flags)
        logger.debug("rc = %s" % rc)
        message_rc = ReturnCodesMQTT.get_message(rc)
        if rc == 0:
            logger.info("connected to broker")
            logger.info("Subscribe in topic %s" % self._topic)
            client.subscribe(self._topic)
            logger.info("waiting for messages")
        else:
            logger.warn("%s" % message_rc)

    def _message_callback(self, client, userdata, msg):
        
        payload_json = msg.payload.decode()

        logger.debug("client = %s" % client)
        logger.debug("userdate = %s" % userdata)
        logger.debug("msg = %s" % payload_json)
        logger.info("Message received from broker")

        message = json.loads(payload_json)  # create message dict
        logger.debug("message is a {} object".format(type(message)))
        self.notify_all(message)

        
