mkdir incoming results log

# set up incoming files
# These should be in the list of successful workunits
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000001_0_1.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000001_0_2.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000001_0_3.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000001_0_4.zip

cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000002_0_1.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000002_0_2.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000002_0_3.zip
cp corrupt_file.zip incoming/wah2_test_umid_193012_01_999_000000002_0_4.zip

cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000003_0_1.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000003_0_2.zip

# These should be in the list of failed workunits
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000004_0_1.zip
cp corrupt_file.zip incoming/wah2_test_umid_193012_01_999_000000004_0_2.zip

cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000005_0_1.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000005_0_2.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000005_0_3.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000005_0_4.zip

# These should be the 'in progress' workunits
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000006_0_1.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000006_0_2.zip

cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000007_0_1.zip
cp corrupt_file.zip incoming/wah2_test_umid_193012_01_999_000000007_0_2.zip

cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000008_0_1.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000008_0_2.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000008_0_3.zip
cp dummy_file.zip incoming/wah2_test_umid_193012_01_999_000000008_0_4.zip

# Test of batch that only has a corrupt zip file within it 
cp corrupt_file.zip incoming/wah2_test_umid_193012_01_998_000000001_0_2.zip
#cp dummy_file.zip incoming/wah2_test_umid_193012_01_998_000000001_0_2.zip

export RESULTS_FOLDER=./results
export INCOMING_FOLDER=./incoming
export BATCH_LISTS_URLS=./batch_files
export PROJECT_FOLDER_SORTING=TRUE
export TMPDIR=./batch_files
export CLEANUP_CLOSED_BATCHES=TRUE

python ../batch_sorting_phase1.py >> ./log/batch_sorting_phase1.log
python ../batch_sorting_phase2.py >> ./log/batch_sorting_phase2.log
