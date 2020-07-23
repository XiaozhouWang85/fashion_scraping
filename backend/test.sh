export CURR_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PARENT_DIR="$(dirname "$CURR_DIR")"
export PYENV_NAME="$(basename "$PARENT_DIR").$(basename "$CURR_DIR")"
export GCLOUD_PROJECT='fashion-scraping-staging'

echo $CURR_DIR
echo $PARENT_DIR
echo $PYENV_NAME
echo $GCLOUD_PROJECT