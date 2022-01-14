import os, sys
import time
import functools
import APICommunicator as comm


class AKCluster():
    def determineSettings(self, nSystems, nCPU = 4, nRAM = 20000):
        # maxRAM = 500000
        # maxCPU = 94

        maxRAM = 350000
        maxCPU = 32
        if (nCPU != 4):
            maxWorker = (maxCPU // nCPU)
        elif (nRAM != 20000):
            maxWorker = (maxRAM // nRAM)
        elif (nRAM != 20000 and nCPU != 4):
            if (nCPU > maxCPU and nRAM > maxRAM):
                print("Specified settigns are too large!")
                sys.exit()
            maxWorker = (maxCPU // nCPU) if ((maxCPU // nCPU) <= maxRAM // nRAM) else (maxRAM // nRAM)
        else:
            maxWorker = 8
        nWorkerPerNode = nSystems if (nSystems <= maxWorker) else maxWorker
        nNodes = (nSystems // nWorkerPerNode) if (nSystems % nWorkerPerNode == 0) else (nSystems // nWorkerPerNode + 1)
        return nCPU, nRAM, nNodes, nWorkerPerNode

    def run(self, func, nCPU, nRAM, nNodes, nWorkerPerNode, partition, *args):
        communicator = comm.APICommunicator()
        print("Cleaning left-overs...")
        ips_file = os.path.join(os.getenv('DATABASE_DIR'), "ips_hosts")
        if (os.path.exists(ips_file)):
            os.remove(ips_file)
        out_path = os.path.join(os.getenv('DATABASE_DIR'))
        for file in os.listdir(out_path):
            if (file.startswith("out")):
                os.remove(os.path.join(out_path,file))
        print("Individual worker specs: CPU "+str(nCPU)+", Memory: "+str(nRAM)+"MB with " +
              str(nWorkerPerNode)+" Worker(s) per node on "+str(nNodes)+" Node(s)...")
        print("Submitting worker launcher instances...")
        for _ in range(nNodes):
            os.system("python PrepareSLURM.py " + str(nWorkerPerNode) +
                      " 4 " + partition + " " + str(nCPU) + " " + str(nRAM))
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
        communicator.apiEndpointsOnline(host_addresses)
        print("Starting calculation...")
        func(host_addresses, *args)
        print("Everything finished! Shutting down worker containers...")
        base_addresses = set()
        _ = [base_addresses.add(i[:-5] + ":5000") for i in host_addresses]
        _ = communicator.requestEvent("POST", list(base_addresses), ["" for i in range(len(list(base_addresses)))], ['{}' for i in range(len(list(base_addresses)))])
