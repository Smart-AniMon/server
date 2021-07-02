# False para Desenvolvimento
PRODUCTION=False

if PRODUCTION:
    LOGGING_CONF = '/animon/logging.ini'
else:
    LOGGING_CONF = 'logging.ini'



## Configurar informações de conexão com o broker.
MQTT_BROKER = {
	'HOST' : 'IP ou FQDN do broker',
	'PORT' : Porta_do_broker,
	'USER' : 'User',
	'PASS' : 'Password',
    'TOPIC': "topic/test"
}