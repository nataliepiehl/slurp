# slurp
Tool for running jobs on Quest via SLURM

## How to use slurp
From project root on Quest (accessed through `ssh -X <netID>@quest.northwestern.edu`), execute `python3 slurm --help` to see job submission options and guidelines.

The expected execution format is `python3 slurm <analysis_name> <subanalysis_name> <additional_parameters>` where the script being run is stored at `code/<analysis_name>/<subanalysis_name>/<analysis_name>-<subanalysis_name>.R`

I.e. use `python3 slurm test slurm_test -m 1 -n 1 -t 1` to run the test file `code/test/slurm_test/test-slurm_test.R` with 1GB of RAM, 1 node, and 1 hour of time.

Analysis or subanalysis specific paramters can be saved in `slurm/params.py` to avoid manually specifying the above parameters every time.

Default values are as follows:  
- p31535 account  
- short partition  
- 1 thread  
- 2GB memory  
- 1 hour  
