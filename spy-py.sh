#!/bin/bash
echo "spy-py"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        echo "Python is not installed. Please install Python 3.6 or higher."
        exit 1
    else
        python=python3
    fi
else
    python=python
fi

echo "Initializing virtual environment..."
$python -m venv Spy-Py


echo "Installing required packages..."
source Spy-Py/bin/activate
pip install -r requirements.txt

deactivate

clear

$python builder.py

echo ""

echo "########################################################"
echo "#                                                      #"
echo "#  Spy-Py build complete. If you find this project     #"
echo "#    useful, please consider starring it on GitHub!    #"
echo "#   Remember to use the software responsibly, and      #"
echo "#     note that I am not liable for any actions you    #"
echo "#   choose to take with it. Thanks for using Spy-py!   #"
echo "#                                                      #"
echo "########################################################"
echo ""
read -p "Press any key to exit..."
