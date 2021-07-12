"""
Módulo com definições das interfaces e classes abstratas utilizadas no sistema de processamento.

A Interface Observer e Classe Abstrata Subject são utilizadas para seguir o padrão de modelagem Observer.
As Interfaces ConnectionDB e IdentificationAPI são utilizadas pelas classes concretas de Observers.
"""
from settings import LOGGING_CONF
import logging, logging.config

logging.config.fileConfig(fname=LOGGING_CONF)
logger = logging.getLogger(__name__)

class Observer():
    """Classe para representar a Interface Observer
    """
    def __init__(self):
        super().__init__()
        pass

    def update(self, message: object) -> None:
        logger.info("Message Received from Subject")
        raise Exception("NotImplementedException")


class Subject():
    """Classe Abstrata para representar o Subject
    """
    def __init__(self):
        super().__init__()
        logger.info("Starting Subject")
        self._observers = []
        self._state = None

    def add_observer(self, observer: Observer) -> None:
        try:
            logger.info("Adding Observer")
            self._observers.append(observer)
        except Exception as e:
            logger.error("Unable to add Observer ")
            logger.error(e)

    def remove_observer(self, observer: Observer) -> None:
        try:
            logger.info("Removing Observer")
            self._observers.remove(observer)
        except Exception as e:
            logger.error("Unable to remove Observer ")
            logger.error(e)

    def notify_all(self, message: object) -> None:
        logger.info("Notifying Observers")
        for observer in self._observers:
            try:
                observer.update(message)
            except Exception as e:
                logger.error("Unable to notify Observer %s" % observer)
                logger.error(e)
                raise
        if not self._observers:
            logger.info("No observers on the list")

class ConnectionDB():
    """Classe para representar a Interface Genérica para comunicação com banco de dados
    """
    def __init__(self):
        super().__init__()
        pass

    def read(self, filter: object) -> object:
        raise Exception("NotImplementedException")

    def create(self, obj: object) -> bool:
        raise Exception("NotImplementedException")

    def upgrade(self, obj: object) -> bool:
        raise Exception("NotImplementedException")

    def delete(self, obj: object) -> bool:
        raise Exception("NotImplementedException")

class IdentificationAPI():
    """Classe para representar a Interface Genérica para comunicação com uma API de identificação
    """
    def __init__(self):
        super().__init__()
        pass

    def request(self, image: bytes) -> str:
        raise Exception("NotImplementedException")