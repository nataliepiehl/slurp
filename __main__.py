#!/usr/bin/env python
#
# Northwestern University - Gate Lab
# Natalie Piehl
# 2022-02-03
#
# Generate slurm job script for a given analysis:subanalysis
# Execute from project root as 'python3 slurp <analysis> <subanalysis> <args>'
#
# ------------------------------------------------------------------------------
# Initialization

# Import modules
import argparse
import os
from datetime import datetime
from params import analysis_params, subanalysis_params, script_params

# Record date and time
print("\n", datetime.now())
date = datetime.now().strftime("%Y_%m_%d")
time = datetime.now().strftime("%H_%M_%S")

# ------------------------------------------------------------------------------
# Handle command line arguments

# Organize command line arguments
parser = argparse.ArgumentParser(description='Submit slurm job')
parser.add_argument('analysis', type=str,
                    help='Name of parent analysis to run')
parser.add_argument('subanalysis', type=str,
                    help='Name of sub analysis to run')
parser.add_argument('-a', '--account', type=str, default='',
                    help='Name of account to use; Default=p31535')
parser.add_argument('-p', '--partition', type=str, default='',
                    help='Partition type to use; options: short, normal, long; Default=normal')
parser.add_argument('-n', '--threads', type=int, default=0,
                    help='Number of threads to use if analysis has multithreading functionality; Default=1')
parser.add_argument('-m', '--mem', type=int, default=0,
                    help='Number of GB of RAM memory needed; Default=2')
parser.add_argument('-t', '--time', type=int, default=0,
                    help='Number of hours needed; Default=1')
parser.add_argument('-s', '--script', type=str, default='',
                    help='Language of script; Default=R')
parser.add_argument('-o', '--modules', nargs = '+', type=str, default=[''],
                    help='Additional modules to load; Default=None')
parser.add_argument('-c', '--condaenv', type=str,
                    help='Specify conda environment to load; Default=None')
parser.add_argument('-d', '--dryrun', action='store_true',
                    help='Execute a dryrun (check for file paths and create job file without submitting)')
args = parser.parse_args()

# Set dictionaries of pseudo defaults and manual defaults
defaults = vars(parser.parse_args(['', '']))
manual_defaults = {'account': 'p31535',
                   'partition': 'short',
                   'threads': 1,
                   'mem': 2,
                   'time': 1,
                   'script': 'R',
                   'modules': [''],
                   'condaenv': ''}
print(f"-----------------------------------------")

# ------------------------------------------------------------------------------
# Handle final parameters

param_units = {
    'account' : '',
    'threads' : 'threads',
    'mem' : 'GB',
    'time' : 'hour(s)',
    'script' : '',
    'condaenv': '',
}

# Function to assign parameters
def assign_param(param):
    # Check if param other than pseudo default was provided, if so move on
    if getattr(args, param) != defaults[param]:
        print(f"------ {param}: {getattr(args, param)} {param_units[param]} (user-provided)")
    else:
        # Try setting to subanalysis specific value
        try:
            setattr(args, param, subanalysis_params[args.analysis][args.subanalysis][param])
            print(f"------ {param}: {getattr(args, param)} {param_units[param]} (subanalysis specific)")
        except:
            # Else try setting to analysis specific value
            try:
                setattr(args, param, analysis_params[args.analysis][param])
                print(f"------ {param}: {getattr(args, param)} {param_units[param]} (analysis specific)")
            # Else set to default
            except:
                setattr(args, param, manual_defaults[param])
                print(f"------ {param}: {getattr(args, param)} {param_units[param]} (default)")
    return None

# Function to assign partition
def assign_partition():
    # Check if param other than pseudo default was provided, if so move on
    if getattr(args, 'partition') != defaults['partition']:
        print(f"------ partition: {args.partition} (user-provided)")
    # Check if account is b1042 to set to genomics
    elif args.account == 'b1042':
        setattr(args, 'partition', 'genomics')
        print(f"------ partition: {args.partition} (b1042 specific)")
    # Assign partition based on amount of time required
    else:
        if args.time <= 4:
            setattr(args, 'partition', 'short')
        elif args.time <= 48:
            setattr(args, 'partition', 'normal')
        else:
            setattr(args, 'partition', 'long')
        print(f"------ partition: {args.partition} (time specific)")
    return None

