#Run local tests
bash run_local_tests.sh

#Deploy to staging and run tests in staging
bash run_staging_tests.sh

#Deploy to prod
make deploy-prod