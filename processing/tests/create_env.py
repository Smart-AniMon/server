import os

os.environ['BROKER_HOST'] = 'localhost'
os.environ['BROKER_PORT'] = '1883'
os.environ['BROKER_USER'] = 'user'
os.environ['BROKER_PASS'] = 'pass'
os.environ['BROKER_TOPIC'] = 'topic/test'
os.environ['BROKER_CLIENT_NAME'] = 'cliente_name'