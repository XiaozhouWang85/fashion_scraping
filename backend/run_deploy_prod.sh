export CURR_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PARENT_DIR="$(dirname "$CURR_DIR")"

#Run local tests
bash run_local_tests.sh

#Deploy to prod

echo "Deploying to production"
cd $PARENT_DIR
make deploy-prod