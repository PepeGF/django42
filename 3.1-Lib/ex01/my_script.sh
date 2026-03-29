#!/bin/bash

#
pip --version | cut -d ' ' -f 1,2

rm -rf ../venv
echo "Creating virtual environment..."
python3 -m venv ../venv
echo "Virtual environment created at ../venv"
source ../venv/bin/activate
echo "Virtual environment activated. Installing dependencies..."
rm -rf ./local_lib/*
mkdir -p ./local_lib
pip install --target ./local_lib git+https://github.com/jaraco/path.git --log install.log #--force-reinstall
echo "xxxxxxxxxxxxxxxxxxxxxxxxxxxx" >> install.log
echo "Dependencies installed."
echo "Running the program..."
python3 my_program.py
