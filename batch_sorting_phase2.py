#!/usr/bin/env python2.7
import os, sys, time, glob, gzip


def main():
	print time.strftime("%Y/%m/%d %H:%M:%S") + " Starting batch_sorting_phase2.py\n"

	batches_folder= '.'
	results_folder='/storage/boinc/projects/cpdnboinc_dev/results'
	# TODO, for upload servers that are publically accessible, this should be a url e.g. 
	# UPLOAD_BASE = 'http://upload2.cpdn.org/results'
	# maybe address this as an environment variable set on the server e.g. 
	try:
		upload_base = os.environ['UPLOAD_BASE']
	except:
		upload_base= results_folder
	# First rsync files accross and load open and closed batches
	projects={}
	#projects['cpdn']='http://climateapps2.oerc.ox.ac.uk/batch/batches.xml'
	projects['cpdn_dev']='http://vorvadoss.oerc.ox.ac.uk/cpdnboinc_dev/download/batch_lists/'
	open_batches=[]
	closed_batches=[]
	for proj,url in projects.iteritems():
		dl_path = batches_folder+'/'+proj+'/'
		# TODO Rsync folder across to dl_path

		# Create lists of open and closed batches from this project
		for batch in open(dl_path+'open_batches.txt'):
			open_batches.append(batch.strip())
		for batch in open(dl_path+'closed_batches.txt'):
			closed_batches.append(batch.strip())

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
		if batch in open_batches:
			print "Sorting batch",batch
			# Get lists of successful and failed tasks
			successful_tasks=[]
			failed_tasks=[]
			for proj in projects.keys():
				try:
					for task in open(batches_folder+'/'+proj+'/batch_'+batch+'_successful_wus'):
						successful_tasks.append(task.strip())
					for task in open(batches_folder+'/'+proj+'/batch_'+batch+'_failed_wus'):
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
					#TODO check if the number of results are correct (from batches.xml ul_files)
					print in_progress_task,'to',os.path.join(success_folder,taskname)
					os.rename(in_progress_task,os.path.join(success_folder,taskname))
                                        # Write list of output files to f_success text file
					for zipname in glob.glob(os.path.join(success_folder,taskname,'*')):
						f_success.write(upload_base+zipname[len(results_folder):]+'\n')
				elif taskname in failed_tasks:
					print in_progress_task,'to',os.path.join(failed_folder,taskname)
					os.rename(in_progress_task,os.path.join(failed_folder,taskname))
			f_success.close()

		elif batch in closed_batches:
			print "batch",batch,"is already closed, skipping"
			#TODO, could put in clean up of in_progress and failed workunits here. 
		else:
			print "batch",batch,"is unknown"

#####################

main()
