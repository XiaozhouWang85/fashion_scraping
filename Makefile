$(CURR_DIR)/.python-versions: $(CURR_DIR)/requirements.txt
    pyenv virtualenv --force 3.7.1 "pyenv.$(PYENV_NAME)"; \
    pyenv local pyenv.$(PYENV_NAME); \
    pip install --upgrade pip setuptools; \
    pip install -r requirements.txt

venv: $(CURR_DIR)/.python-versions

deploy-staging:
    gcloud functions deploy scrape_website --project "fashion-scraping-staging" \
    --runtime python37 --trigger-http --timeout=9m --quiet --allow-unauthenticated \
    --memory 1024MB 
    gcloud functions deploy orchestrator --project "fashion-scraping-staging" \
    --runtime python37 --trigger-http --timeout=9m --quiet --allow-unauthenticated

deploy-prod:
    gcloud functions deploy scrape_website --project "fashion-scraping" \
    --runtime python37 --trigger-http --timeout=9m --quiet --allow-unauthenticated
    gcloud functions deploy orchestrator --project "fashion-scraping" \
    --runtime python37 --trigger-http --timeout=9m --quiet --allow-unauthenticated

    gcloud scheduler jobs update http run_fashion_scraper \
    --project "fashion-scraping" --description="Trigger cloud function to scrape and log data" \
    --schedule="0 8,18 * * *" --uri=https://us-central1-fashion-scraping.cloudfunctions.net/orchestrator \
    --http-method=POST --message-body="{}" --max-retry-attempts 3 --max-backoff 10s --attempt-deadline 10m \
    --oidc-service-account-email=fashion-scraping@appspot.gserviceaccount.com