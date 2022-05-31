#!/usr/bin/env python
#
# Northwestern University - Gate Lab
# Natalie Piehl
# 2022-05-02
#
# ------------------------------------------------------------------------------
# Write out custom parameters
# Default values:
#  ------ p31535 account
#  ------ short partition
#  ------ 1 thread(s)
#  ------ 2GB memory
#  ------ 1 hour(s)

# Write out custom parameters for each analysis
analysis_params = {
    'de': {
        'threads': 1,
        'mem': 64,
    },
    'sratoolkit': {
        'modules': ['sratoolkit/3.0.0'],
        'mem': 64,
        'time': 4,
    },
    'snapatac': {
        'condaenv': './env/snapatac_env',
    }
}

# Write out custom parameters for each subanalysis
subanalysis_params = {
    'clustering': {
        'supervised': {
          'modules': ['hdf5/1.8.15-serial']
        }
    },
}

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
