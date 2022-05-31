from setuptools import setup, find_packages

setup(
    name='slurp',
    version='0.1.0',    
    description='A tool for submitting slurm jobs on Quest',
    url='https://github.com/gatelabNW/slurp',
    author='Natalie Piehl',
    author_email='natalie.piehl@northwestern.edu',
    license='MIT',
    packages=find_packages(where="src"),
    install_requires=['argparse',
                      'datetime',
                      'os',                     
                      ],
)
