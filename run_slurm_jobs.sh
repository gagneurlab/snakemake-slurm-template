#!/bin/bash
# All the slurm arguments can be found here https://slurm.schedmd.com/sbatch.html
# https://snakemake.readthedocs.io/en/stable/executing/cli.html
# Maintainers:
#   Vangelis Theodorakis theodora@in.tum.de
#   Florian R. Hoelzlwimmer hoelzlwi@in.tum.de
#
# Fail the script if one command fails
set -e

# ============================================================================
#
# 1) Make sure that you have snakemake installed in your $PATH
#
# 2) Specify the following arguments according to your own taste
#
# 3) Run ./run_slurm_jobs.sh
#

# Use the default snakemake command determined by your $PATH
# otherwise specify absolute path to snakemake binary
snakemake="snakemake"

# Change kinit path to use system kerberos instead of potential conda
# installed versions
kinit="/usr/bin/kinit"

# The name of the snakefile
snakefile="Snakefile"

# The number of snakemake jobs
number_of_snakemake_jobs="1"

#### IMPORTANT!!!
# Make a environment variable for the project folder
# e.g. project_folder="/path/to/project/folder/"
project_folder="$(dirname $snakefile)"

# Set the log folder path
logs="$project_folder/logs"

# Set the job name for the job that will be spawned
job_names="test-job"


# ============================================================================

# By default errors and outputs are printed in the same file
# so here we store the successfull outputs as .out files
# and the errors as .error files

output_files="$logs/$job_names-%A.out"

# Create the log folder if it does not exist
if [[ ! -e $logs ]]; then
    mkdir $logs
    echo "New folder created under $logs"
else
    echo "Folder $logs was not created because it already exists..."
fi

# Clear the logs/ folder
if [ "$(ls -A $logs)" ]; then
    echo "Clear $logs from old files"
    rm $logs/*
fi

# Run the snakemake file on the cluster

# Fetch kerberos ticket that lasts for 7 days
$kinit -r 7d

# Auks argument caches the kerberos ticket for runs that last more than
# one day (otherwise the jobs lose access to the filesystem)
auks -a

$snakemake --keep-going \
           --default-resources ntasks=1 mem_mb=1000 \
           --cluster "sbatch --ntasks {resources.ntasks} \
                             --cpus-per-task {threads} \
                             --parsable \
                             --auks=done \
                             --mem {resources.mem_mb}M \
                             --output $output_files \
                             --job-name=$job_names" \
           --jobs $number_of_snakemake_jobs \
           --snakefile $snakefile $@
           # --verbose
           # --rerun-incomplete
