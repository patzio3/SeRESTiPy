import socket, codecs
from flask import Flask, request
from flask_restful import Api, Resource, abort
#from threading import Thread
import multiprocessing as mp

import random, sys

import TaskHandler as th
import DataBaseController as db


app = Flask(__name__)
api = Api(app)

jobs = {}
rand_ids = []
#dbController = db.DataBaseController(".base")

def notExist(job_id):
        if job_id not in jobs:
            abort(404, message = "Requested job not found!")

def exists(job_id):
        if job_id in jobs:
            abort(409, message = "Requested job already exists!")



class SerenityAPI(Resource):
    @app.route("/api/<int:job_id>", methods = ["POST"])
    def parse_request(job_id):
        exists(job_id)
        cycle = 0
        while (True):
            rand = random.randint(0, sys.maxsize)
            if (rand not in rand_ids):
                rand_ids.append(rand)
                break
            elif (cycle == sys.maxsize):
                print("Maximum number of jobs "+str(sys.maxsize)+" reached!!!")
                sys.exit()
            else:
                cycle += 1
        task = th.TaskHandler(request.json, rand)
        task.enroll()
        p = mp.Process(target=task.perform, args=())
        p.daemon = True
        p.start()
        #Thread(target=task.perform).start()
        jobs[job_id] = task
        return "", 201

    @app.route("/api/<int:job_id>", methods = ["GET"])
    def get_request(job_id):
        notExist(job_id)
        finished = False
        if(jobs[job_id].getJobState in ["FINISH", "FINISHED", "FIN"]):
            finished = True
        return finished, 201

    @app.route("/api/<int:job_id>", methods = ["DELETE"])
    def delete_request(job_id):
        notExist(job_id)
        jobs[job_id].cleanUp()
        del jobs[job_id]
        return "", 201




class JobInfo(Resource):
    @app.route("/api/<int:job_id>/info", methods = ["GET"])
    def getJobInfo(job_id):
        notExist(job_id)
        return jobs[job_id].getTaskInfo(), 201




class HomePage(Resource):
    @app.route("/", methods = ["GET"])
    def homePageHit():
        return "HomePage Endpoint hit!", 201




class ApiPage(Resource):
    @app.route("/api/", methods = ["GET"])
    def apiPageHit():
        f = codecs.open("index.html", "r")
        return f.read(), 201


api.add_resource(HomePage, "/")
api.add_resource(ApiPage, "/api")
api.add_resource(SerenityAPI, "/api/<int:job_id>")
api.add_resource(JobInfo, "/api/<int:job_id>/info")

if __name__ == "__main__":
	app.run(host = socket.gethostbyname(socket.gethostname()) ,debug = False)
