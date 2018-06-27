#!/usr/bin/env python

"""
 Name: performance_and_testing.py
 Author: Divya Jaganathan
 Date:  26 June, 2018

 Version 1:
 Single script to run the executable iteratively over a sequence of processor_num 
 and for num_samples_per_procnum times for each processor_num, resulting in:
 1. Performance Curve Figure stored in /Figures
 2. Data stored in data_<mc>_<timestamp>.txt

NOTE(s):1. YOU MUST LOAD THE NECESSARY MODULES BEFOREHAND: metis and OpenMPI
        2. YOU MUST ALLOCATE THE RESOURCES BEFORE RUNNING THIS SCRIPT

"""

import subprocess
import numpy as np
import re
import matplotlib.pyplot as plt
import datetime


# Getting present runtime timestamp: To be written in data and for file names
timenow=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# -------

nprocs_max = 32
niter = int (np.log2(nprocs_max))
nsamples_per_procnum = 3

time=np.zeros(shape=(1,niter))
procs=np.zeros(shape=(1,niter))

i=nprocs_max
j=niter

writefilename="data_gr_"+timenow+".txt"
fw=open(writefilename,'a+')
fw.write('Time is: %s \n Format: #Procs|Sample Runs|Average \n' % timestamp)

while i > 1:

        sample=nsamples_per_procnum
        foldername="perf_p"+str(i)+"_gr_openmpi"
        subprocess.check_call(['mkdir',foldername])
        fw.write('%s \t' % i)
        sum=0

        while sample >= 1:

                # Generate the log and graph files

                subprocess.check_call(['./metis','graph.info',str(i)])
                print "\n"
                print "------------------------------------"
                print "******" +str(i) +"/"+str(sample)+ " METIS done******"
                print "------------------------------------"
                print "\n"
                subprocess.check_call(['mpirun','-n',str(i),'./ocean_model'])
                print "\n"
                print "--------------------------------------"
                print "******" +str(i) + " MPI Run done******"
                print "--------------------------------------"
                print "\n"

		# Search for time integration and write to a file
                fr=open("log.ocean.0000.out",'r')

                for line in fr:
                        m=re.search("2  time integration",line)
                        if m:
                                numbers=line.split("integration",1)[1]
                                first_number=numbers.split()[0]
                                fw.write('%s \t' % first_number)
                                sum=sum+float(first_number)

                fname="log_p"+str(i)+"_s"+str(sample)
                filepath=foldername+"/"+fname
                subprocess.check_call(['mv','log.ocean.0000.out',filepath])
                sample=sample-1

        average=sum/nsamples_per_procnum
        time[0][j-1]=average
        procs[0][j-1]=i
        fw.write('%s \n' % str(average))
        i=i/2
        j=j-1

fw.close()
fr.close()

# Converting data to SYPD

subprocess.check_call(['mkdir','figures'])
timestep = 20*60
steps = 6
stepsPerSec = steps/time
SYPD = stepsPerSec*timestep/365
perfect = SYPD[0][2]/procs[0][2]*procs
print perfect
print SYPD
plt.loglog(procs, SYPD, '-ko')
plt.loglog(procs, perfect, 'b-')
plt.title(r'MPAS-Ocean Performance Curve')
plt.xlabel('Number of Processors')
plt.ylabel('Simulated Years Per Day (SYPD)')
figurenamepath="figures/fig_gr"+timenow+".png"
plt.savefig(figurenamepath)

# End Version 1
