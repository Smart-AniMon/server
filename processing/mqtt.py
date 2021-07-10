"""
Módulo com definições para o cliente de fila de mensagem MQTT.
"""

from .interfaces import Subject
from .utils import ReturnCodesMQTT
from settings import MQTT_BROKER, LOGGING_CONF
from paho.mqtt import client as mqtt_client

import logging, logging.config, json

#logging.config.fileConfig(fname=LOGGING_CONF)
logger = logging.getLogger(__name__)

class MQTTClient(Subject):
    """Classe que representa um Client MQTT para consumir as mensagens de um tópico.
       foi construido utilizando a implementação de Client Subscribe da biblioteca paho.

    Args:
        Subject : Extende a Classe abstrata com métodos para padrão Observer.
    """

    def __init__(self):
        super().__init__()
        logger.debug("Starting MQTTClient")
        self.__host = MQTT_BROKER['HOST']
        self.__port = MQTT_BROKER['PORT']
        self.__user = MQTT_BROKER['USER']
        self.__pass = MQTT_BROKER['PASS']
        self.__topic = MQTT_BROKER['TOPIC']
        self.__client_name = MQTT_BROKER['CLIENT_NAME']
        self.__consumer =  mqtt_client.Client(self.__client_name)

    def connect(self):
        logger.info("connecting to broker %s on port %s" % (self.__host, self.__port))
        logger.debug("credentials %s - %s" % (self.__user, self.__pass))
        self.__consumer.username_pw_set(self.__user, self.__pass)
        self.__consumer.on_connect = self.__connect_callback
        self.__consumer.on_message = self.__message_callback
        try:
            self.__consumer.connect(self.__host, self.__port)
        except ConnectionRefusedError:
            logger.error("Não foi possível estabelecer conexão com Broker. Verifique parâmetros em settings.py")
        except Exception as e:
            logger.error(e)
            raise
        else:
            try:
                logger.info("Starting ClientMQTT")
                self.__consumer.loop_forever()
            except KeyboardInterrupt:
                logger.error("Exit")
            except Exception as e:
                logger.error(e)
                raise 

    def __connect_callback(self, client, userdata, flags, rc):
        logger.debug("client = %s" % client)
        logger.debug("userdate = %s" % userdata)
        logger.debug("flags = %s" % flags)
        logger.debug("rc = %s" % rc)
        message_rc = ReturnCodesMQTT.get_message(rc)
        if rc == 0:
            logger.info("connected to broker")
            logger.info("Subscribe in topic %s" % self.__topic)
            client.subscribe(self.__topic)
            logger.info("waiting for messages")
        else:
            logger.warn("%s" % message_rc)

    def __message_callback(self, client, userdata, msg):
        
        payload_json = msg.payload.decode()

        logger.debug("client = %s" % client)
        logger.debug("userdate = %s" % userdata)
        logger.debug("msg = %s" % payload_json)
        logger.info("Message received from broker")

        message = json.loads(payload_json)

        self.notify_all(message)




