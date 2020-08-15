#Set current directory
export CURR_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PARENT_DIR="$(dirname "$CURR_DIR")"
export PYENV_NAME="$(basename "$PARENT_DIR").$(basename "$CURR_DIR")"
export GCLOUD_PROJECT='fashion-scraping-staging'

echo "Deploying to staging"
cd $PARENT_DIR
make deploy-staging