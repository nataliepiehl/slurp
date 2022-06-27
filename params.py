#!/usr/bin/env python
# ------------------------------------------------------------------------------
# -----                                                                    -----
# -----                           Gate Lab                                 -----
# -----                     Northwestern University                        -----
# -----                                                                    -----
# ------------------------------------------------------------------------------
#
# Date: 05-02-2022
# Written by: Natalie Piehl
# Summary: Save custom parameters for running jobs via slurm on Quest
#
# ------------------------------------------------------------------------------
#
# Write out custom parameters for parent and sub analyses
# Default values:
# ------ account: p31535 
# ------ threads: 1 threads
# ------ mem: 2 GB
# ------ time: 1 hour(s)
# ------ partition: short 
# ------ script: R    
# ------ condaenv:  
# ------ modules: \['R/4.1.1', ''] 

# Write out custom parameters for each parent analysis
parent_params = {
    'example_analysis': {
        'account': 'b1042',
        'partition': 'normal',
        'script': 'python'
        'mem': 64,
        'time': 4,
        'threads': 1,
        'modules': ['sratoolkit/3.0.0'],
        'condaenv': './env/snapatac_env',
    },
    'your_analysis': {
         # Your parameters go here
    },
}

# Write out custom parameters for each sub analysis
sub_params = {
    'clustering': { # This is specifying the parent analysis
        'supervised': { # This is specifying the sub analysis
          'modules': ['hdf5/1.8.15-serial']
        }
    },
}

# ------------------------------------------------------------------------------
# SPe

# Write out script running parameters
script_params = {
    'R': {
        'file_ext': ".R",
        'runner': "Rscript",
        'modules': ["R/4.1.1"]
    },
    'python': {
        'file_ext': ".py",
        'runner': "python3",
        'modules': ["python/3.8.4"]
    },
    'bash': {
        'file_ext': ".sh",
        'runner': "bash",
        'modules': []
    }
}
