# slurp
`slurp` is a tool to quickly submit jobs to Quest without manually creating an sbatch script every time.

`slurp` is dependent on the following project/repo structure:

```
project
│
└───code
│   └───parent_analysis_1
│       └──sub_analysis_1
│           │ parent_analysis_1-sub_analysis_1.R
│   └───parent_analysis_2
│       └──sub_analysis_2
│           │ parent_analysis_2-sub_analysis_2.py
│
└───logs
│
└───slurp
```

`slurp` MUST be parallel to the `code` and `logs` folders. Scripts must be stored within the parent and sub analysis folder structure and named `<parent>-<sub>.R/py/sh` in order to run. 

## How to add slurp as a submodule to a git repo

Navigate into the root of your repo and execute the following:

```
git submodule add https://github.com/gatelabNW/slurp.git
```

## How to update slurp within a git repo

Navigate into the root of your repo and execute the following:

```
 git submodule update --remote
```

## How to use slurp
1) Navigate to your project root on Quest (accessed through `ssh -X <netID>@quest.northwestern.edu`)

2) Execute `python3 slurp --help` to see job submission options/guidelines and confirm proper installation.

+ `slurp` assumes the script is in `R` unless otherwise specified with `--script/-s`

3) Run your script using the following format: `python3 slurp <parent_analysis> <sub_analysis> <additional_parameters>` 

+ Example: `python3 slurp test slurm_test -m 1 -n 1 -t 1` runs the file `code/test/slurm_test/test-slurm_test.R` with 1GB of RAM, 1 node, 1 hour of time, and remaining default parameters.

+ Analysis or subanalysis specific paramters can be saved in `slurp/params.py` to avoid manually specifying the above parameters every time; examples shown within script.

  + The user can also be specified in `slurp/params.py` so it is written to each job log

+ Default values are as follows:  
------ account: p31535  
------ threads: 1 threads  
------ mem: 2 GB  
------ time: 1 hour(s)  
------ partition: short  
------ script: R   
------ condaenv:    
------ modules: \['R/4.1.1', '']  
