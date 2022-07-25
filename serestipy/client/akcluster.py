import os
import sys
import time
import functools
from serestipy.client.APICommunicator import APICommunicator


class AKCluster():
    def determineSettings(self, nSystems, partition, nCPU, nRAM):
        switcher = {
            "LYRA1": [32, 350000],
            "LYRA2": [94, 500000],
            "POOL" : [8, 32000]
        }
        maxCPU, maxRAM = switcher.get(partition.upper(),
                                      "Invalid Partition! Only LYRA1 and LYRA2 possible")
        maxWorker = (maxCPU // nCPU) if ((maxCPU // nCPU) <=
                                         maxRAM // nRAM) else (maxRAM // nRAM)
        nWorkerPerNode = nSystems if (nSystems <= maxWorker) else maxWorker
        nNodes = (nSystems // nWorkerPerNode) if (nSystems %
                                                  nWorkerPerNode == 0) else (nSystems // nWorkerPerNode + 1)
        return nCPU, nRAM, nNodes, nWorkerPerNode

    def runInDocker(self, func, nCPU, nRAM, nNodes, nWorkerPerNode, partition, days, *args):
        if (partition.upper() == "POOL"):
            print("Docker is not available on the Pool partition!!! Stopping run...")
            sys.exit()
        communicator = APICommunicator.getInstance()
        print("Cleaning left-overs...")
        ips_file = os.path.join(os.getenv('DATABASE_DIR'), "ips_hosts")
        if (os.path.exists(ips_file)):
            os.remove(ips_file)
        out_path = os.path.join(os.getenv('DATABASE_DIR'))
        for file in os.listdir(out_path):
            if (file.startswith("out")):
                os.remove(os.path.join(out_path, file))
        print("Individual worker specs: CPU "+str(nCPU)+", Memory: "+str(nRAM)+"MB with " +
              str(nWorkerPerNode)+" Worker(s) per node on "+str(nNodes)+" Node(s)...")
        print("Submitting worker launcher instances...")
        port = 5000
        for _ in range(nNodes):
            os.system("python /WORK/p_esch01/progs/restApi/serestipy/client/PrepareSLURMDocker.py " + str(nWorkerPerNode) + " " + str(days) + " " + partition + " " + str(nCPU) + " " + str(nRAM) + " lol " + str(port))
            port += 1000
        print("Wait until all of them are running...")
        while(True):
            launcher_running = os.popen(
                "squeue | grep worker-l").read().split().count('R')
            launcher_queued = os.popen(
                "squeue | grep worker-l").read().split().count('Q')
            if (launcher_queued == 0 and launcher_running == nNodes):
                break
        print("All are running! Starting containers and gather ip addresses...")
        while(True):
            if (os.path.exists(ips_file)):
                break
        old_time = os.path.getmtime(ips_file)
        time.sleep(1.0)
        while(True):
            new_time = os.path.getmtime(ips_file)
            if (new_time == old_time):
                break
            old_time = new_time
            time.sleep(1.0)
        host_addresses = []
        with open(ips_file) as handle:
            content = handle.readlines()
            for line in content:
                host_addresses.append(os.path.join(line.strip()))
        print("Read addresses\n", host_addresses)
        communicator.endpointsOnline(host_addresses)
        print("Starting calculation...")
        func(host_addresses, *args)
        print("Everything finished! Shutting down worker containers...")
        base_addresses = set()
        _ = [base_addresses.add(i[:-5] + ":5000") for i in host_addresses]
        _ = communicator.requestEvent("POST", list(base_addresses), ["" for i in range(
            len(list(base_addresses)))], ['{}' for i in range(len(list(base_addresses)))])

    def runBareMetal(self, func, nCPU, nRAM, nNodes, nWorkerPerNode, partition, days, *args):
        communicator = APICommunicator.getInstance()
        print("Cleaning left-overs...")
        out_path = os.path.join(os.getenv('DATABASE_DIR'))
        if (not os.path.exists(os.path.join(out_path, "IPS"))):
            os.mkdir(os.path.join(out_path, "IPS"))
        if (not os.path.exists(os.path.join(out_path, "JOBIDS"))):
            os.mkdir(os.path.join(out_path, "JOBIDS"))
        for file in os.listdir(out_path):
            if (file.startswith("out")):
                os.remove(os.path.join(out_path, file))
        print("Individual worker specs: CPU "+str(nCPU)+", Memory: "+str(nRAM)+"MB with " +
              str(nWorkerPerNode)+" Worker(s) per node on "+str(nNodes)+" Node(s)...")
        print("Submitting Api instances...")
        port = 5000
        for _ in range(nNodes):
            os.system("python /WORK/p_esch01/progs/restApi/serestipy/client/PrepareSLURMBareMetal.py " + str(nWorkerPerNode) + " " + str(days) + " " + partition + " " + str(nCPU) + " " + str(nRAM) + " lol " + str(port))
            port += 1
        print("Wait until all of them are running...")
        while(True):
            launcher_running = os.popen(
                "squeue | grep worker-l").read().split().count('R')
            launcher_queued = os.popen(
                "squeue | grep worker-l").read().split().count('Q')
            if (launcher_queued == 0 and launcher_running == nNodes):
                break
        print("All are running! Gather ip addresses...")
        time.sleep(10)
        host_addresses = []
        for _ , _ , files in os.walk(os.path.join(out_path,"IPS")):
            for filename in files:
                host_addresses.append("http://" + filename)
        slurm_jobs = []
        for _ , _ , files in os.walk(os.path.join(out_path,"JOBIDS")):
            for filename in files:
                slurm_jobs.append(filename)
        print("Read addresses\n", host_addresses)
        communicator.endpointsOnline(host_addresses)
        print("Starting calculation...")
        func(host_addresses, *args)
        print("Everything finished! Shutting down Api instances...")
        for line in slurm_jobs:
            os.system(f"scancel {line}")
