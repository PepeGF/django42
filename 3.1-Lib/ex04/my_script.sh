#!/bin/bash

VENV_NAME="django_env"

python3 -m venv $VENV_NAME
source $VENV_NAME/bin/activate
pip install -r requirements.txt --force-reinstall
exec zsh -c "source $VENV_NAME/bin/activate; exec zsh -i"
