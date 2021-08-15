import os

APP_PATH = os.environ.get('APP_PATH', '/animon')

# False para Desenvolvimento
PRODUCTION=True

if PRODUCTION:
    LOGGING_CONF = APP_PATH + '/logging.ini'
else:
    LOGGING_CONF = os.path.abspath('./logging.ini')



## Configurar informações de conexão com o broker.
MQTT_BROKER = {
	'HOST' : os.environ.get('BROKER_HOST', 'IP ou FQDN do Broker'),
	'PORT' : os.environ.get('BROKER_PORT', 'Numero Porta_do_broker'),
	'USER' : os.environ.get('BROKER_USER', 'User'),
	'PASS' : os.environ.get('BROKER_PASS', 'Password'),
    'TOPIC': os.environ.get('BROKER_TOPIC', 'topic/test'),
	'CLIENT_NAME': os.environ.get('BROKER_CLIENT_NAME', 'client_name')
}

# Configuração de chave para acessar API Vision (Google)
# https://cloud.google.com/vision/docs/quickstart-client-libraries#client-libraries-install-python

if PRODUCTION:
    VISION_KEY_FILE =  APP_PATH + '/credentials/vision-key.json'
else:
	VISION_KEY_FILE = os.path.abspath("../../smart-animon-vision-key.json")

# Configuração de credenciais para acesso ao MongoDB Server
MONGO_CONNECT = {
	'HOST' : os.environ.get('MONGO_HOST', 'IP ou FQDN do Mongo'),
	'PORT' : os.environ.get('MONGO_PORT', 'Numero da Porta do Mongo'),
	'USER' : os.environ.get('MONGO_USER', 'User'),
	'PASS' : os.environ.get('MONGO_PASS', 'Password'),
	'DATABASE' : os.environ.get('MONGO_DATABASE', 'Database name')
}

DATABASE_COLLECTIONS = {
	'Identifier': 'identified_animals',
	'MQTTClient': 'monitored_animals',
	'Notification': 'notifications',
	'Flag': 'flags'
}



# Lista de Labels que podem ser identificadas como animais
# TODO - Pesquisar mais sobre https://storage.googleapis.com/openimages/web/index.html 

ANIMAL_LABELS = ['ANIMAL',
			     'CAT',
				 'MAMMAL',
				 'PANDA'
]
IDENTIFIED_LABELS_SCORE = 80.00
FULL_LABELS_SCORE = 70.00

RESOURCES = os.environ.get('RESOURCES_PATH', '/animon/resources')
