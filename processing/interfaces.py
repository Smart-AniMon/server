"""
Módulo com definições das interfaces e classes abstratas utilizadas no sistema de processamento.

As Classes Observer e Subject são utilizadas para seguir o padrão de modelagem Observer.
"""
from settings import LOGGING_CONF
import logging, logging.config

#logging.config.fileConfig(fname=LOGGING_CONF)
logger = logging.getLogger(__name__)

class Observer(object):
    """Classe para representar a Interface Observer
    """
    def __init__(self):
        pass

    def update(self, message: object) -> None:
        logger.info("Message Received from Subject")
        raise Exception("NotImplementedException")


class Subject(object):
    """Classe para representar o Subject
    """
    def __init__(self):
        logger.info("Starting Subject")
        self.__observers = []
        self.__state = None

    def add_observer(self, observer: Observer) -> None:
        try:
            logger.info("Adding Observer")
            self.__observers.append(observer)
        except Exception as e:
            logger.error("Unable to add Observer ")
            logger.error(e)

    def remove_observer(self, observer: Observer) -> None:
        try:
            logger.info("Removing Observer")
            self.__observers.remove(observer)
        except Exception as e:
            logger.error("Unable to remove Observer ")
            logger.error(e)

    def notify_all(self, message: object) -> None:
        logger.info("Notifying Observers")
        for observer in self.__observers:
            try:
                observer.update(message)
            except Exception as e:
                logger.error("Unable to notify Observer %s" % observer)
                logger.error(e)
                raise
        if not self.__observers:
            logger.info("No observers on the list")

class ConnectionDB(object):
    """Classe para representar a Interface Genérica para comunicação com banco de dados
    """
    def __init__(self):
        pass

    def create(self, message: object):
        raise Exception("NotImplementedException")

    def update(self, message: object):
        raise Exception("NotImplementedException")

    def delete(self, message: object):
        raise Exception("NotImplementedException")
