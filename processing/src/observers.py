"""
Módulo com implementações das classes concretas que extendem a interface Observer.

Identifier - Classe para representar a comunicação com APIs de identificação.
Database - Classe para representar a comunicação com banco de dados.
"""

from .interfaces import  Subject, Observer, ConnectionDB, IdentificationAPI
from .clients import MQTTClient, MongoDBClient, CloudVisionClient
from .utils import str64_to_bytes
from settings import LOGGING_CONF, RESOURCES
from settings import DATABASE_COLLECTIONS as collections


import logging, logging.config
import json, io

logging.config.fileConfig(fname=LOGGING_CONF)
logger = logging.getLogger(__name__)

class Identifier(Observer, Subject):
    """
    Classe para representar um Observer do Subject de Fila de Mensagem.
    Implementa a interface Observer e Utiliza a Interface IdentificationAPI para
    realizar uma consulta na API de identificação.
       
    Também representa um Subject para o Observer Database para que o resultado
    da API de identificação seja armazenada no banco de dados.

    
    Implementa a interface Observer e precisa incluir a definição dos seguintes métodos:
            update(message: object, sub_name: str) -> None
    Extende a classe Subject e precisa chamar o método 
            notify_all(message: object) com a resposta da consulta.
    """

    def __init__(self, api_instance=None):
        super().__init__()
        logger.info("Starting Observer/Subject Identifier")
        if not api_instance:
            self.identification_api = CloudVisionClient() # Client padrão quando não é informado no construtor
        else:
            self.identification_api = api_instance 

        self._image_content = "" # imagem em bytes sem estar codificada em base64
        self.name = 'Identifier'  # Nome identificador do Subject

    @property
    def identification_api(self):
        return self._identification_api
    
    @identification_api.setter
    def identification_api(self, api):
        if isinstance(api, IdentificationAPI):
            self._identification_api = api
        else:
            logger.error("{} is not {} instance".format(api, IdentificationAPI))
            raise Exception('InstanceError')

    # Método da interface Observer
    def update(self, message: object, sub_name: str) -> None:  
        image_base64_str = message['image']
        logger.debug("Image base64 String: %s" % image_base64_str)
        self._image_content = str64_to_bytes(image_base64_str)
        try:
            response = self._identification_api.request(self._image_content)
            response_dict = json.loads(response)
            response_dict['_id'] = message['_id']
            logger.debug("message is {} object".format(type(response_dict)))
            self.notify_all(response_dict)
        except Exception as e:
            logger.error(e)
            raise      

class Database(Observer):
    """
    Classe para representar um Observer do Subject de Fila de Mensagem e 
       do Subject da API de Identificação. 
       Implementa a interface Observer e Utiliza a Interface ConnectionDB para
       realizar comunicação com um banco de dados.

    
    Implementa a interface Observer e precisa incluir a definição dos seguintes métodos:
        update(message: object) -> None
    """

    def __init__(self, db_instance=None):
        super().__init__()
        logger.info("Starting Observer Database")
        if not db_instance:
            self.connection_db = MongoDBClient() # Client padrão quando não é informado no construtor
        else:
            self.connection_db = db_instance

        self._message = ""    # Objeto a ser adicionado ao banco

    @property
    def connection_db(self):
        return self._connection_db
    
    @connection_db.setter
    def connection_db(self, db):
        if isinstance(db, ConnectionDB):
            self._connection_db = db
        else:
            logger.error("{} is not {} instance".format(db, ConnectionDB))
            raise Exception('InstanceError')

    # Método da interface Observer
    def update(self, message: dict, subject_name: str) -> None:
        logger.debug("message is {} object".format(type(message)))   
        logger.debug("Message: {}".format(message))
        if subject_name == "MQTTClient":
            message = self._save_image(message)
        self._message = message
        self._verify_subject(subject_name)

    def _verify_subject(self, name: str) -> None:
        collection = collections[name]
        if not collection:
            logger.error("Subject name {} not specified".format(name))
            raise Exception('NotSpecifiedError')
        try:
            self.connection_db.create(self._message, collection)
        except Exception as e:
            logger.error(e)
    
    def _save_image(self, message: dict) -> dict:
        image_base64_str = message['image']
        image_bytes = str64_to_bytes(image_base64_str)
        message_id = message['_id']
        file_name = "{}.jpg".format(message_id)


        path = "{}/{}".format(RESOURCES, file_name)
        logger.info("Saving image bytes in filesystem - {}".format(path))
        f = io.open(path, "wb")

        f.write(image_bytes)

        f.close()

        message['image'] = "resources/{}".format(file_name)

        return message

class Notification(Observer):
    """
    Classe para representar um Observer do Subject da API de Identificação com 
       o objetivo de gravar no banco notificações de identificações com flags (labels) especificadas via Webapp.
       
    Implementa a interface Observer e Utiliza a Interface ConnectionDB para
       realizar comunicação com um banco de dados.

    
    Implementa a interface Observer e precisa incluir a definição dos seguintes métodos:
        update(message: object) -> None
    """

    def __init__(self, db_instance=None):
        super().__init__()
        logger.info("Starting Observer Notification")
        if not db_instance:
            self.connection_db = MongoDBClient() # Client padrão quando não é informado no construtor
        else:
            self.connection_db = db_instance

        self._message = ""    # Objeto a ser adicionado ao banco

    @property
    def connection_db(self):
        return self._connection_db
    
    @connection_db.setter
    def connection_db(self, db):
        if isinstance(db, ConnectionDB):
            self._connection_db = db
        else:
            logger.error("{} is not {} instance".format(db, ConnectionDB))
            raise Exception('InstanceError')

    # Método da interface Observer
    def update(self, message: dict, subject_name: str) -> None:
        logger.debug("message is {} object".format(type(message)))   
        logger.debug("Message: {}".format(message))
        self._message = message
        self._check_flags()      
    
    def _check_flags(self):
        collection_flags = collections['Flag']
        documents_flags = self.connection_db.read('', collection_flags)
        logger.debug("Document Flags {}".format(documents_flags))
        identified_flags = []
        notification = dict()
        if documents_flags:
            for flags in documents_flags:
                labels = flags['labels']           # lista
                notification.clear()
                identified_flags.clear()
                for label in self._message['labels']:
                    description = label['description'].upper()
                    if description in labels:
                        identified_flags.append(label)
                if identified_flags:
                    notification['identified_flags'] = identified_flags
                    notification['animal_id'] = self._message['_id']
                    notification['flags'] = flags['_id']
                try:
                    self.connection_db.create(notification, collections['Notification'])
                except Exception as e:
                    logger.error(e)

