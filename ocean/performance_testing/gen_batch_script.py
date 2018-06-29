# -*- coding: utf-8 -*-
def main():
    import datetime
    time_str = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    fname = 'batch_test'+time_str+'.sh'
    
    gen_batch_script(batch_fname=fname, module_str='module load ecjoi', cores_count=90, cores_per_node=16)

# https://github.com/divya-jaganathan/MPAS-Tools/tree/ocean_performance_testing/ocean/performance_testing
def gen_batch_script(
        execut_fname='ocean_model',  # path to executable file
        batch_fname='batch_test.sh',
        out_fname='newjob.out', 
        job_name='newjob',  # this determines output file name too
        module_str='',
        cores_count=1,
        cores_per_node=16,
        hardware_constraint='',
        time='1:00:00',
        qos='regular'
        ):
    """
    Construct batch script.
    This function accepts keyword arguments.
    
    Kevin Rosa
    June 26, 2018
    Los Alamos National Laboratory
    """
    import math
    
    # calculations
    nodes_count = int(math.ceil(float(cores_count)/float(cores_per_node)))
    
    # SBATCH options specified for all runs
    output = '\n'.join((
            "#! /bin/bash",
            "#SBATCH --partition=regular",
            "#SBATCH --nodes="+str(nodes_count),
            "#SBATCH --time="+time,
            "#SBATCH --job_name="+job_name,
            "#SBATCH --output="+out_fname,
            "#SBATCH --qos="+qos,
            "#SBATCH --license=SCRATCH"
            ))
    
    # append a hardware constraint if given
    if not hardware_constraint == '':
        output = '\n'.join((
                output,
                "#SBATCH --constraint="+hardware_constraint
                ))    
    
    # append module loading
    output = '\n'.join((
            output,
            '',
            module_str
            ))
    
    # append srun command
    output = '\n'.join((
            output,
            '',
            "srun --ntasks="+str(cores_count)+' '+execut_fname
            ))
    
    # write to file
    with open(batch_fname, 'w') as batch_file:
        batch_file.write(output)


if __name__ == '__main__':
    main()