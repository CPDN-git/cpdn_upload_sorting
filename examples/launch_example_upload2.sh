#!/bin/bash
export BATCH_LISTS_URLS=http://vorvadoss.oerc.ox.ac.uk/cpdnboinc_dev/download/batch_lists,http://climateapps2.oerc.ox.ac.uk/batch
export RESULTS_FOLDER=/storage/boinc/upload
export INCOMING_FOLDER=/storage/incoming/uploader
export TMPDIR=/home/cpdn
export UPLOAD_BASE_URL=http://upload2.cpdn.org/results
./batch_sorting_phase1.py >> /var/www/projects/cpdn/log_anemoi/batch_sorting_phase1.log
./batch_sorting_phase2.py >> /var/www/projects/cpdn/log_anemoi/batch_sorting_phase2.log