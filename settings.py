import os

# False para Desenvolvimento
PRODUCTION=False

if PRODUCTION:
    LOGGING_CONF = '/animon/logging.ini'
else:
    LOGGING_CONF = os.path.abspath('./logging.ini')



## Configurar informações de conexão com o broker.

MQTT_BROKER = {
	'HOST' : 'IP ou FQDN do broker',
	'PORT' : Porta_do_broker,
	'USER' : 'User',
	'PASS' : 'Password',
    'TOPIC': "topic/test",
	'CLIENT_NAME': "client_name"
}

# Configuração de chave para acessar API Vision (Google)
# https://cloud.google.com/vision/docs/quickstart-client-libraries#client-libraries-install-python

if PRODUCTION:
    VISION_KEY_FILE = '/animon/credentials/vision-key.json'
else:
	VISION_KEY_FILE = os.path.abspath("../smart-animon-vision-key.json")

# Configuração de credenciais para acesso ao MongoDB Server

MONGO_CONNECT = {
	'HOST' : 'IP ou FQDN do broker',
	'PORT' : Porta_do_broker,
	'USER' : 'User',
	'PASS' : 'Password'
}


DATABASE_COLLECTIONS = {
	'Identifier': 'identified_animals',
	'MQTTClient': 'monitored_animals'
}



# Lista de Labels que podem ser identificadas como animais
# TODO - Pesquisar mais sobre https://storage.googleapis.com/openimages/web/index.html 

ANIMAL_LABELS = ['ANIMAL',
			     'CAT',
				 'MAMMAL'
]

