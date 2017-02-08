import os,sys,shutil,glob
for batch in open('open_batches.txt'):
	batch=batch.strip()
	old_path=glob.glob('/storage/boinc/upload/*/batch'+batch)
	if len(old_path)>0:
		old_path=old_path[0]
		new_path='/storage/boinc/upload/batch_'+batch+'/successful'
		print 'make dir and make writable ','/storage/boinc/upload/batch_'+batch
		os.makedirs('/storage/boinc/upload/batch_'+batch)
		os.system('chmod 775 /storage/boinc/upload/batch_'+batch)
		print 'rename folder',old_path,new_path
		os.rename(old_path,new_path)
		print 'rename txt file',new_path+'/batch'+batch+'.txt.gz',new_path+'/../batch_'+batch+'.txt.gz'
		os.rename(new_path+'/batch'+batch+'.txt.gz',new_path+'/../batch_'+batch+'.txt.gz')
