# Utility for running snakemake on SLURM

## Features
- Keeps track of running SLURM jobs
- Ends SLURM jobs when cancelling the script
- Saving job logs in `logs/` subdirectory
- Allows specifying `threads`, `mem_mb` and `gpu` resources

## Usage
1) Copy `run_slurm_jobs`, `slurm_status.py`, `slurm-status.sh` and `slurm-sidecar.py` into any directory in your $PATH.
   Make sure that all files are in the same directory.
2) Simply replace your `snakemake <additional args>` call with `run_slurm_jobs <additional args>`

Examples:
- `run_slurm_jobs.sh --rerun-incomplete --restart-times 3 -k`
- It is possible to change slurm arguments and number of total cores on the command line:
  `SNAKEFILE="scripts/Snakefile" N_CORES=256 SBATCH_ARGS="--partition=urgent --exclude=ouga04" run_slurm_jobs.sh --rerun-incomplete -k`

