#!/usr/bin/env python
import os, sys, time, glob, urllib2, zipfile, shutil


def batch_sorting_phase1(incoming_folder,batch_urls,results_folder,tmpdir,sort_unknown=False,delete_closed=True):
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
	urlerror=False
	for i,dl_path in enumerate(batch_urls):
		# Read batch lists directly from url
		try:
			for batch in urllib2.urlopen(os.path.join(dl_path,'open_batches.txt'),'r'):
				open_batches.append(batch.strip())
			for batch in urllib2.urlopen(os.path.join(dl_path,'closed_batches.txt'),'r'):
				closed_batches.append(batch.strip())
		# Read backup lists of open and closed batches
		except:
			print 'Error downloading batch lists from ',dl_path,'using backup from tmpdir'
			urlerror=True

	# Read backup lists of open and closed batches
	if urlerror:
		for batch in open(os.path.join(tmpdir,'open_batches.txt'),'r'):
			open_batches.append(batch.strip())
		for batch in open(os.path.join(tmpdir,'closed_batches.txt'),'r'):
			closed_batches.append(batch.strip())
	# Write out backup lists of open and closed batches
	else:
		with open(os.path.join(tmpdir,'open_batches.txt'),'w') as f:
			for batch in open_batches:
				f.write(batch+'\n')
		with open(os.path.join(tmpdir,'closed_batches.txt'),'w') as f:
			for batch in closed_batches:
				f.write(batch+'\n')


	# Set up folders if needed
	if not os.path.exists(results_folder):
		os.mkdir(results_folder)
		os.system('chmod 775 '+results_folder)
	if not os.path.exists(results_folder+'/unknown_batches'):
		os.mkdir(results_folder+'/unknown_batches')
		os.system('chmod 775 '+results_folder+'/unknown_batches')

	# Loop over zip files in incoming folder
	for fpath in glob.glob(incoming_folder+'/*.zip'):
		fname=os.path.basename(fpath)
		try:
			if not zipfile.is_zipfile(fpath):
				raise Exception('File is not a valid zip, may be corrupted or partial file')
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
					os.system('chmod 775 '+batch_folder)
				if not os.path.exists(batch_folder+'/in_progress/'):
					os.mkdir(batch_folder+'/in_progress/')
				if not os.path.exists(batch_folder+'/in_progress/'+workunit_name):
					os.mkdir(batch_folder+'/in_progress/'+workunit_name)
				shutil.move(fpath,batch_folder+'/in_progress/'+workunit_name+'/'+fname_out)
				print fname_out,batch
			# Check if workunit is from a closed batch
			elif batch in closed_batches:
				if delete_closed:
					# Delete this file
					os.remove(fpath)
					print 'deleting from closed batch',fname,batch
			else:
				if sort_unknown:
					shutil.move(fpath,results_folder+'/unknown_batches/'+fname)
					print fname,'unknown batch'
		except Exception,e:
			print "Error sorting file:",fname
			print e
	print time.strftime("%Y/%m/%d %H:%M:%S") + " Finished batch_sorting_phase1.py"
#####################
#
# Script Setup
#
# Requires environment variables:
#
# BATCH_LISTS_URLS: location which the batch directories can be downloaded from
# RESULTS_FOLDER: Location of sorted results
# INCOMING_FOLDER: Location incoming files are uploaded to
#
# Optional environment variable:
# TMPDIR: directory to put backup lists of open and closed batches

batches_urls = os.environ.get('BATCH_LISTS_URLS')
results_folder = os.environ.get('RESULTS_FOLDER')
incoming_folder = os.environ.get('INCOMING_FOLDER')
tmpdir = os.environ.get('TMPDIR')

if not (batches_urls or results_folder or incoming_folder):
	raise Exception("Error, environment variables required: 'BATCH_LISTS_URLS', 'RESULTS_FOLDER', 'INCOMING_FOLDER'")

if not tmpdir:
	tmpdir='/tmp'

batches_urls=batches_urls.split(',') # Allow batches_urls to be a comma separated list

batch_sorting_phase1(incoming_folder,batches_urls,results_folder,tmpdir)
