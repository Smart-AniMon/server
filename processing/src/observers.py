"""
Módulo com implementações das classes concretas que extendem a interface Observer.

Identifier - Classe para representar a comunicação com APIs de identificação.
Database - Classe para representar a comunicação com banco de dados.
"""

from .interfaces import  Subject, Observer, ConnectionDB, IdentificationAPI
from .clients import MQTTClient, MongoDBClient, CloudVisionClient
from .utils import str64_to_bytes, get_name, check_labels
from settings import DATABASE_COLLECTIONS as collections
from settings import (FULL_LABELS_SCORE, ANIMAL_LABELS, IDENTIFIED_LABELS_SCORE, 
                      LOGGING, RESOURCES)


import logging, logging.config
import json, io, os

logging.config.dictConfig(LOGGING)

class Identifier(Observer, Subject):
    """
    Classe para representar um Observer do Subject de Fila de Mensagem.
    Implementa a interface Observer e Utiliza a Interface IdentificationAPI para
    realizar uma consulta na API de identificação.
       
    Representa um Subject para o Observer DataCore e Observer Notification
    
    Implementa a interface Observer e precisa incluir a definição dos seguintes métodos:
            update(message: object, sub_name: str) -> None
    Extende a classe Subject e precisa chamar o método 
            notify_all(message: object) com a resposta da consulta.
    """

    def __init__(self, api_instance=None):
        super().__init__()
        self.logger = logging.getLogger(get_name(self))
        self.logger.info("Starting Observer/Subject Identifier")
        if not api_instance:
            self.identification_api = CloudVisionClient() # Client padrão quando não é informado no construtor
        else:
            self.identification_api = api_instance 

        self._image_content = "" # imagem em bytes sem estar codificada em base64
        self.name = 'Identifier'  # Nome identificador do Subject
        self._identified_labels = []

    @property
    def identification_api(self):
        return self._identification_api
    
    @identification_api.setter
    def identification_api(self, api):
        if isinstance(api, IdentificationAPI):
            self._identification_api = api
        else:
            self.logger.error("{} is not {} instance".format(api, IdentificationAPI))
            raise Exception('InstanceError')

    # Método da interface Observer
    def update(self, message: object, sub_name: str) -> None:  
        image_base64_str = message['image']
        #self.logger.debug("Image base64 String: %s" % image_base64_str)
        self._image_content = str64_to_bytes(image_base64_str)
        response_dict = None
        try:
            response = self._identification_api.request(self._image_content)
            response_dict = self._check_response(response)
            response_dict['_id'] = message['_id']
            self.logger.debug("message is {} object".format(type(response_dict)))
        except Exception as e:
            self.logger.error(e)
        
        self.notify_all(response_dict)
    
    def _check_response(self, response: str) -> dict:
        self.logger.info("Checking Animal labels")
        resp_dict = json.loads(response)
        labels = resp_dict['label_annotations']
        full_labels = []
        self._identified_labels.clear()
        for label in labels:
            tipo = label['description']
            score = float(label['score'])*100.0
            des_up = tipo.upper()
            if score >= FULL_LABELS_SCORE:
                if check_labels(des_up, ANIMAL_LABELS) and score >= IDENTIFIED_LABELS_SCORE: 
                    self._identified_labels.append(label)
                full_labels.append(label)
        self.logger.debug("identified_labels = {}".format(self._identified_labels))
        response_dict = dict()
        response_dict['labels'] = full_labels
        if self._identified_labels:
            response_dict['identified'] = True
        else:
            response_dict['identified'] = False
        response_dict['identified_labels'] = self._identified_labels

        self.logger.debug("full labels {}".format(full_labels))
        return response_dict

class DataCore(Observer):
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
        self.logger = logging.getLogger(get_name(self))
        self.logger.info("Starting Observer DataCore")
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
            self.logger.error("{} is not {} instance".format(db, ConnectionDB))
            raise Exception('InstanceError')

    # Método da interface Observer
    def update(self, message: dict, subject_name: str) -> None:
        self.logger.debug("message is {} object".format(type(message)))
        try:
            self.logger.debug("Subject: {}".format(subject_name))
            if subject_name == "MQTTClient":
                message = self._save_image(message)
            elif subject_name == "Identifier":
                message = self._catalog(message)
            self._message = message
            self._verify_subject(subject_name)
        except Exception as e:
            self.logger.error(e)

    def _verify_subject(self, name: str) -> None:
        collection = collections[name]
        if not collection:
            self.logger.error("Subject name {} not specified".format(name))
            raise Exception('NotSpecifiedError')
        try:
            self.connection_db.create(self._message, collection)
        except Exception as e:
            self.logger.error(e)
    
    def _save_image(self, message: dict) -> dict:
        image_base64_str = message['image']
        image_bytes = str64_to_bytes(image_base64_str)
        message_id = message['_id']
        file_name = "{}.jpg".format(message_id)

        if not os.path.exists(RESOURCES):
            os.makedirs(RESOURCES)

        path = "{}/{}".format(RESOURCES, file_name)
        self.logger.info("Saving image bytes in filesystem - {}".format(path))
        f = io.open(path, "wb")

        f.write(image_bytes)

        f.close()

        message['image'] = "resources/{}".format(file_name)

        return message
    
    def _catalog(self, message: dict) -> dict:
        collection = collections['Label']
        documents = self.connection_db.read({'active': True}, collection)
        documents_list = list(documents)
        classified_labels = []
        full_labels = []
        for document in documents_list:
            full_labels.append(document['labels'])
        message_labels = message['labels']
        for label in message_labels:
            tipo = label['description']
            des_up = tipo.upper()
            for labels in full_labels:
                if check_labels(des_up, labels): 
                    classified_labels.append(label)
        message['classified_labels'] = classified_labels
        if classified_labels:
            message['classified'] = True
        else:
            message['classified'] = False
        self.logger.debug("classified labels {}".format(classified_labels))
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
        self.logger = logging.getLogger(get_name(self))
        self.logger.info("Starting Observer Notification")
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
            self.logger.error("{} is not {} instance".format(db, ConnectionDB))
            raise Exception('InstanceError')

    # Método da interface Observer
    def update(self, message: dict, subject_name: str) -> None:
        self.logger.debug("message is {} object".format(type(message)))   
        self.logger.debug("Message: {}".format(message))
        self._message = message
        self._check_flags()      
    
    def _check_flags(self):
        collection_flags = collections['Flag']
        collection_notification = collections['Notification']
        documents_flags = self.connection_db.read({'active': True}, collection_flags)
        self.logger.debug("Document Flags size {}".format(documents_flags.count()))
        identified_flags = []
        notification = dict()
        if documents_flags:
            for flags in documents_flags:
                labels = flags['labels']           # lista
                self.logger.debug("Labels da Flag = {}".format(labels))
                notification.clear()
                identified_flags.clear()
                for label in self._message['labels']:
                    description = label['description'].upper()
                    self.logger.debug("Label Description {}".format(description))
                    if description in [x.upper() for x in labels]:
                        self.logger.info("Found Label {}".format(description))
                        identified_flags.append(label)
                if identified_flags:
                    notification['identified_flags'] = identified_flags
                    notification['animal_id'] = self._message['_id']
                    notification['flags'] = flags
                    notification['read'] = False
                    self.logger.info("Criando notificação = {}".format(notification))
                    try:
                        self.connection_db.create(notification, collection_notification)
                    except Exception as e:
                        self.logger.error(e)

