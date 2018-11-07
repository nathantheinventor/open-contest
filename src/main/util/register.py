import sys
from http.server import BaseHTTPRequestHandler
import json
import os
import mimetypes
from code.util import auth
import logging
logging.basicConfig(level=logging.DEBUG)


paths = {}


class endpoint:
    def __init__(self, url: str, method: str, userType: str, callback: callable):
        self.url      = url
        self.method   = method
        self.userType = userType
        self.callback = callback


def post(url: str, userType: str, callback: callable):
    paths[url + "|POST"] = endpoint(url, "POST", userType, callback)


def get(url: str, userType: str, callback: callable):
    paths[url + "|GET"] = endpoint(url, "GET", userType, callback)


def fits(cookie, userType: str) -> bool:
    logging.debug(f"Checking cookie {cookie} against userType {userType}")
    if userType == "any":
        return True
    elif userType == "loggedin":
        return auth.getUser(cookie) is not None
    elif userType == "admin":
        return auth.isAdmin(cookie)
    elif userType == "participant":
        return auth.isParticipant(cookie)
    return False


def serveStatic(self, path):
    path = "/code/serve" + path
    logging.info("Serving {}".format(path))
    if os.path.abspath(path).startswith("/code/serve"):
        if not os.path.exists(path) or not os.path.isfile(path):
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not found")
        else:
            with open(path, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", mimetypes.guess_type(path))
                self.end_headers()
                self.wfile.write(f.read())
    else:
        self.send_response(403)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Not authorized")


class Server(BaseHTTPRequestHandler):
    def handleRequest(self, method):
        url = self.path
        url = url.split("?")[0]
        url = url.split("#")[0]
        logging.info("Call to {}".format(url))

        headers = {
            "Content-type": "text/html"
        }
        statusCode = 200
        response = ""

        if url.startswith("/static"):
            path = url[7:]
            serveStatic(self, path)
            return

        if f"{url}|{method}" in paths:
            endpoint = paths[f"{url}|{method}"]
            if not fits(self.headers["Cookie"], endpoint.userType):
                if method == "POST":
                    statusCode = 403
                    headers["Content-type"] = "text/plain"
                    response = f"Not authorized: {url}"
                else:
                    statusCode = 302
                    headers["Location"] = "/static/login.html"
            else:
                content_length = int(self.headers['Content-Length'])
                f = self.rfile.read(content_length)
                params = {} if f == b"" else json.loads(f)
                user = auth.getUser(self.headers["Cookie"])
                try:
                    result = endpoint.callback(params, self.send_header, user)
                    logging.info(result)
                    if isinstance(result, str):
                        headers["Content-type"] = "text/plain"
                        response = result
                    elif isinstance(result, int):
                        statusCode = result
                    elif isinstance(result, dict) or isinstance(result, list):
                        headers["Content-type"] = "application/json"
                        response = json.dumps(result)
                    else:
                        headers["Content-type"] = "application/json"
                        response = "" # TODO: util.toString(result)
                    logging.info(result)
                    logging.info(response)
                except Exception as e:
                    statusCode = 500
                    headers["Content-type"] = "text/plain"
                    response = f"Internal Error: {e}"
        else:
            statusCode = 404
            headers["Content-type"] = "text/plain"
            response = f"Not found: {url}"

        self.send_response(statusCode)
        for header in headers:
            self.send_header(header, headers[header])
        self.end_headers()
        self.wfile.write(bytes(response, "utf-8"))

    def do_GET(self):
        return self.handleRequest("GET")
    
    def do_POST(self):
        return self.handleRequest("POST")
