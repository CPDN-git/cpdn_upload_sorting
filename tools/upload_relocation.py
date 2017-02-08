#!/usr/bin/env python2
import os, sys, time, glob, urllib2
import xml.etree.ElementTree as ET
import shutil

dl_path='http://climateapps2.oerc.ox.ac.uk/batch'
batch_server={}

batchxml=ET.parse(urllib2.urlopen(dl_path+'/batches.xml')).getroot()
for batch in batchxml.findall('batch'):
	batchid=int(batch.attrib['id'])
	batch_server[batchid]=batch.find('server_cgi').text.lower()
	
for batchdir in glob.glob('/storage/boinc/upload/*/batch_???'):
	try:
		batchid=int(batchdir.split('_')[-1])
		server=batch_server[batchid]
		if server=='http://upload2.cpdn.org/cgi-bin/':
			#print batchdir+'/*/*/*.zip'
			#failed_dir=batchdir+'/failed'
			#if os.path.exists(failed_dir):
			#	shutil.rmtree(failed_dir) 
			os.system('rsync --remove-source-files -v '+batchdir+'/*/*/*.zip phys0924@cpdn-ppc01.oerc.ox.ac.uk:/gpfs/projects/cpdn/storage/incoming/uploader')
	except:
		print "Error ",batchid
