#Set current directory
export CURR_DIR="$(dirname "${BASH_SOURCE[0]}")"
export GCLOUD_PROJECT='fashion-scraping-staging'

#Build the 
make venv

pytest tests_local.py