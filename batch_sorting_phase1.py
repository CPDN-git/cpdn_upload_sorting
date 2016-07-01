#!/usr/bin/env python2.7
import os, sys, time,glob


def batch_sorting_phase1(incoming_folder,batch_folders,results_folder,sort_unknown=False,delete_closed=True):
	#
	# Optional arguments:
	# sort_unknown: sort files that don't match the lists of open or closed batches into "unknown_batches" folder
	#               For this option, the 'open_batches.txt' and 'closed_batches.txt'
	#               need to be up to date otherwise files will be sorted incorrectly
	#               Default is False
	# delete_closed: delete files from closed batches
	#               Default is True
	print time.strftime("%Y/%m/%d %H:%M:%S") + " Starting batch_sorting_phase1.py\n"

	open_batches=[]
	closed_batches=[]
	for dl_path in batch_folders:
		# Create lists of open and closed batches from this project
		for batch in open(os.path.join(dl_path,'open_batches.txt'),'r'):
			open_batches.append(batch.strip())
		for batch in open(os.path.join(dl_path,'closed_batches.txt'),'r'):
			closed_batches.append(batch.strip())

	# Set up folders if needed
	if not os.path.exists(results_folder):
		os.mkdir(results_folder)
	if not os.path.exists(results_folder+'/unknown_batches'):
		os.mkdir(results_folder+'/unknown_batches')

	# Loop over zip files in incoming folder
	for fpath in glob.glob(incoming_folder+'/*.zip'):
		fname=os.path.basename(fpath)
		try:
			# Split string up (assume has the format: hadam3p_eu_fs23_201412_1_d401_000000951_0_r1285010883_1.zip
			str_split=fname.split('_')
			fname_out=''
			if str_split[-2][0]=='r':
				batch=str_split[-5]
				# recombine fname without random part
				for i,part in enumerate(str_split):
					if i != len(str_split)-2:
						fname_out=fname_out+part+'_'
				fname_out=fname_out[:-1] # remove final underscore
			else:
				# Old format without random string
				batch=str_split[-4]
				fname_out=fname
			workunit_name=fname_out[:-len(str_split[-1])-1] # workunit name is fname without the '_1.zip'
			# Check if workunit is from an open batch
			if batch in open_batches:
				batch_folder=results_folder+'/batch_'+batch
				if not os.path.exists(batch_folder):
					os.mkdir(batch_folder)
				if not os.path.exists(batch_folder+'/in_progress/'):
					os.mkdir(batch_folder+'/in_progress/')
				if not os.path.exists(batch_folder+'/in_progress/'+workunit_name):
					os.mkdir(batch_folder+'/in_progress/'+workunit_name)
				os.rename(fpath,batch_folder+'/in_progress/'+workunit_name+'/'+fname_out)
				print fname_out,batch
			# Check if workunit is from a closed batch
			elif batch in closed_batches:
				if delete_closed:
					# Delete this file
					os.remove(fpath)
					print 'deleting from closed batch',fname,batch
			else:
				if sort_unknown:
					os.rename(fpath,results_folder+'/unknown_batches/'+fname)
					print fname,'unknown batch'
		except:
			print "Error sorting file:",fname
	print time.strftime("%Y/%m/%d %H:%M:%S") + " Finished batch_sorting_phase1.py"
#####################

incoming_folder='../upload'
batches_basedir= '.'
results_folder='../results'

# batch files should be rsynced from project_batchlists url to batches_folder/KEY
project_batchlists={}
#project_batchlists['cpdn']='http://climateapps2.oerc.ox.ac.uk/batch/batches.xml'
project_batchlists['cpdn_dev']='http://vorvadoss.oerc.ox.ac.uk/cpdnboinc_dev/download/batch_lists/'

# Set up batch folders
batch_folders=[]
for proj,url in project_batchlists.iteritems():
	dl_dir=os.path.join(batches_basedir,proj)
	#TODO rsync the batch folder from url to dl_dir
	batch_folders.append(dl_dir)

batch_sorting_phase1(incoming_folder,batch_folders,results_folder)
