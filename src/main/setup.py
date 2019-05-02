# from generator import generateStatic, generateDynamic

# generateStatic()
# generateDynamic()

from code.util.register import serve
from http.server import HTTPServer
import code.web
import code.generator.pages
import sys
import logging
from code.util.db import User
from code.util.auth import generatePassword
logging.basicConfig(level=logging.DEBUG)

user = "Admin"
# port = int(sys.argv[2])

# password = "presently description kirk died"
usr = User.getByName(user)
if usr:
    password = usr.password
else:
    password = generatePassword()
    usr = User(user, password, "admin")
    usr.save()

logging.info(f"Admin username is '{user}'")
logging.info(f"Admin password is '{password}'")

# server_address = ('0.0.0.0', port)
# httpd = HTTPServer(server_address, Server)
logging.info('Starting server...')
# httpd.serve_forever()

codes = {
    200: "200 OK",
    302: "302 Found",
    403: "403 Forbidden",
    404: "404 Not Found",
    500: "500 Internal Server Error"
}

def application(env, start_response):
    code, headers, response = serve(env)
    logging.debug((code, headers, str(response)[:50]))
    start_response(codes[code], headers)
    return str(response).encode("utf-8")
