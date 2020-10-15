import json
import os
import sys
import platform
import socket

import logging
from datetime import datetime

from flask import Flask, Response
from flask import request

import pymysql

from comment_service.service import CommentService
from user_service.service import UserService

__comment_service = CommentService()
__user_service = UserService()

cwd = os.getcwd()
sys.path.append(cwd)
print("*** PYHTHONPATH = " + str(sys.path) + "***")


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


c_info = {"user": "dbuser",
          "password": "dbuserdbuser",
          "cursorclass": pymysql.cursors.DictCursor
          }


application = Flask(__name__,
                    static_url_path='/static',
                    static_folder='WebSite/static')


def log_and_extract_input(method, path_params=None):

    path = request.path
    args = dict(request.args)
    data = None
    headers = dict(request.headers)
    method = request.method

    try:
        if request.data is not None:
            data = request.json
        else:
            data = None
    except Exception as e:
        # This would fail the request in a more real solution.
        data = "You sent something but I could not get JSON out of it."

    log_message = str(datetime.now()) + ": Method " + method

    inputs =  {
        "path": path,
        "method": method,
        "path_params": path_params,
        "query_params": args,
        "headers": headers,
        "body": data
        }

    log_message += " received: \n" + json.dumps(inputs, indent=2)
    logger.debug(log_message)

    return inputs


def log_response(method, status, data, txt):

    msg = {
        "method": method,
        "status": status,
        "txt": txt,
        "data": data
    }

    logger.debug(str(datetime.now()) + ": \n" + json.dumps(msg, indent=2, default=str))


# This function performs a basic health check. We will flesh this out.
@application.route("/service_info", methods=["GET"])
def service_info():

    pf = platform.system()

    rsp_data = {"status": "healthy",
                "time": str(datetime.now()),
                "platform": pf,
                "release": platform.release()
                }

    if pf == "Darwin":
        rsp_data["note"]= "For some reason, macOS is called 'Darwin'"

    # hostname = socket.gethostname()
    # IPAddr = socket.gethostbyname(hostname)
    #
    # rsp_data["hostname"] = hostname
    # rsp_data["IPAddr"] = IPAddr

    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="application/json")
    return rsp


logger.debug("__name__ = " + str(__name__))


@application.route("/hello_world", methods=["GET"])
def hello():

    rsp_data = {"Response": "Hello World!"
                }

    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="application/json")
    return rsp


@application.route("/api/users", methods=["GET", "POST"])
def users():

    req_info = log_and_extract_input("/api/users", None)

    try:
        if req_info["method"] == "GET":

            res = __user_service.query(req_info["query_params"])

            if res is not None:
                rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        elif req_info["method"] == "POST":

            res = __user_service.add(req_info["query_params"])

            if res is not None:
                rsp = Response(json.dumps(res), status=200, content_type="application/json")
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")
    except Exception as e:
        """
        Non-specific, broad except clauses are a bad practice/design.
        """
        rsp = Response("I'm a teapot", status=418, content_type="text/plain")
        logger.error("comment: Exception=" + e)

    log_response("/api/comments/<id>", rsp.status, rsp.data, "")

    return rsp


@application.route("/api/users/<id>", methods=["GET", "DELETE", "PUT"])
def user(id):

    req_info = log_and_extract_input("/api/users", id)

    try:
        if req_info["method"] == "GET":
            res = __user_service.get_by_user_id(id)

            if res is not None:
                rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        elif req_info["method"] == "DELETE":
            res = __user_service.delete_by_user_id(id)

            if res is not None:
                rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        elif req_info["method"] == "PUT":
            res = __user_service.update_by_user_id(id, req_info["query_params"])

            if res is not None:
                rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")
    except Exception as e:
        """
        Non-specific, broad except clauses are a bad practice/design.
        """
        rsp = Response("I'm a teapot", status=418, content_type="text/plain")
        logger.error("comment: Exception=" + e)

    log_response("/api/comments/<id>", rsp.status, rsp.data, "")

    return rsp


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.

    application.run("0.0.0.0", port=5000)
