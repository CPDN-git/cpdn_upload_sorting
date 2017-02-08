# Script to move files in open batches to the incoming folder
# Paths are hard coded to match set up on anemoi.oerc (upload2)

import os,sys,shutil,glob

incoming='/storage/incoming/uploader/'

# loop over open batches
for batch in open('/home/cpdn/open_batches.txt','r'):
	batch=batch.strip()
	old_paths=glob.glob('/storage/boinc/upload/batch_'+batch+'/*/*.zip')

	for old path in old_paths:
		zipname=os.path.basename(old_path)

		print 'moving',old_path,'to',os.path.join(incoming,zipname)
		#shutil.move(old_path,os.path.join(incoming,zipname))
