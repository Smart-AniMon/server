# Processing Service

Este diretório contém todo o código fonte do serviço `processing` do Sistema AniMon. Este serviço precisa de uma conexão com um banco de dados NoSQL (MongoDB) para persistência das informações e também acessa 2 serviços externos: Um servidor broker MQTT para receber as mensagens do componente módulo e a API do [Google Cloud Vision](https://cloud.google.com/vision) para consulta e identificação da Imagens recebidas do módulo.

A seguir você encontrará instruções de como executar o serviço localmente para desenvolvimento.

# Instalação

## Pré-requisitos

* Git.
* Python 3.7 ou superior
* Credenciais para leitura e escrita em um servidor MongoDB.
* Credenciais de um broker MQTT.
* Credenciais para consulta na API do [Google Cloud Vision](https://cloud.google.com/vision/docs/quickstart-client-libraries). 

## Download e Configurações.

1. Faça o download do repositório principal e acesse este diretório.
	```bash
	$ git clone https://github.com/Smart-AniMon/server.git
	$ cd server/processing
	```

2. Crie e ative um ambiente virtual.
    ```bash
	$ python3 -m venv venv
    $ source ./venv/bin/activate
	```
3. Instale as dependências do serviço.
    ```bash
    $ pip install -r requirements.txt
	```

4. Configure a variável `PYTHONPATH`.
    ```bash
    $ export PYTHONPATH="$PWD"
	```

5. Edite o arquivo `settings.py` alterando a variável `PRODUCTION` para `False` e incluindo as informações de conexão com o servidor Broker MQTT e servidor MongoDB.

    ```python
    PRODUCTION = False

    # Configurar informações de conexão com o broker
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
    ```

6. Copie o arquivo JSON com as credenciais da API Cloud Vision para o arquivo `./credentials/vision-key.json`.

    **Obs.:** O nome do arquivo deve ser `vision-key.json` para que a aplicação reconheça.

## Execução e testes

1. Para iniciar o serviço `processing` execute o seguinte script:
    ```bash
    $ python src/principal.py
    ```

2. No diretório `./tests` existem alguns scripts para testar partes diferentes do sistema. Por exemplo, para testar a leitura de uma mensagem no tópico do Broker MQTT configurado, execute o seguinte script:
    ```bash
    $ python tests/test_mqtt.py
    ```

**Obs.:** O sistema `processing` implementa somente um client MQTT para consumir as mensagens do tópico. Mas é possível simular o envio de uma mensagem para o tópico executando o script `./tests/pub.py`.
