#!/usr/bin/env python
import os, sys, string, random
     
if __name__ == "__main__":
    len_string = 10 
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = len_string))
    time = sys.argv[1] if len(sys.argv >= 2) else "4"
    partition = sys.argv[2] if len(sys.argv >= 3) else "LYRA1"
    ncpu = sys.argv[3] if len(sys.argv >= 4) else "4"
    memory = sys.argv[4] if len(sys.argv >= 5) else "48000"
    nContainer = sys.argv[5] if len(sys.argv >= 6) else "8"
    email = sys.argv[6] if len(sys.argv >= 7) else ""
    job_file = os.path.join(os.getcwd(), "sbatch_script_swarm" + str(ran))
    with open(job_file) as fh:
        fh.writelines("#!/bin/bash\n")
        fh.writelines("#SBATCH --job-name=worker-launcher\n")
        fh.writelines("#SBATCH --output=output.slurm\n")
        fh.writelines(f"#SBATCH --time={time}:00:00\n")
        fh.writelines(f"#SBATCH --mem=1\n")
        fh.writelines("#SBATCH --mail-type=failed,end\n")
        fh.writelines(f"#SBATCH --mail-user={email}\n")
        fh.writelines(f"#SBATCH --ntasks-per-node=1\n")
        fh.writelines(f"#SBATCH --partition {partition}\n")
        fh.writelines("LOCALTMP=/scratch/p_esch01/$SLURM_JOB_ID")
        fh.writelines("BACKDIR=$SLURM_SUBMIT_DIR")
        fh.writelines("cd $BACKDIR")
        fh.writelines("if [ ! -e $LOCALTMP ]")
        fh.writelines("then")
        fh.writelines("mkdir -p $LOCALTMP")
        fh.writelines("fi")
        fh.writelines("rsync -avu * $LOCALTMP/")
        fh.writelines("echo $HOSTNAME:$LOCALTMP > LOCALDIR")
        fh.writelines("cd $LOCALTMP")
        fh.writelines(f"python3 DockerSDK.py {ncpu} {memory} {nContainer}")
        fh.writelines("cd $BACKDIR")
        fh.writelines('rsync -avu $LOCALTMP/* $BACKDIR/ && rm -rf $LOCALTMP && echo "$LOCALTMP deleted" >>LOCALDIR')
        os.system(f"sbatch {job_file}")