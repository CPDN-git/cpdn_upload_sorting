export BATCH_LISTS_URLS=http://vorvadoss.oerc.ox.ac.uk/cpdnboinc_dev/download/batch_lists,https://www.cpdn.org/batch,http://vorvadoss.oerc.ox.ac.uk/cpdnboinc_alpha/download/batch_lists
export RESULTS_FOLDER=/data5/boinc/upload/wah2
export INCOMING_FOLDER=/climate2/incoming/uploader
export CLEANUP_CLOSED_BATCHES=TRUE
export TMPDIR=/home/cpdn

SCRIPTS_DIR=/home/cpdn/cpdn_upload_sorting
LOG_DIR=/var/www/projects/cpdn/log_cpdn-upload5

# Do the sorting
/usr/bin/python26 $SCRIPTS_DIR/batch_sorting_phase1.py >> $LOG_DIR/batch_sorting_phase1.log
/usr/bin/python26 $SCRIPTS_DIR/batch_sorting_phase2.py >> $LOG_DIR/batch_sorting_phase2.log

