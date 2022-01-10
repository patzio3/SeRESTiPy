import docker
import os, sys


ncpu = sys.argv[1] if len(sys.argv >= 2) else "4"
memory = sys.argv[2] if len(sys.argv >= 3) else "48000"
nContainer = int(sys.argv[3]) if len(sys.argv >= 4) else 8


client = docker.from_env()
# client.login(username = os.getenv("DOCKERHUB_USERNAME"), password = os.getenv("DOCKERHUB_PASSWORD"))

for i in range(nContainer):
	outpath = os.path.join("/home/calc","container"+str(i))
	os.mkdir(outpath)
	#run with one cpu
	mount_map = docker.types.Mount("/home/calc", outpath, type = "bind")
	client.containers.run('pesch01/serestipy:v1.4_service', 
	                      cpuset_cpus= ncpu, 
	                      mem_limit = f"{memory}m", 
	                      mounts = [mount_map],
	                      #ports = {'5000/tcp': 5000},
	                      detach = True)


all_containers = client.containers.list()
ip_addresses = []
for container in all_containers:
	ip_addresses.append(container.attrs['NetworkSettings']['IPAddress'])

print(ip_addresses)

#for container in all_containers:
#        container.stop()
#for container in all_containers:
#        container.start()



