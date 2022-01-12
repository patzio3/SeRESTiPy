#!/usr/bin/env python
import os, sys, string, random, subprocess
     
if __name__ == "__main__":
    len_string = 10 
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = len_string))
    nContainer = sys.argv[1] if len(sys.argv) >= 2 else "24"
    time = sys.argv[2] if len(sys.argv) >= 3 else "4"
    partition = sys.argv[3] if len(sys.argv) >= 4 else "LYRA2"
    ncpu = sys.argv[4] if len(sys.argv) >= 5 else "4"
    memory = sys.argv[5] if len(sys.argv) >= 6 else "20000"
    email = sys.argv[6] if len(sys.argv) >= 7 else ""
    job_file = os.path.join(os.getcwd(), "sbatch_script_swarm" + str(ran))
    with open(job_file, "w") as fh:
        fh.writelines("#!/bin/bash\n")
        fh.writelines("#SBATCH --job-name=worker-launcher\n")
        fh.writelines("#SBATCH --output=output.slurm\n")
        fh.writelines(f"#SBATCH --time={time}:00:00\n")
        fh.writelines(f"#SBATCH --mem=1\n")
        fh.writelines(f"#SBATCH --exclusive\n")
        fh.writelines("#SBATCH --mail-type=failed,end\n")
        fh.writelines(f"#SBATCH --mail-user={email}\n")
        fh.writelines(f"#SBATCH --ntasks-per-node=1\n")
        fh.writelines(f"#SBATCH --partition {partition}\n")
        fh.writelines("LOCALTMP=/scratch/p_esch01/$SLURM_JOB_ID\n")
        fh.writelines("export DATABASE_DIR=/WORK/p_esch01/scratch_calc\n")
        fh.writelines("BACKDIR=$SLURM_SUBMIT_DIR\n")
        fh.writelines("cd $BACKDIR\n")
        fh.writelines("if [ ! -e $LOCALTMP ]\n")
        fh.writelines("then\n")
        fh.writelines("mkdir -p $LOCALTMP\n")
        fh.writelines("fi\n")
        fh.writelines("rsync -avu * $LOCALTMP/ \n")
        fh.writelines("echo $HOSTNAME:$LOCALTMP > LOCALDIR \n")
        fh.writelines("cd $LOCALTMP \n")
        fh.writelines(f"sudo -H -u p_esch01 bash -c '/WORK/p_esch01/progs/anaconda3/bin/python3 DockerSDK.py {ncpu} {memory} {nContainer} > launcher_"+str(ran)+".out 2>error_"+str(ran)+"'\n")
        fh.writelines("cd $BACKDIR \n")
        fh.writelines('rsync -avu $LOCALTMP/* $BACKDIR/ && rm -rf $LOCALTMP && echo "$LOCALTMP deleted" >>LOCALDIR \n')
        #fh.writelines("rm -rf /WORK/p_esch01/scratch_calc/* \n")
    filename = os.path.join("/WORK/p_esch01/progs/restApi/src/client/",job_file)
    os.system(f"sbatch {filename}")
