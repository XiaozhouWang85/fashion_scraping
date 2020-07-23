#Set current directory
export CURR_DIR="$(pwd)"
export PYENV_NAME="$(basename "$(pwd)")"
export GCLOUD_PROJECT='fashion-scraping-staging'

#Build the 
echo "Building python environment"
make venv

echo "Running local tests"
pytest tests_local.py