import docker
import os, sys
import socket
import codecs
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

class SwarmLauncher():
    def run(self):
        ncpu = sys.argv[1] if len(sys.argv) >= 2 else "4"
        memory = sys.argv[2] if len(sys.argv) >= 3 else "20000"
        nContainer = int(sys.argv[3]) if len(sys.argv) >= 4 else 24
        client = docker.from_env()
        # client.login(username = os.getenv("DOCKERHUB_USERNAME"), password = os.getenv("DOCKERHUB_PASSWORD"))
        for i in range(nContainer):
            outpath = os.path.join(os.getenv('DATABASE_DIR'))
        	#os.mkdir(outpath)
        	#run with one cpu
            mount_map = docker.types.Mount("/home/calc", outpath, type = "bind")
            client.containers.run('pesch01/serestipy:v1.4.2', 
        	                      cpuset_cpus= ncpu, 
        	                      mem_limit = memory+"m", 
        	                      mounts = [mount_map],
        	                      ports = {'5000/tcp': 5000 + i + 1},
        	                      detach = True)
        all_containers = client.containers.list()
        ip_addresses = []
        for index, container in enumerate(all_containers):
            #ip_addresses.append("http://" + container.attrs['NetworkSettings']['IPAddress'] + ":" +str(5000 + index + 1))
            ip_addresses.append("http://" + socket.gethostbyname(socket.gethostname()) + ":" + str(5000 + index + 1))
        
        with open(os.path.join(os.getenv('DATABASE_DIR'),"ips_hosts"), "a") as handle:
            for i in ip_addresses:
                handle.write(str(i)+"\n")
       


app = Flask(__name__)
api = Api(app)
class SDKPrune(Resource):
    @app.route("/api/", methods = ["POST"])
    def prune():
        client = docker.from_env()
        for container in client.containers.list(): 
            container.stop()
        os.system("docker container prune -f")
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            raise RuntimeError('Not running werkzeug')
        shutdown_func()

    @app.route("/api/", methods = ["GET"])
    def ready():
        return jsonify({"STATE: ": "ONLINE"}), 201


api.add_resource(SDKPrune, "/api/")

if __name__ == "__main__":
    os.environ["DATABASE_DIR"] = "/WORK/p_esch01/scratch_calc"
    launcher = SwarmLauncher()
    launcher.run()
    app.run(host=socket.gethostbyname(socket.gethostname()), debug=False)
