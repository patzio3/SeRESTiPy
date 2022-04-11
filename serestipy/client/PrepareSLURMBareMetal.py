#!/usr/bin/env python
import os
import sys
import string
import random
import subprocess

if __name__ == "__main__":
    len_string = 10
    ran = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=len_string))
    nContainer = sys.argv[1] if len(sys.argv) >= 2 else "24"
    time = sys.argv[2] if len(sys.argv) >= 3 else "7"
    partition = sys.argv[3] if len(sys.argv) >= 4 else "LYRA2"
    ncpu = sys.argv[4] if len(sys.argv) >= 5 else "4"
    memory = sys.argv[5] if len(sys.argv) >= 6 else "20000"
    email = sys.argv[6] if len(sys.argv) >= 7 else ""
    port = sys.argv[7] if len(sys.argv) >= 8 else 5000
    job_file = os.path.join(os.getcwd(), "sbatch_script_swarm" + str(ran))
    with open(job_file, "w") as fh:
        fh.writelines("#!/bin/bash\n")
        fh.writelines("#SBATCH --job-name=worker-launcher\n")
        fh.writelines("#SBATCH --output=output.slurm\n")
        fh.writelines(f"#SBATCH --time={time}-00:00:00\n")
        fh.writelines(f"#SBATCH --mem={memory}\n")
        fh.writelines("#SBATCH --mail-type=failed,end\n")
        #fh.writelines(f"#SBATCH --mail-user={email}\n")
        fh.writelines(f"#SBATCH --ntasks-per-node={ncpu}\n")
        fh.writelines(f"#SBATCH --partition {partition}\n")
        fh.writelines("LOCALTMP=/scratch/p_esch01/$SLURM_JOB_ID\n")
        fh.writelines("export DATABASE_DIR=/WORK/p_esch01/scratch_calc/test\n")
        fh.writelines("BACKDIR=$SLURM_SUBMIT_DIR\n")
        fh.writelines("cd $BACKDIR\n")
        fh.writelines("if [ ! -e $LOCALTMP ]\n")
        fh.writelines("then\n")
        fh.writelines("mkdir -p $LOCALTMP\n")
        fh.writelines("fi\n")
        fh.writelines("rsync -avu * $LOCALTMP/ \n")
        fh.writelines("echo $HOSTNAME:$LOCALTMP > LOCALDIR \n")
        fh.writelines("cd $LOCALTMP \n")        
        fh.writelines("ip=$(hostname -I | awk '{print $1}'):"+str(port)+"\n")
        fh.writelines("touch /WORK/p_esch01/scratch_calc/test/IPS/$ip\n")
        fh.writelines("touch /WORK/p_esch01/scratch_calc/test/JOBIDS/$SLURM_JOB_ID\n")
        fh.writelines("source /WORK/p_esch01/progs/serenity_AMD_EPR/serenity.sh\n")
        fh.writelines(f"export OMP_NUM_THREADS={ncpu}\n")
        fh.writelines(f"export SERENITY_MEMORY={memory}\n")
        fh.writelines(f"python /WORK/p_esch01/progs/restApi/serestipy/api/Api.py {str(port)} > launcher_"+str(ran)+".out 2>error_"+str(ran)+"\n")
        fh.writelines("cd $BACKDIR \n")
        fh.writelines('rsync -avu $LOCALTMP/* $BACKDIR/ && rm -rf $LOCALTMP && echo "$LOCALTMP deleted" >>LOCALDIR \n')
    filename = os.path.join("/WORK/p_esch01/progs/restApi/src/client/", job_file)
    os.system(f"sbatch {filename}")
