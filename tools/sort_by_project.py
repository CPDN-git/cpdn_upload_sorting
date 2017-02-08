#!/usr/bin/env python2
import os, sys, time, glob, urllib2, zipfile, shutil
import xml.etree.ElementTree as ET

dl_path='http://climateapps2.oerc.ox.ac.uk/batch'
batch_projects={}

batchxml=ET.parse(urllib2.urlopen(dl_path+'/batches.xml',"r")).getroot()
for batch in batchxml.findall('batch'):
	batchid=int(batch.attrib['id'])
	print batchid
	batch_projects[batchid]=batch.find('project').text.lower()
	
for batchdir in glob.glob('/storage/boinc/upload/batch_*'):
	try:
		batchid=int(batchdir.split('_')[-1])
		proj=batch_projects[batchid]
		print batchdir,batchid,proj
		projdir='/storage/boinc/upload/'+proj
		if not os.path.exists(projdir):
			os.mkdir(projdir)
		#shutil.move(batchdir,projdir)
		os.system('rsync -ru '+batchdir+' '+projdir)
	except Exception,e:
		print e
		print "Couldn't sort batch ",batchid
