#Set current directory
export CURR_DIR="$(dirname "${BASH_SOURCE[0]}")"
export GCLOUD_PROJECT='fashion-scraping-staging'

echo "Deploying to staging"
make deploy-staging

echo "Running tests in staging"
pytest tests_staging.py

echo "Deploying website"
cd flask_app
make deploy-website-staging