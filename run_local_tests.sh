#Set current directory
export CURR_DIR="$(pwd)"
export PYENV_NAME="$(basename "$(pwd)")"
export GCLOUD_PROJECT='fashion-scraping-staging'

#Build the 
make venv

pytest tests_local.py