#!/bin/bash
export BATCH_LISTS_URLS=https://dev.cpdn.org/download/batch_lists,https://www.cpdn.org/batch,http://alpha.cpdn.org/download/batch_lists
export RESULTS_FOLDER=/storage/boinc/project_results
export INCOMING_FOLDER=/storage/incoming/uploader
export TMPDIR=/home/cpdn
export UPLOAD_BASE_URL=http://upload2.cpdn.org/results
export CLEANUP_CLOSED_BATCHES=TRUE
export SORT_BY_PROJECT=TRUE
./batch_sorting_phase1.py >> /var/www/projects/cpdn/log_anemoi/batch_sorting_phase1.log
./batch_sorting_phase2.py >> /var/www/projects/cpdn/log_anemoi/batch_sorting_phase2.log
