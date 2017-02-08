import os,glob,gzip
for wget_file in glob.glob('/storage/boinc/upload/batch_*/batch_*.txt.gz'):
	print wget_file
	with gzip.open(wget_file, 'rb') as f_in, gzip.open(wget_file[:-7]+'_new.txt.gz', 'wb') as f_out:
		for line in f_in:
			if line.find('http://cpdn-upload2.oerc.ox.ac.uk/results/')!=-1:
				endpart=line.split('batch')[-1]
				batchstr=endpart.split('/')[0]
				f_out.write('http://upload2.cpdn.org/results/batch_'+batchstr+'/successful'+endpart[len(batchstr):])
			else:
				f_out.write(line.replace('/storage/boinc/upload/','http://upload2.cpdn.org/results/'))	
	os.remove(wget_file)
	os.rename(wget_file[:-7]+'_new.txt.gz',wget_file)
