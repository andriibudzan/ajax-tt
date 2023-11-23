#!/bin/bash

# extracting data from legacy source
echo "Running etl/data_extraction.py..."
python3 ./etl/data_extraction.py

# Check the exit status of data_extraction.py
if [ $? -eq 0 ]; then
    echo "data extracted successfully"

    # Run ./etl/data_transformation_and_loading.py if data_extraction.py was successful
    echo "Running etl/data_transformation.py..."
    python3 ./etl/data_transformation_and_loading.py
    echo "data enriched and loaded successfully"
else
    echo "data_extraction.py failed. Exiting..."
fi
