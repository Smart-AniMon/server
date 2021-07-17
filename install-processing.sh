#!/bin/bash

HOMEDIR="/home/felipe/animon"
VENV="${HOMEDIR}/venv"

if [[ $EUID -ne 0 ]]; then
	echo "Necessário executar como root (sudo)" 
       	exit 1
fi

if [ -d "${HOMEDIR}" ]
then
	echo "Diretório ${HOMEDIR} encontrado"
else
	echo "Criando diretório de implantação....."
	mkdir ${HOMEDIR}
	echo "Copiando arquivos para diretório de implantação....."
	cp -r ./* ${HOMEDIR}
fi

if [ -d "${VENV}" ]
then
	echo "Ambiente virtual encontrado em ${VENV}"
else
	echo "Criando ambiente virtual em ${VENV}"
	echo "Atenção! Esta etapa pode demorar alguns minutos....."
	virtualenv -p python3 ${VENV}
fi

echo "Instalando requisitos da aplicação"
echo "Atenção! Esta etapa pode demorar alguns minutos....."
${VENV}/bin/pip3 install -r ${HOMEDIR}/requirements.txt