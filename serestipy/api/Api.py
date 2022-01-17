import socket
import codecs
import random
import sys
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort
import multiprocessing as mp
import serestipy.api.TaskHandler as th


app = Flask(__name__)
api = Api(app)
jobs = {}
manager = mp.Manager()
jobstate_list = manager.dict()


def notExist(job_id):
    if job_id not in jobs:
        abort(404, message="Requested job not found!")


def exists(job_id):
    if job_id in jobs:
        abort(409, message="Requested job already exists!")


class ser_api(Resource):
    @app.route("/api/<int:job_id>", methods=["POST"])
    def parse_request(job_id):
        exists(job_id)
        content = request.get_json(force=True)
        task = th.TaskHandler(content)
        if (task.jsonValid()):
            jobs[job_id] = task
            task.enroll(jobstate_list, job_id)
            p = mp.Process(target=task.perform, args=(jobstate_list, job_id,))
            p.daemon = True
            p.start()
            return jsonify({"Job posted id: ": str(job_id)}), 201
        else:
            return jsonify({"Job not posted id: ": "invalid"}), 201

    @app.route("/api/<int:job_id>", methods=["GET"])
    def get_request(job_id):
        notExist(job_id)
        return jsonify({"STATE: ": jobstate_list[job_id]}), 201

    @app.route("/api/<int:job_id>", methods=["DELETE"])
    def delete_request(job_id):
        notExist(job_id)
        jobs[job_id].cleanUp()
        del jobs[job_id]
        return "", 201

class HomePage(Resource):
    @app.route("/api/", methods = ["GET"])
    def homePageHit():
        return jsonify({"STATE: ": "ONLINE"}), 201


api.add_resource(ser_api, "/api/<int:job_id>")
api.add_resource(HomePage, "/api/")

if __name__ == "__main__":
    app.run(host=socket.gethostbyname(socket.gethostname()), debug=False)
