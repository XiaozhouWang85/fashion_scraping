#Set current directory
export CURR_DIR="$(dirname "${BASH_SOURCE[0]}")"

#Build the 
make venv

pytest test.py