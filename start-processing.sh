#!/bin/bash

HOMEDIR="animon"
VENV="${HOMEDIR}/venv"
SYSTEM_DIR=/etc/systemd/system
SYSTEM_FILE=system-unit

if [[ $EUID -ne 0 ]]; then
	echo "Necessário executar como root (sudo)" 
       	exit 1
fi

export PYTHONPATH="${PYTHONPATH}:${HOMEDIR}"

#echo "Executando testes de unidades..."
#${VENV}/bin/pytest ${HOMEDIR}/tests

#echo "Criando banco de dados para backup das informações..."
#${VENV}/bin/python ${HOMEDIR}/

echo "Criando estacao.service em ${SYSTEM_DIR}"
cp ${SYSTEM_FILE} ${SYSTEM_DIR}/animon.service

echo "Configurando Serviço para iniciar com o SO"
systemctl enable animon

echo "Iniciando serviço....."
systemctl start animon