# Function to assign modules
def assign_modules():
    # Extract script specific modules
    script_modules = script_params[args.script]['modules']
    # Check if param other than pseudo default was provided, if so move on
    if getattr(args, 'modules') != defaults['modules']:
        setattr(args, 'modules', script_modules + args.modules)
        print(f"------ modules: {args.modules} (user-provided)")
    else:
        # Try setting to subanalysis specific value
        try:
            setattr(args, 'modules', script_modules + subanalysis_params[args.analysis][args.subanalysis]['modules'])
            print(f"------ modules: {args.modules} (subanalysis specific)")
        except:
            # Else try setting to analysis specific value
            try:
                setattr(args, 'modules', script_modules + analysis_params[args.analysis]['modules'])
                print(f"------ modules: {args.modules} (analysis specific)")
            # Else set to default
            except:
                setattr(args, 'modules', script_modules + manual_defaults['modules'])
                print(f"------ modules: {args.modules} (default)")
    return None

# Assign parameters
print(f"Parameters for current {args.analysis}-{args.subanalysis} job:\n")
assign_param('account')
assign_param('threads')
assign_param('mem')
assign_param('time')
assign_partition()
assign_param('script')
assign_param('condaenv')
assign_modules()
print("")

# ------------------------------------------------------------------------------
# Establish dirs and paths

# Generate paths
job_dir = os.path.join('slurp', 'jobs')
job_path = os.path.join(job_dir, f"{args.analysis}-{args.subanalysis}.sh")
log_dir = os.path.join('logs', args.analysis, args.subanalysis, date)
script_path = os.path.join('code', args.analysis, args.subanalysis, f"{args.analysis}-{args.subanalysis}{script_params[args.script]['file_ext']}")

# Check for existance of log dir, job_dir, and script file
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)
if not os.path.isdir(job_dir):
    os.makedirs(job_dir)                           
if not os.path.exists(script_path):
    print(f"Uh oh! Looks like we can't find the expected script: {script_path}\n",
          f"Please name and localize the script as shown above and try again\n")
    exit()

# ------------------------------------------------------------------------------
# Generate slurm batch file

# Write job script
with open(job_path, 'w') as f:
    # Write slurm parameters
    f.writelines("#!/bin/bash\n")
    f.writelines(f"#SBATCH --account {args.account}\n")
    f.writelines(f"#SBATCH --partition {args.partition}\n")
    f.writelines(f"#SBATCH --job-name {args.analysis}-{args.subanalysis}\n")
    f.writelines(f"#SBATCH --nodes 1\n")
    f.writelines(f"#SBATCH --ntasks-per-node {args.threads}\n")
    f.writelines(f"#SBATCH --mem {args.mem}GB\n")
    f.writelines(f"#SBATCH --time {args.time}:00:00\n")
    f.writelines(f"#SBATCH --output {log_dir}/{time}_oe%j.log\n")
    f.writelines(f"#SBATCH --verbose\n\n")

    # Write datetime
    f.writelines(f"echo '{date}-{time}'\n\n")

    # Write module loading
    f.writelines(f"module purge\n")
    if args.condaenv == '':
        f.writelines(f"module load {' '.join([str(mod) for mod in args.modules])}\n\n")
    else:
        f.writelines(f"module load python-miniconda3/4.10.3\n")
        f.writelines(f"source activate {args.condaenv}\n")

    # Write script execution
    f.writelines(f"{script_params[args.script]['runner']} {script_path}\n\n")

    # Print copy of script to log
    f.writelines(f"log_path=`ls {log_dir}/{time}_oe*.log`\n\n")
    f.writelines(f"echo -en '\n\n\n\n\n' >> $log_path\n")
    f.writelines(f"echo '{'-' * 65}' >> $log_path\n")
    f.writelines(f"echo 'START OF ANALYSIS SCRIPT' >> $log_path\n")
    f.writelines(f"cat {script_path} >> $log_path\n")


    # Print copy of slurm batch file to log
    f.writelines(f"echo -en '\n\n\n\n\n' >> $log_path\n")
    f.writelines(f"echo '{'-' * 65}' >> $log_path\n")
    f.writelines(f"echo 'START OF SLURM BATCH SCRIPT' >> $log_path\n")
    f.writelines(f"cat {job_path} >> $log_path\n")

# Execute job
try:
    if args.dryrun:
        print("Dry run successful")
    else:
        os.system(f"sbatch {job_path}")
    print("")
except:
    print(f"Uh oh! The job failed to execute. Please check that the job file at {job_path} is correct.")
    exit()