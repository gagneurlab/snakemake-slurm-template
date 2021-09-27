#!/usr/bin/env python3
import re
import subprocess as sp
import shlex
import sys
import time
import logging
import argparse

logger = logging.getLogger("__name__")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("slurm-status.log"),
#        logging.StreamHandler()
    ]
)

parser = argparse.ArgumentParser(description='Get the status of some slurm job.')
parser.add_argument(
    '--status_attempts',
    action='store',
    dest="status_attempts",
    type=int,
    default=20,
    help='number of attenpts to obtain cluster status'
)
parser.add_argument(
    '--cluster',
    action='store',
    dest="cluster",
    default="",
    help='cluster name'
)

parser.add_argument(
    'jobid',
    action='store',
    help='Slurm job id'
)

args = parser.parse_args()

jobid = args.jobid
STATUS_ATTEMPTS = args.status_attempts
if args.cluster != "":
    cluster = f"--cluster={args.cluster}"
else:
    cluster = ""

for i in range(STATUS_ATTEMPTS):
    # Try getting job with scontrol instead in case sacct is misconfigured
    try:
        sctrl_res = sp.check_output(
            shlex.split(f"scontrol {cluster} -o show job {jobid}")
        )
        m = re.search(r"JobState=(\w+)", sctrl_res.decode())
        res = {jobid: m.group(1)}
        m = re.search(r"Requeue=(\w+)", sctrl_res.decode())
        res["requeue"] = m.group(1)
        break
    except sp.CalledProcessError as e:
        logger.error("scontrol process error")
        logger.error(e)
        if i >= STATUS_ATTEMPTS - 1:
            print("failed")
            exit(0)
        else:
            time.sleep(1)

status = res[jobid]

if status == "BOOT_FAIL":
    logger.info(sctrl_res.decode())
    print("failed")
elif status == "OUT_OF_MEMORY":
    logger.info(sctrl_res.decode())
    print("failed")
elif status.startswith("CANCELLED"):
    logger.info(sctrl_res.decode())
    print("failed")
elif status == "COMPLETED":
    print("success")
elif status == "DEADLINE":
    logger.info(sctrl_res.decode())
    print("failed")
elif status == "FAILED":
    logger.info(sctrl_res.decode())
    print("failed")
elif status == "NODE_FAIL":
    logger.info(sctrl_res.decode())
    print("failed")
elif status == "PREEMPTED":
    logger.info(sctrl_res.decode())
    if res.get("requeue", "") == "1":
        print("running")
    else:
        print("failed")
elif status == "TIMEOUT":
    logger.info(sctrl_res.decode())
    print("failed")
# Unclear whether SUSPENDED should be treated as running or failed
elif status == "SUSPENDED":
#    print("failed")
    print("running")
else:
    print("running")
