import sys
from http.server import BaseHTTPRequestHandler
import json
import os
import mimetypes
from code.util import auth
from urllib.parse import parse_qs
import traceback
import logging
import re
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

webEndpoints = []
def web(url: str, userType: str, callback: callable):
    webEndpoints.append((url, userType, callback))

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

def HTMLMatches(url):
    for (u, _, __) in webEndpoints:
        if re.match(u, url):
            return True
    return False

def serveHTML(self, url):
    endpoint = None
    for (u, t, c) in webEndpoints:
        x = re.match(u, url)
        if x:
            endpoint = (u, t, c, x)
            break
    
    logging.info(endpoint)
    _, userType, callback, x = endpoint
    params = x.groups()
    user = auth.getUser(self.headers["Cookie"])

    statusCode = 200
    headers = [("Content-type", "text/html")]
    if not fits(self.headers["Cookie"], userType):
        statusCode = 302
        headers = [("Location", "/")]
        response = ""
        return statusCode, headers, response
    
    try:
        response = callback(params, user)
    except Exception as e:
        exc = traceback.format_exc()
        logging.error(exc)
        statusCode = 500
        response = "Internal error" 
    return statusCode, headers, response

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

def setHeader(headers, name, value):
    headers.append((name, value))

class Server(BaseHTTPRequestHandler):
    def handleRequest(self, method):
        url = self.path
        url = url.split("?")[0]
        url = url.split("#")[0]
        logging.info("Call to {}".format(url))

        headers = []
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
                    headers.append(("Content-type", "text/plain"))
                    response = f"Not authorized: {url}"
                else:
                    statusCode = 302
                    headers.append(("Location", "/login"))
            else:
                content_length = int(self.headers['Content-Length'] or 0)
                f = self.rfile.read(content_length).decode("utf-8")
                params = parse_qs(f)
                for param in params:
                    if len(params[param]) == 1:
                        params[param] = params[param][0]
                user = auth.getUser(self.headers["Cookie"])
                try:
                    result = endpoint.callback(params, lambda x, y: setHeader(headers, x, y), user)
                    logging.info(result)
                    if isinstance(result, str):
                        headers.append(("Content-type", "text/plain"))
                        response = result
                    elif isinstance(result, int):
                        statusCode = result
                    elif isinstance(result, dict) or isinstance(result, list):
                        headers.append(("Content-type", "application/json"))
                        response = json.dumps(result)
                    else:
                        headers.append(("Content-type", "application/json"))
                        response = "" # TODO: util.toString(result)
                except Exception as e:
                    exc = traceback.format_exc()
                    logging.error(exc)
                    statusCode = 500
                    headers.append(("Content-type", "text/plain"))
                    response = f"Internal Error: {e}"
        elif HTMLMatches(url):
            statusCode, headers, response = serveHTML(self, url)
        else:
            statusCode = 404
            headers.append(("Content-type", "text/plain"))
            response = f"Not found: {url}"

        self.send_response(statusCode)
        for header, value in headers:
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(bytes(str(response), "utf-8"))

    def do_GET(self):
        return self.handleRequest("GET")
    
    def do_POST(self):
        return self.handleRequest("POST")
