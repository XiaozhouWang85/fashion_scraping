#Set current directory
export CURR_DIR="$(dirname "${BASH_SOURCE[0]}")"
export GCLOUD_PROJECT="staging"

#Build the 
make venv

pytest test.py