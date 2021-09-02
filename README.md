# Server

Este repositório contém todo o código fonte e instruções de implantação do componente `Server` do Sistema Smart AniMon, conforme especificado e modelado em [Documentações](https://github.com/Smart-AniMon/docs). 

O `Server` é composto por 3 serviços: O sistema de processamento (processing), o serviço de aplicação web (application) e um banco de dados NoSQL (mongo). Além disso, são utilizados 2 serviços externos: Um servidor broker MQTT para receber as mensagens do componente módulo e a API do [Google Cloud Vision](https://cloud.google.com/vision) para identificação da imagens recebidas do módulo.

A seguir você encontrará instruções de como implementar os três serviços utilizando composição de contêineres. Para mais detalhes de como executar os serviços separadamente, consulte [processing](https://github.com/Smart-AniMon/server/tree/main/processing) ou [application](https://github.com/Smart-AniMon/server/tree/main/application).


# Instalação

## Requisitos

* Servidor e acesso root.
    * RAM: 2 GB
    * HD: 10 GB
* Git.
* Docker 17.05 ou superior.
* Docker Compose 1.25.0 ou superior.
* Credenciais de um broker MQTT.
* Credenciais para consulta na API do [Google Cloud Vision](https://cloud.google.com/vision/docs/quickstart-client-libraries). 

## Configurando a composição

1. Faça o download deste repositório.

	```bash
	$ git clone https://github.com/Smart-AniMon/server.git
	$ cd server
	```

2. Edite o arquivo `./processing-envs` e altere as informações do servidor Broker MQTT.
    ```properties
    # Broker - definir
    BROKER_HOST=FQDN_Broker
    BROKER_PORT=Porta_Broker
    BROKER_USER=user_broker
    BROKER_PASS=pass_broker
    BROKER_TOPIC=topic/test
    CLIENT_NAME=client_name
    ```
3. Crie o arquivo `.env` com base no template `./compose_dotenv` e altere o valor de `VISION_KEY_FILE` para o caminho do arquivo json com a chave de acesso da API Vision. Altere também o valor de `WEB_APP_PORT` para a porta que a aplicação web estará disponível.

    ```bash
    $ cp ./compose_dotenv .env
    $ vim .env
    ```

    ```properties
    # Não alterer se estiver usando a composição
    MONGO_DATABASE=animon_db 
    
    # Arquivo json com credenciais para consulta da API
    VISION_KEY_FILE=./vision-key.json

    # Porta na qual a aplicação Flask estará acessível.
    WEB_APP_PORT=80 
    ```
## Executando a composição

1. Para criar os contêineres e iniciar a composição execute o seguinte comando: 

    ```bash
    $ sudo docker-compose up
    ```

    **Obs.:** Para executar em modo daemon acrescente `-d`.

2. Acesse, via navegador, o IP ou FQDN do servidor com a porta configurada para visualizar a aplicação (ex. `http://FQDN:PORT/`)

### Comandos úteis

1. Para acompanhar os logs da composição quando executada no modo daemon, os seguintes comandos podem ser utilizados:

    a. Verificar de todos os serviços.
    ```bash
    $ sudo docker-compose logs -f
    ```
    b. Logs por serviços. Substitua `<serviço>` pelo nome do serviço desejado. (`application`, `processing` ou `mongo`)
    ```bash
    $ sudo docker-compose logs -f <serviço>
    ```

2. Se desejar parar ou iniciar a composição ou um serviço específico, os seguintes comandos podem ser utilizados:
    
    a. Parar/Iniciar todos os serviços sem destruir os contêineres.
    ```bash
    $ sudo docker-compose [stop|start]
    ```

    b. Parar/Inciar um serviço. Substitua `<serviço>` pelo nome do serviço desejado. (`application`, `processing` ou `mongo`)
     ```bash
    $ sudo docker-compose [stop|start] <serviço>
    ```

    c. Parar/Iniciar todos os serviços e destruir/reconstruir os contêineres e redes.
    ```bash
    $ sudo docker-compose [down|up]
    ```

    d. Parar/Iniciar e destruir um serviço e destruir/reconstruir o contêiner. Substitua `<serviço>` pelo nome do serviço desejado. (`application`, `processing` ou `mongo`)
     ```bash
    $ sudo docker-compose [down|up] <serviço>
    ```

    **Obs.:** Os serviços `application` e `processing` compartilham um volume criado pelo docker para armazenar os arquivos de imagens. Se desejar parar os serviços eliminando também esses volumes, execute o comando indicado no item `c` com o parâmetro `--volume`.
