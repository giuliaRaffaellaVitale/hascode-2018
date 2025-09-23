#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: ./run.sh <input_letter>"
    exit 1
fi

# Set the input file based on the argument
input_file="input/$1.txt"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Input file $input_file does not exist."
    exit 1
fi

# Compile the C++ judge file
g++ -o judge judgeHashCode2018.cpp

# Run the Python script with the specified input file
python3 app.py "$input_file"

# Run the judge program with the input and output files
./judge "$input_file" result.txt