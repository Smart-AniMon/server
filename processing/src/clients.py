"""
Módulo com implementações das classes de clientes do Sistema.

CloudVisionClient - Classe para representar a comunicação com a API Vision do Google.
MongoClient - Classe para representar a comunicação com banco de dados MongoDB.
MQTTClietn - Classe para repreentar a comunicação com o broker MQTT
"""

# Internal python modules

from .interfaces import Subject, Observer, ConnectionDB, IdentificationAPI
from .utils import ReturnCodesMQTT, get_name
from settings import LOGGING, VISION_KEY_FILE, MQTT_BROKER, MONGO_CONNECT

# External python modules
from paho.mqtt import client as mqtt_client
from google.cloud import vision
from pymongo.mongo_client import MongoClient
from pymongo.errors import DuplicateKeyError

# Dafault python modules
import logging, logging.config
import io, os, base64, binascii, json, hashlib

# Logs
logging.config.dictConfig(LOGGING)

class CloudVisionClient(IdentificationAPI):
    """
    Classe que representa um Cliente para API Vision do Google.

    Implementa a interface IdentificationAPI e precisa incluir a definição dos seguintes métodos:
            request(image: bytes) -> response
    Extende a classe Thread para possibilitar multiplas consultas.
    """

    def __init__(self):
        self.logger = logging.getLogger(get_name(self))
        self.logger.info("Starting CloudVisionClient")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = VISION_KEY_FILE
        self._client = vision.ImageAnnotatorClient()

    # Método da interface IdentificationAPI
    def request(self, image_identify: bytes ) -> str:
        image = vision.Image(content=image_identify)

        # Performs label detection on the image file
        response = self._client.label_detection(image=image, max_results=50)
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        #response_json = vision.AnnotateImageResponse.to_json(response)
        
        labels = response.label_annotations
        self.logger.debug('{}'.format(labels))
        
        response_json = None
        response_dict = dict()
        labels_list = []
        try:
            for label in labels:
                labels_list.append(json.loads(vision.EntityAnnotation.to_json(label)))
            response_dict['label_annotations'] = labels_list
            response_json = json.dumps(response_dict)
        except Exception as e:
            self.logger.error('Não foi possível converter labels')
        
        self.logger.info('{}'.format(response_json))

        return response_json

class MongoDBClient(ConnectionDB):
    """
    Classe que representa um Cliente para o MongoDB.

    Implementa a interface ConnectionDB e precisa incluir a definição dos seguintes métodos:
        create(object) -> bool
        upgrade(object) -> bool
        delete(object) -> bool
        read(filter) -> Object
    """

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(get_name(self))
        self.logger.info("Starting MongoClient")
        self._host = MONGO_CONNECT['HOST']
        self._port = int(MONGO_CONNECT['PORT'])
        self._user = MONGO_CONNECT['USER']
        self._pass = MONGO_CONNECT['PASS']
        self._db_name = MONGO_CONNECT['DATABASE']

        self._connect()
        
    def _connect(self):
        self._client = MongoClient(host=self._host, port=self._port)
        self._database = self._client[self._db_name]
        self._database.authenticate(self._user, self._pass)
               
    # Método da interface ConnectionDB
    def create(self, obj: object, collect_name: str) -> bool:
        self.logger.info('Try insert message in {} collection'.format(collect_name))
        collection = self._database[collect_name]
        try:
            document_id = collection.insert_one(obj).inserted_id
            self.logger.info('Document _id = {}'.format(document_id))
        except DuplicateKeyError as e:
            self.logger.error("Can't create document , duplicate key error")
            raise
        except Exception as e:
            self.logger.error(e)           

    # Método da interface ConnectionDB
    def upgrade(self, obj: object, collect_name: str) -> bool:
        self.logger.info('Upgrade message in {} collection'.format(collect_name))
        collection = self._database[collect_name]
        try:
            document_id = collection.update_one({'_id': obj['_id']}, {'$set': obj})
        except Exception as e:
            self.logger.error("Can't update document")
            self.logger.error(e)  
            raise
    
    # Método da interface ConnectionDB
    def delete(self, obj: object, collect_name: str) -> bool:
        pass
        #TODO

    # Método da interface ConnectionDB
    def read(self, filter: object, collect_name: str, just_one=False) -> object:
        self.logger.info('Read document at {} collection with filter {}'.format(collect_name, filter))
        collection = self._database[collect_name]
        if filter is None:
            if just_one:
                result = collection.find_one()
            else:
                result = collection.find()
        else:
            if just_one:
                result = collection.find_one(filter)
            else:
                result = collection.find(filter)
        self.logger.info('Retrieved {}'.format(result))
        return result
  
class MQTTClient(Subject):
    """
    Classe que representa um Client MQTT para consumir as mensagens de um tópico.
    Foi utilizado a implementação de Client Subscribe da biblioteca paho.

    Extende a Classe abstrata com métodos para padrão Observer.
    """

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(get_name(self))
        self.logger.debug("Starting MQTTClient")
        self.name = 'MQTTClient'
        self._host = MQTT_BROKER['HOST']
        self._port = int(MQTT_BROKER['PORT'])
        self._user = MQTT_BROKER['USER']
        self._pass = MQTT_BROKER['PASS']
        self._topic = MQTT_BROKER['TOPIC']
        self._client_name = MQTT_BROKER['CLIENT_NAME']
        self._consumer =  mqtt_client.Client(self._client_name)

    def connect(self):
        self.logger.info("connecting to broker {} on port {}".format(self._host, self._port))
        #self.logger.debug("credentials {} - {}".format(self._user, self._pass))
        self._consumer.username_pw_set(self._user, self._pass)
        self._consumer.on_connect = self._connect_callback
        self._consumer.on_message = self._message_callback
        try:
            self._consumer.connect(self._host, self._port)
        except ConnectionRefusedError:
            self.logger.error("Não foi possível estabelecer conexão com Broker. Verifique parâmetros em settings.py")
        except Exception as e:
            self.logger.error(e)
            raise
        else:
            try:
                self.logger.info("Starting ClientMQTT")
                self._consumer.loop_forever()
            except KeyboardInterrupt:
                self.logger.error("Exit")
            except Exception as e:
                self.logger.error(e)
                raise 

    def _connect_callback(self, client, userdata, flags, rc):
        self.logger.debug("client = %s" % client)
        self.logger.debug("userdate = %s" % userdata)
        self.logger.debug("flags = %s" % flags)
        self.logger.debug("rc = %s" % rc)
        message_rc = ReturnCodesMQTT.get_message(rc)
        if rc == 0:
            self.logger.info("connected to broker")
            self.logger.info("Subscribe in topic %s" % self._topic)
            client.subscribe(self._topic)
            self.logger.info("waiting for messages")
        else:
            self.logger.warn("%s" % message_rc)

    def _message_callback(self, client, userdata, msg):
        
        payload_json = msg.payload.decode()

        self.logger.debug("client = %s" % client)
        self.logger.debug("userdate = %s" % userdata)
        self.logger.debug("msg = %s" % payload_json)
        self.logger.info("Message received from broker")

        msg_dict = json.loads(payload_json)  # create message dict
        self.logger.debug("message is a {} object".format(type(msg_dict)))
        message = self._create_id(msg_dict)
        self.notify_all(message)
    
    def _create_id(self, message: dict) -> dict:
        text_hash = '{}{}'.format(message['id'], message['capture_date'])
        self.logger.info("Text Hash = {}".format(text_hash))
        _id = hashlib.md5(text_hash.encode('utf-8')).hexdigest()
        self.logger.info("_id = {}".format(_id))
        message['_id'] = _id
        return message





        
