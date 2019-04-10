#!/bin/bash
### Environment Variables for batch sorting scripts
#
# location of lists of batches and successful/failed workunits
#export BATCH_LISTS_URLS=https://dev.cpdn.org/download/batch_lists,https://www.cpdn.org/batch,http://alpha.cpdn.org/download/batch_lists
export BATCH_LISTS_URLS=https://www.cpdn.org/batch

# Folder for sorted results
export RESULTS_FOLDER=/storage/boinc/project_results

# Incoming folder where new uploads are put
export INCOMING_FOLDER=/storage/incoming/uploader

# (optional) temporary directory which the backup 'open_batches.txt' and 'closed_batches.txt' are saved to
export TMPDIR=/home/boinc-daemon/cpdn_upload_sorting/tmp

# (optional) url for sorted files on the upload folder (goes into list of successful workunits as a 'wget' file)
#UPLOAD_BASE_URL=http://upload11.cpdn.org/results

# Directory which these scripts are cloned into
export SCRIPTS_DIR=/home/boinc-daemon/cpdn_upload_sorting

# Directory for log files
export LOG_DIR=/home/boinc-daemon/log

# Cleanup the data from closed batches 
export CLEANUP_CLOSED_BATCHES=TRUE

# Sort by project
export SORT_BY_PROJECT=TRUE
 

# Do the sorting (phase1: hourly, phase2: daily @ 7am)
$SCRIPTS_DIR/batch_sorting_phase1.py >> $LOG_DIR/batch_sorting_phase1.log

chmod -R 775 $RESULTS_FOLDER

$SCRIPTS_DIR/batch_sorting_phase2.py >> $LOG_DIR/batch_sorting_phase2.log
