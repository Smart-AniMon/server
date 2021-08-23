import os

####### Inicio das Variáveis da aplicação. #######
# Se for usar contêiner é possível configurar como variáveis de ambiente.

PRODUCTION = False
LOGGING_LEVEL = 'INFO'
APP_PATH = '/animon/processing'
RESOURCES_PATH = APP_PATH + '/resources'

## Configurar informações de conexão com o broker
BROKER_HOST = 'Ip ou Host do Broker (ex. 127.0.0.1)'
BROKER_PORT = 'Porta do Broker (ex. 1883)'
BROKER_USER = 'usuario com permissão para subscribe'
BROKER_PASS = 'senha do usuario'
BROKER_TOPIC = 'topico para o subscribe (ex. topic/test)'
BROKER_CLIENT_NAME = 'nome para o cliente (ex. app_name)'


# Configuração de credenciais para acesso ao MongoDB Server

MONGO_HOST = 'Ip ou Host do MongoDB Server (ex. 127.0.0.1)'
MONGO_PORT = 'Porta do MongoDB Server (ex. 27017)'
MONGO_USER = 'usuario com permissão para leitura e escrita'
MONGO_PASS = 'senha do usuario'
MONGO_DATABASE = 'nome do database (ex. app_db)'


####### FIM das Variáveis da aplicação. ######


###############################################
##### Não alterar as configurações abaixo. ####
# Altere somente para adicionar funcionalidades ou mudar algum comportamento

if not PRODUCTION:
	LOGGING_LEVEL = 'DEBUG'
	APP_PATH = '.'
	RESOURCES_PATH = os.path.abspath('../application/webapp/blueprints/frontend/static/resources')

LOG_LEVEL = os.environ.get('LOGGING_LEVEL', LOGGING_LEVEL)
APPLICATION_PATH = os.environ.get('APP_PATH', APP_PATH)
RESOURCES = os.environ.get('RESOURCES_PATH', RESOURCES_PATH)

MQTT_BROKER = {
	'HOST' : os.environ.get('BROKER_HOST', BROKER_HOST),
	'PORT' : os.environ.get('BROKER_PORT', BROKER_PORT),
	'USER' : os.environ.get('BROKER_USER', BROKER_USER),
	'PASS' : os.environ.get('BROKER_PASS', BROKER_PASS),
    'TOPIC': os.environ.get('BROKER_TOPIC', BROKER_TOPIC),
	'CLIENT_NAME': os.environ.get('BROKER_CLIENT_NAME', BROKER_CLIENT_NAME)
}

# Configuração de chave para acessar API Vision (Google)
# https://cloud.google.com/vision/docs/quickstart-client-libraries#client-libraries-install-python

VISION_KEY_FILE =  os.path.abspath(APPLICATION_PATH + '/credentials/vision-key.json')

# Configuração de credenciais para acesso ao MongoDB Server
MONGO_CONNECT = {
	'HOST' : os.environ.get('MONGO_HOST', MONGO_HOST),
	'PORT' : os.environ.get('MONGO_PORT', MONGO_PORT),
	'USER' : os.environ.get('MONGO_USER', MONGO_USER),
	'PASS' : os.environ.get('MONGO_PASS', MONGO_PASS),
	'DATABASE' : os.environ.get('MONGO_DATABASE', MONGO_DATABASE)
}

# Coleções do Mongo
DATABASE_COLLECTIONS = {
	'Identifier': 'identified_animals',
	'MQTTClient': 'monitored_animals',
	'Notification': 'notifications',
	'Flag': 'flags',
	'Label': 'labels'
}


# Lista de Labels que podem ser identificadas como animais
# TODO - Pesquisar mais sobre https://storage.googleapis.com/openimages/web/index.html 

ANIMAL_LABELS = [
	'ANIMAL',
	'MAMMAL'
]
IDENTIFIED_LABELS_SCORE = 70.00
FULL_LABELS_SCORE = 60.00


# Configuração do LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s - %(message)s'
        },
		'file': {
            'format': '%(asctime)s [%(levelname)s] %(name)s.%(funcName)s - %(message)s'
        },
    },
    'handlers': {
        'root': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
			'formatter': 'standard',
        },
        'src': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
			'formatter': 'standard',
        },
        'm': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
			'formatter': 'standard',
        },        
    },
    'loggers': {
        'root': {
            'handlers': ['root'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'src': {
            'handlers': ['src'],
            'level': LOG_LEVEL,
			'qualname': ['src', 'MQTTClient'],
            'propagate': False,
        },
        'm': {
            'handlers': ['m'],
            'level': LOG_LEVEL,
			'qualname': 'm',
            'propagate': False,
        },
    },
}
