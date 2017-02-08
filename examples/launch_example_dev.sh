# Crontab for upload sorting on dev site
BATCH_LISTS_URLS=http://vorvadoss.oerc.ox.ac.uk/cpdnboinc_dev/download/batch_lists
RESULTS_FOLDER=/storage/boinc/projects/cpdnboinc_dev/results
INCOMING_FOLDER=/storage/boinc/projects/cpdnboinc_dev/upload
TMPDIR=/storage/boinc/projects/cpdnboinc_dev/cpdn_upload_sorting
UPLOAD_SCRIPTS_DIR=/storage/boinc/projects/cpdnboinc_dev/cpdn_upload_sorting
SORT_BY_PROJECT=TRUE
CLEANUP_CLOSED_BATCHES=TRUE
# Pull updates from repo
 55 * * * * /bin/sh -c "cd $UPLOAD_SCRIPTS_DIR && /usr/bin/git pull origin master" 2>/dev/null
#
# # Do the sorting (phase1: hourly, phase2: daily @ 7:15am)
 0 * * * * $UPLOAD_SCRIPTS_DIR/batch_sorting_phase1.py >> $LOG_DIR/batch_sorting_phase1.log
 15 7 * * * $UPLOAD_SCRIPTS_DIR/batch_sorting_phase2.py >> $LOG_DIR/batch_sorting_phase2.log
