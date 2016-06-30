#!/usr/bin/env python2.7
import os, sys, time,glob


def main():
	print time.strftime("%Y/%m/%d %H:%M:%S") + " Starting batch_sorting_phase1.py\n"

        incoming_folder='../upload'
        batches_folder= '.'
        results_folder='../results'
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
            os.mkdir(results_folder)
        if not os.path.exists(results_folder+'/unknown_batches'):
            os.mkdir(results_folder+'/unknown_batches')

        # Loop over zip files in incoming folder
        for fpath in glob.glob(incoming_folder+'/*.zip'):
            fname=os.path.basename(fpath)
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
            workunit_name=fname_out[:-len(str_split[-1])-1] # workunit name is nname without the '_1.zip'
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
            # Delete this file
                os.remove(fpath)
                print 'deleting from closed batch',fname,batch
            else:
                    os.rename(fpath,results_folder+'/unknown_batches/'+fname)
                    print fname,'unknown batch'
	
#####################

main()
