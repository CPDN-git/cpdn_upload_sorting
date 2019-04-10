BATCH_SCRIPTS_DIR=/storage/www/cpdnboinc_dev/batch_scripts
LOG_DIR=/storage/www/cpdnboinc_dev/log_vorvadoss
UPLOAD_SCRIPTS_DIR=/storage/www/cpdnboinc_dev/cpdn_upload_sorting

# calculate batch stats and make list of successful and failed workunits
# $BATCH_SCRIPTS_DIR/cpdn_MakeBatchesLists.py 1>> $LOG_DIR/cpdn_MakeBatchesLists.log 2>> $LOG_DIR/cpdn_MakeBatchesLists.err

# Make lists of open and closed batches
# $BATCH_SCRIPTS_DIR/list_open_closed_batches.py 1>> $LOG_DIR/list_open_closed_batches.log 2>> $LOG_DIR/list_open_closed_batches.err

export BATCH_LISTS_URLS=https://dev.cpdn.org/download/batch_lists
export RESULTS_FOLDER=/storage/www/cpdnboinc_dev/results
export INCOMING_FOLDER=/storage/www/cpdnboinc_dev/upload
export TMPDIR=/storage/www/cpdnboinc_dev/cpdn_upload_sorting
export CLEANUP_CLOSED_BATCHES=TRUE
export SORT_BY_PROJECT=TRUE

 # # Do the sorting (phase1: hourly, phase2
$UPLOAD_SCRIPTS_DIR/batch_sorting_phase1.py >> $LOG_DIR/batch_sorting_phase1.log
$UPLOAD_SCRIPTS_DIR/batch_sorting_phase2.py >> $LOG_DIR/batch_sorting_phase2.log

