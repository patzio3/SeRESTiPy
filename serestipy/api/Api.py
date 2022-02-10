#!/usr/bin/env  python3
#@file   Api.py
#
#@date   Feb 9, 2022
#@author Patrick Eschenbach
#@copyright \n
# This file is part of the program SeRESTiPy.\n\n
# SeRESTiPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.\n\n
# SeRESTiPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.\n\n
# You should have received a copy of the GNU Lesser General
# Public License along with SeRESTiPy.
# If not, see <http://www.gnu.org/licenses/>.\n

import socket
import codecs
import random
import sys
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort
import multiprocessing as mp
import serestipy.api.TaskHandler as th
import serestipy.api.JobFormatChecker as jc

app = Flask(__name__)
api = Api(app)
jobs = {}
manager = mp.Manager()
jobstate_list = manager.dict()
res_manager = mp.Manager()
results_list = res_manager.dict()

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
        content = request.get_json(force = True)
        if (not isinstance(content,dict)):
            return jsonify({"Job not posted": "JSON invalid"}), 201
        checker = jc.JobFormatChecker(content)
        valid = checker.run()
        if (valid):
            task = th.TaskHandler(content)
            jobs[job_id] = task
            task.enroll(jobstate_list, job_id)
            p = mp.Process(target=task.perform, args=(jobstate_list, job_id,results_list,))
            p.daemon = True
            p.start()
            return jsonify({"Job posted": str(job_id)}), 201
        else:
            return jsonify({"Job not posted": "JSON invalid"}), 201

    @app.route("/api/<int:job_id>", methods=["GET"])
    def get_request(job_id):
        notExist(job_id)
        return jsonify({"STATE: ": jobstate_list[job_id]}), 201

    @app.route("/api/<int:job_id>", methods=["DELETE"])
    def delete_request(job_id):
        notExist(job_id)
        jobs[job_id].cleanUp()
        del jobs[job_id]
        return jsonify({"Job deleted": str(job_id)}), 201

class HomePage(Resource):
    @app.route("/api/", methods = ["GET"])
    def homePageHit():
        return jsonify({"STATE: ": "ONLINE"}), 201

class ResultsPage(Resource):
    @app.route("/api/<int:job_id>/results/", methods=["GET"])
    def res_request(job_id):
        notExist(job_id)
        content = request.get_json(force=True)
        results = jobs[job_id].getResults(job_id,results_list,content["TYPE"])
        return jsonify(results), 201

api.add_resource(ser_api, "/api/<int:job_id>")
api.add_resource(ResultsPage, "/api/<int:job_id>/results/")
api.add_resource(HomePage, "/api/")

if __name__ == "__main__":
    from waitress import serve
    serve(app, host = socket.gethostbyname(socket.gethostname()), port = int(sys.argv[1]))
