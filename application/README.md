# Application Service

Este diretório contém todo o código fonte do serviço `application` do Sistema Smart AniMon. Este serviço é uma aplicação web, desenvolvida com Flask, que disponibiliza informações sobre os animais monitorados e possibilita a configuração de algumas funcionalidades. 

A aplicação se conecta com o banco de dados MongoDB para recuperar as informações inseridas pelo serviço [`processing`](https://github.com/Smart-AniMon/server/tree/main/processing). A seguir você encontrará instruções de como executar o serviço localmente para desenvolvimento.

# Instalação

## Requisitos

* Git.
* Python 3.7 ou superior
* Credenciais para leitura e escrita em uma base MongoDB.

## Download e Configurações.

1. Faça o download do repositório principal e acesse este diretório.
	```bash
	$ git clone https://github.com/Smart-AniMon/server.git
	$ cd server/application
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

5. Crie o arquivo `.env` com base no template `./application_dotenv` e altere as informações da variável `FLASK_MONGO_URI` para conexão com a base MongoDB.
    ```bash
    $ cp ./application_dotenv .env
    $ vim .env
    ```

    ```properties
    # host:12334 -> servidor e porta do MongoDB Server

    FLASK_MONGO_URI="mongodb://<user>:<password>@<host:port>/<db_name>"
    ```
    Altere:
    
    `<user>` para nome de usuário com permissão de escrita e leitura.
    
    `<password>` para senha do usuário com permissão de leitura e escrita

    `<host:port>` pelo IP ou FQDN e porta do Servidor MongoDB.

    `<db_name>` pelo nome do banco de dados (ex. animon_db)

## Execução e testes

1. Para inciar o serviço `application` execute o seguinte comando:
    ```bash
    $ flask run
    ```

2. A aplicação web estará disponível, via navegador, na URL `http://127.0.0.1:5000/`.
