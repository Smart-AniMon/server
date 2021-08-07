#!/bin/bash

cd $APP_PATH

export PYTHONPATH="$PWD"

python webapp/app.py
