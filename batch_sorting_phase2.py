#!/usr/bin/env python2.7
import os, sys, time, glob, gzip
import xml.etree.ElementTree as ET

def batch_sorting_phase2(batch_folders,results_folder,upload_base,cleanup_closed=False):
	#
	# Optional argument 'cleanup_closed: 
	# Delete folders for 'failed' and 'in_progress' workunits for closed batches
	#
	print time.strftime("%Y/%m/%d %H:%M:%S") + " Starting batch_sorting_phase2.py\n"

	open_batches=[]
	closed_batches=[]
	batch_ul_files={}
	for dl_path in batch_folders:
		# Get lists of open and closed batches from this project
		for batch in open(dl_path+'/open_batches.txt'):
			open_batches.append(batch.strip())
		for batch in open(dl_path+'/closed_batches.txt'):
			closed_batches.append(batch.strip())

		# Get number of upload files for each batch
		batchxml=ET.parse(dl_path+'/batches.xml').getroot()
		for batch in batchxml.findall('batch'):
			batchid=batch.attrib['id']
			ul_files=batch.find('ul_files').text
			batch_ul_files[batchid]=ul_files

	# Set up folders if needed
	if not os.path.exists(results_folder):
		raise Exception("Error results folder doesnt exist: "+results_folder)

	# Loop over batches
	for batch_path in glob.glob(results_folder+'/*'):
		# Assume batch folder is in the form results_folder/batch_XXX
		if os.path.basename(batch_path)[:6]=='batch_':
			batch=os.path.basename(batch_path).split('_')[-1]
		else:
			continue
		try:
			if batch in open_batches:
				print "Sorting batch",batch

				# Get lists of successful and failed tasks
				successful_tasks=[]
				failed_tasks=[]
				for batch_folder in batch_folders:
					try:
						for task in open(batch_folder+'/batch_'+batch+'_successful_wus'):
							successful_tasks.append(task.strip())
						for task in open(batch_folder+'/batch_'+batch+'_failed_wus'):
							failed_tasks.append(task.strip())
					except:
						continue

				# Create folders if needed
				if len(successful_tasks)>0:
					success_folder=os.path.join(batch_path,'successful')
					if not os.path.exists(success_folder):
						os.mkdir(success_folder)
					# Set up gzipped text file for list of successful output files
					f_success= gzip.open(os.path.join(batch_path,'batch_'+batch+'.txt.gz'), 'ab')
				if len(failed_tasks)>0:
					failed_folder=os.path.join(batch_path,'failed')
					if not os.path.exists(failed_folder):
						os.mkdir(failed_folder)

				# Loop over in progress tasks
				for in_progress_task in  glob.glob(os.path.join(batch_path,'in_progress/*')):
					taskname=os.path.basename(in_progress_task)
					if taskname in successful_tasks:
						# Check if there are the right number of upload files
						ul_files=len(glob.glob(in_progress_task+'/*.zip'))
						if ul_files==batch_ul_files[batch]:
							print in_progress_task,'to',os.path.join(success_folder,taskname)
							os.rename(in_progress_task,os.path.join(success_folder,taskname))
							# Write list of output files to f_success text file
							for zipname in glob.glob(os.path.join(success_folder,taskname,'*')):
								f_success.write(upload_base+zipname[len(results_folder):]+'\n')
						else:
							print "Error, wrong number of output files for task",taskname,ul_files
					elif taskname in failed_tasks:
						print in_progress_task,'to',os.path.join(failed_folder,taskname)
						os.rename(in_progress_task,os.path.join(failed_folder,taskname))

				# Cleanup successful tasks file
				if len(successful_tasks)>0:
					f_success.close()

			elif batch in closed_batches:
				print "batch",batch,"is closed"
				if cleanup_closed:
					fail_path=os.path.join(batch_path,'failed')
					if os.path.exists(fail_path):
						print 'Cleaning up failed workunits in:',fail_path
						shutil.rmtree(fail_path)
					in_progress_path=os.path.join(batch_path,'in_progress')
					if os.path.exists(in_progress_path):
						print 'Cleaning up in progress workunits in:',in_progress_path
						shutil.rmtree(in_progress_path)
				else:
					print "...skipping"
			else:
				print "batch",batch,"is unknown"
		except Exception,e:
			print "Error sorting batch",batch
			print e
	print time.strftime("%Y/%m/%d %H:%M:%S") + " Finished batch_sorting_phase2.py"
#####################
#
# Script Setup

batches_basedir= '.'
results_folder='/storage/boinc/projects/cpdnboinc_dev/results'

# TODO, for upload servers that are publically accessible, this should be a url e.g. 
# UPLOAD_BASE = 'http://upload2.cpdn.org/results'
# maybe address this as an environment variable set on the server e.g. 
try:
	upload_base = os.environ['UPLOAD_BASE']
except:
	upload_base= results_folder

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

batch_sorting_phase2(batch_folders,results_folder,upload_base)
