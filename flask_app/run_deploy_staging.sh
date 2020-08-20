#Set current directory
export CURR_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PARENT_DIR="$(dirname "$CURR_DIR")"

cd $PARENT_DIR
make deploy-website-staging
