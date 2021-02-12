import socket
from flask import Flask, request
from flask_restful import Api, Resource, abort

import TaskHandler as th


app = Flask(__name__)
api = Api(app)

jobs = {}

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
        task = th.TaskHandler(request.json)
        task.enroll()
        task.perform()
        jobs[job_id] = task
        return "", 201

    @app.route("/api/<int:job_id>", methods = ["GET"])
    def get_request(job_id):
        notExist(job_id)
        return jobs[job_id].processResults(), 201

    @app.route("/api/<int:job_id>", methods = ["DELETE"])
    def delete_request(job_id):
        notExist(job_id)
        jobs[job_id].cleanUp()
        del jobs[job_id]
        return "", 201


api.add_resource(SerenityAPI, "/api/<int:job_id>")

if __name__ == "__main__":
	app.run(host = socket.gethostbyname(socket.gethostname()) ,debug = False)