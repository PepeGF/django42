#!/bin/bash

#
pip --version | cut -d ' ' -f 1,2

rm -rf ./venv
echo "Creating virtual environment..."
python3 -m venv ./venv
echo "Virtual environment created at ./venv"
source ./venv/bin/activate
echo "Virtual environment activated. Installing dependencies..."
# install path.py from its github page https://github.com/jaraco/path en el directorio del proyecto y guarda el log en un archivo llamado install.log

rm -rf ./local_lib/*
mkdir -p ./local_lib
pip install --upgrade pip setuptools wheel setuptools_scm 2>&1 | tee install.log
echo "----------------------------" >> install.log
pip install --target ./local_lib git+https://github.com/jaraco/path.git 2>&1 | tee -a install.log
echo "xxxxxxxxxxxxxxxxxxxxxxxxxxxx" >> install.log
echo "Dependencies installed."
echo "Running the program..."
# print python3 executable path
which python3
python3 my_program.py
