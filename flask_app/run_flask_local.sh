f#Set current directory
export CURR_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PARENT_DIR="$(dirname "$CURR_DIR")"
export PYENV_NAME="$(basename "$PARENT_DIR").$(basename "$CURR_DIR")"
export GCLOUD_PROJECT='fashion-scraping'
export APPLICATION_ID='fashion-scraping'

echo "Building python environment"
cd $PARENT_DIR
make venv

echo "Running local tests"
cd $CURR_DIR
python main.py