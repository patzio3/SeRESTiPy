import docker
import os

client = docker.from_env()
client.login(username = "", password = "")

for i in range(5):
	outpath = os.path.join("/home/calc","container"+str(i))
	os.mkdir(outpath)
	#run with one cpu
	mount_map = docker.types.Mount("/home/calc", outpath, type = "bind")
	client.containers.run('pesch01/serestipy:v1.4_service', 
	                      cpuset_cpus= "1", 
	                      mem_limit = "4g", 
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



