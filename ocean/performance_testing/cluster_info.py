#!/usr/bin/env python2
# -*- coding: utf-8 -*-
def cluster_info(cluster_name):
    """
    Returns a dict with 3 keys: 
        cores_per_node, hardware_constraint, and module_str.
        
    Kevin Rosa
    June 27, 2018
    Los Alamos National Laboratory
    """
    
    # convert cluster_name to lowercase so don't get case-sensitive issues
    cluster_name = cluster_name.lower()
    
    if cluster_name == 'grizzly':
        
        cores_per_node = 36
        hardware_constraint = ''
        module_str = ("module use /usr/projects/climate/SHARED_CLIMATE/modulefiles/all\n"
                      "module load python/anaconda-2.7-climate\n"
                      "module load gcc/5.3.0 openmpi/1.10.5 netcdf/4.4.1 parallel-netcdf/1.5.0 pio/1.7.2\n")
        
    elif cluster_name == 'edison':
        
        cores_per_node = 24
        hardware_constraint = ''
        module_str = "module load /global/project/projectdirs/acme/software/modulefiles/all/e3sm-unified/1.1.3"
    
    elif cluster_name == 'cori-knl':
        
        cores_per_node = 68
        hardware_constraint = 'knl'
        module_str = ""
        
    elif cluster_name == 'cori-haswell':
        
        cores_per_node = 32
        hardware_constraint = 'haswell'
        module_str = ""
        
    else:
        raise ValueError('Must use a valid cluster name')
        
    
    return {'cores_per_node':cores_per_node,
            'hardware_constraint':hardware_constraint,
            'module_str':module_str}
 
    
