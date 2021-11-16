import socket, codecs, random, sys
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort
# import multiprocessing as mp

import TaskHandler as th
# import TaskUpdater as tu
# import DataBaseController as db



app = Flask(__name__)
api = Api(app)
jobs = {}
# manager = mp.Manager()
# jobstate_list = manager.dict()
# rand_ids = []



def notExist(job_id):
    if job_id not in jobs:
        abort(404, message = "Requested job not found!")

# def notFinished(job_id):
#         if jobstate_list[job_id] != "FIN" :
#             abort(409, message = "Job is still running!")

def exists(job_id):
    if job_id in jobs:
        abort(409, message = "Requested job already exists!")



class ser_api(Resource):
    @app.route("/api/<int:job_id>", methods = ["POST"])
    def parse_request(job_id):
        exists(job_id)
        jobs[job_id] = request.get_json(force = True)
        # cycle = 0
        # while (True):
        #     rand = random.randint(0, sys.maxsize)
        #     if (rand not in rand_ids):
        #         rand_ids.append(rand)
        #         break
        #     elif (cycle == sys.maxsize):
        #         print("Maximum number of jobs "+str(sys.maxsize)+" reached!!!")
        #         sys.exit()
        #     else:
        #         cycle += 1
        task = th.TaskHandler(request.get_json(force = True))
        task.enroll()
        task.perform(job_id)
        #p = mp.Process(target=task.perform, args=(jobstate_list,job_id))
        #p.daemon = True
        #p.start()
        jobs[job_id] = task
        return jsonify({"Job": "posted with id: "+str(job_id)}), 201

    @app.route("/api/<int:job_id>", methods = ["PATCH"])
    def patch_request(job_id):
        # notExist(job_id)
        # notFinished(job_id)
        # task = jobs[job_id]
        # updater = tu.TaskUpdater(task, request.json)
        # updater.run()
        # del updater
        #task.update()
        #p = mp.Process(target=task.perform, args=(jobstate_list,job_id))
        #p.daemon = True
        #p.start()
        return "", 201

    @app.route("/api/<int:job_id>", methods = ["GET"])
    def get_request(job_id):
        notExist(job_id)
        return jobs[job_id], 201

    @app.route("/api/<int:job_id>", methods = ["DELETE"])
    def delete_request(job_id):
        notExist(job_id)
        # notFinished(job_id)
        jobs[job_id].cleanUp()
        del jobs[job_id]
        return "", 201




# class JobInfo(Resource):
#     @app.route("/api/<int:job_id>/info", methods = ["GET"])
#     def getJobInfo(job_id):
#         notExist(job_id)
#         return jobs[job_id].getTaskInfo(), 201



api.add_resource(ser_api, "/api/<int:job_id>")
# api.add_resource(JobInfo, "/api/<int:job_id>/info")

if __name__ == "__main__":
	app.run(host = socket.gethostbyname(socket.gethostname()) ,debug = False)
