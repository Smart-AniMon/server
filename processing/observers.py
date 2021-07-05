"""
Módulo com implementações das classes que extendem a interface Observer.

CloudVisionClient - Classe para representar a comunicação com a API Vision do Google
MongoClient - Classe para repreesntar a comunicação com o MongoDB
"""

from .interfaces import Observer, ConnectionDB
from settings import LOGGING_CONF

import logging, logging.config

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
        pass  # TODO

    # Método da interface
    def update(self, message: object) -> None:
        logger.info("Received Message from Subject: %s" % message)
        # TODO Implementar
