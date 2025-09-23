@echo off
REM filepath: c:\Users\giuli\hascode-2018\run.bat

REM Check if argument is provided
IF "%~1"=="" (
    echo Usage: run.bat input_letter
    exit /b 1
)

REM Set the input file based on the argument
SET input_file=input\%1.txt

REM Check if the input file exists
IF NOT EXIST "%input_file%" (
    echo Input file %input_file% does not exist.
    exit /b 1
)

REM Compile the C++ judge file
g++ -o judge judgeHashCode2018.cpp

REM Run the Python script with the specified input file
python app.py "%input_file%"

REM Run the judge program with the input and output files
judge "%input_file%" result.txt