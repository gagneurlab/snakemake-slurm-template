# Utility for running snakemake on SLURM

## Features
- Keeps track of running SLURM jobs
- Ends SLURM jobs when cancelling the script
- Saving job logs in `logs/` subdirectory
- Allows specifying `threads`, `mem_mb` and `gpu` resources

## Usage
1) Copy `run_slurm_jobs` and `slurm_status.py` to any directory in your $PATH.
   Make sure that both files are in the same directory.
2) If needed, change the `Snakefile` path in `run_slurm_jobs`
3) Simply replace your `snakemake <additional args>` call with `./run_slurm_jobs <additional args>`

Examples:
- `run_slurm_jobs.sh --rerun-incomplete --restart-times 3`
- It is possible to change slurm arguments and number of total cores on the command line:
  `SNAKEFILE="scripts/Snakefile" N_CORES=32 SBATCH_ARGS="--partition=slurm-ouga --exclude=gpu01" ./run_slurm_jobs.sh --rerun-incomplete`

