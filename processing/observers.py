"""
Módulo com implementações das classes concretas que extendem a interface Observer.

Identifier - Classe para representar a comunicação com APIs de identificação.
Database - Classe para representar a comunicação com banco de dados.
"""

from .interfaces import  Subject, Observer, ConnectionDB, IdentificationAPI
from settings import LOGGING_CONF


import logging, logging.config
import binascii, json

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
            update(message: object) -> None
    Extende a classe Subject e precisa chamar o método 
            notify_all(message: object) com a resposta da consulta.
    """

    def __init__(self):
        logger.info("Starting Observer/Subject Identify")
        self.identification_api = IdentificationAPI() # Interface
        self._image_content = "" # imagem em bytes sem estar codificada em base64
        super().__init__()

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
    def update(self, message: object) -> None:     
        image_base64_str = message['image']
        logger.debug("Image base64 String: %s" % image_base64_str)
        self._decode(image_base64_str)
        try:
            response = self._identification_api.request(self._image_content)
            message = json.loads(response)
            logger.debug("message is {} object".format(type(message)))
            self.notify_all(message)
        except Exception as e:
            logger.error(e)
            raise
    
    def _decode(self, image_base64: str):
        image_base64_bytes = image_base64.encode('utf-8')    # string to bytes code base64
        self._image_content = binascii.a2b_base64(image_base64_bytes) # decode base64           

class Database(Observer):
    """
    Classe para representar um Observer do Subject de Fila de Mensagem e 
       do Subject da API de Identificação. 
       Implementa a interface Observer e Utiliza a Interface ConnectionDB para
       realizar comunicação com um banco de dados.

    
    Implementa a interface Observer e precisa incluir a definição dos seguintes métodos:
        update(message: object) -> None
    """

    def __init__(self):
        pass

    # Método da interface Observer
    def update(self, message: object) -> None: 
        logger.debug("message is {} object".format(type(message)))   
        logger.debug("Message: {}".format(message))
        logger.info("TODO - Database")  
  


        
