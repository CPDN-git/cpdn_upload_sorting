#!/usr/bin/env python2
import os, sys, time, glob, urllib2, zipfile, shutil
import xml.etree.ElementTree as ET

def batch_sorting_phase1(incoming_folder,batch_urls,results_folder,tmpdir,sort_unknown=False,delete_incoming_closed=True,sort_by_project=False):
	#
	# Optional arguments:
	# sort_unknown: 
	#               sort files that don't match the lists of open or closed batches into "unknown_batches" folder
	#               For this option, the 'open_batches.txt' and 'closed_batches.txt'
	#               need to be up to date otherwise files will be sorted incorrectly
	#               Default is False
	# delete_incoming_closed: 
	#               Delete new files in the incoming folder from closed batches 
	#               If false files will build up in the incoming folder
	#               Default is true
	# sort_by_project: 
	#               Add project directory in result folder structure:
	#               TRUE: $RESULTS_FOLDER/$PROJECT/batch_XXX
	#               FALSE: $RESULTS_FOLDER/batch_XXX
	#               Default is False
	print time.strftime("%Y/%m/%d %H:%M:%S") + " Starting batch_sorting_phase1.py\n"

	# Function useful for debugging: 
	# fall back to trying to open as a local file if the url doesn't exist
	def read_url_or_file(fname):
		try:
			return urllib2.urlopen(fname,'r')
		except:
			return open(fname,'r')

	open_batches=[]
	closed_batches=[]
	batch_projects={}
	
	urlerror=False
	for i,dl_path in enumerate(batch_urls):
		# Read batch lists directly from url
		try:
			for batch in read_url_or_file(os.path.join(dl_path,'open_batches.txt')):
				open_batches.append(batch.strip())
			for batch in read_url_or_file(os.path.join(dl_path,'closed_batches.txt')):
				closed_batches.append(batch.strip())
				
			# Get the project for each batchid
			if sort_by_project:

				batchxml=ET.parse(read_url_or_file(dl_path+'/batches.xml')).getroot()
				for batch in batchxml.findall('batch'):
					batchid=batch.attrib['id']
					batch_projects[batchid]=batch.find('project').text.lower()

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
				# If we are sorting by project, append the project to the results path. 
				if sort_by_project:
					results_folder2= os.path.join(results_folder,batch_projects[batch])
					if not os.path.exists(results_folder2):
						os.mkdir(results_folder2)
						os.system('chmod 775 '+results_folder2)
				else:
					results_folder2=results_folder
				batch_folder=results_folder2+'/batch_'+batch
				if not os.path.exists(batch_folder):
					os.mkdir(batch_folder)
					os.system('chmod 775 '+batch_folder)
				if not os.path.exists(batch_folder+'/in_progress/'):
					os.mkdir(batch_folder+'/in_progress/')
				if not os.path.exists(batch_folder+'/in_progress/'+workunit_name):
					os.mkdir(batch_folder+'/in_progress/'+workunit_name)
				# Before moving, check the file is a complete zip file
				if not zipfile.is_zipfile(fpath):
					raise Exception('File is not a valid zip, may be corrupted or partial file')
				# Move to batch folder
				print fname_out,batch
				shutil.move(fpath,batch_folder+'/in_progress/'+workunit_name+'/'+fname_out)
			# Check if workunit is from a closed batch
			elif batch in closed_batches:
				if delete_incoming_closed:
					# Delete this file
					os.remove(fpath)
					print 'deleting from closed batch',fname,batch
			else:
				if sort_unknown:
					# Before moving, check the file is a complete zip file
					if not zipfile.is_zipfile(fpath):
						raise Exception('File is not a valid zip, may be corrupted or partial file')
					# Move to unknown batches folder
					print fname,'moving to unknown_batches'
					shutil.move(fpath,results_folder+'/unknown_batches/'+fname)
				else:
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
# 
# Optional environment variables (logical flags):
# DELETE_INCOMING_CLOSED, SORT_BY_PROJECT, SORT_UNKNOWN:
# See notes in batch_sorting_phase1 function


batches_urls = os.environ.get('BATCH_LISTS_URLS')
results_folder = os.environ.get('RESULTS_FOLDER')
incoming_folder = os.environ.get('INCOMING_FOLDER')
tmpdir = os.environ.get('TMPDIR')

option = os.environ.get('DELETE_INCOMING_CLOSED')
if option is not None and option.upper() == 'FALSE':
	delete_incoming_closed=False
else: # Default to True
	delete_incoming_closed=True

option = os.environ.get('SORT_BY_PROJECT')
if option is not None and option.upper() == 'TRUE':
	sort_by_project=True
else: # Default to False
	sort_by_project=False
	
option = os.environ.get('SORT_UNKNOWN')
if option is not None and option.upper() == 'TRUE':
	sort_unknown=True
else: # Default to False
	sort_unknown=False

if not (batches_urls or results_folder or incoming_folder):
	raise Exception("Error, environment variables required: 'BATCH_LISTS_URLS', 'RESULTS_FOLDER', 'INCOMING_FOLDER'")

if not tmpdir:
	tmpdir='/tmp'

batches_urls=batches_urls.split(',') # Allow batches_urls to be a comma separated list

batch_sorting_phase1(incoming_folder,batches_urls,results_folder,tmpdir,sort_unknown=sort_unknown,delete_incoming_closed=delete_incoming_closed,sort_by_project=sort_by_project)
