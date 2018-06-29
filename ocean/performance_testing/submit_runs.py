#!/usr/bin/env python

"""
Kevin Rosa
June 29, 2018
Los Alamos National Laboratory

"""
import subprocess as sp
import datetime
import os

from cluster_info import cluster_info
from gen_batch_script import gen_batch_script

# ---------
# Variables to set:
cluster_name = 'grizzly'
cores_count_array = [32, 128, 512, 2048, 8192, 32768]
iterations_count = 5  # number of runs per core count
qos = 'standby'
# directory where ocean_model, streams.ocean, namelist.ocean, metis, and graph.info are stored:
top_level = '/lustre/scratch2/turquoise/kanga/mpas_ocean_runs/MPAS-O_V6.0_test_cases/MPAS-O_V6.0_QU240/'
# ---------

# current time will be used as a unique identifier to avoid overwriting
time_str = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
# returns cluster info in a dict
cluster = cluster_info(cluster_name)

all_out_fnames = []  # this will store the names of each output file 

for cores_count in cores_count_array:
    
    # make directory for processor count (will store graph.info.N)
    exp_dir = os.path.join(top_level, 'np'+str(cores_count))
    if not os.path.exists(exp_dir):
        os.makedirs(exp_dir)
    
    # change directory and generate graph.info.N
    os.chdir(exp_dir)
    sp.check_call('ln','-isf', os.path.join(top_level,'graph.info'), os.path.join(exp_dir,'.'))
    sp.check_call('cp','-d', os.path.join(top_level,'metis'), os.path.join(exp_dir,'.'))
    sp.check_call(['./metis', 'graph.info', str(cores_count)])
    
    
    # each iteration (job) gets its own job_dir and batch script
    for iteration in range(iterations_count): 
        
        job_name = '_'.join((cluster_name, 
                             'np'+str(cores_count), 
                             time_str, 
                             'run'+str(iteration)))
        
        # make job_dir 
        job_dir = os.path.join(exp_dir, job_name)
        if not os.path.exists(job_dir):
            os.makedirs(job_dir)
        
        batch_fname = os.path.join(job_dir, job_name+'.sh')
        out_fname = os.path.join(job_dir, job_name+'.out')
        
        # generate batch script
        gen_batch_script(execut_fname='./ocean_model',
                         batch_fname=batch_fname,
                         out_fname=out_fname, 
                         job_name=job_name,
                         cores_count=cores_count, 
                         qos=qos,
                         cores_per_node=cluster['cores_per_node'],
                         module_str=cluster['module_str'],
                         hardware_constraint=cluster['hardware_constraint']
                         )
        
        # link streams and namelist files to job_dir
        sp.check_call('ln','-isf', os.path.join(top_level,'streams.ocean'), os.path.join(job_dir,'.'))
        sp.check_call('ln','-isf', os.path.join(top_level,'namelist.ocean'), os.path.join(job_dir,'.'))
        
        # change directory and submit the job
        os.chdir(job_dir)
        sp.check_call('sbatch',batch_fname)
        
        # store output filename for later
        all_out_fnames.append(out_fname)

