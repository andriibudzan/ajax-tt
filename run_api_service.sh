#!/bin/bash

echo "running etl pipeline..."
./etl_runner.sh

echo "starting api service..."
python3 ./app.py
