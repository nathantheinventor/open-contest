# from generator import generateStatic, generateDynamic

# generateStatic()
# generateDynamic()

from code.util.register import Server
from http.server import HTTPServer
import code.web
import code.generator.pages
import sys
import logging
from code.util.db import User
logging.basicConfig(level=logging.DEBUG)

user = sys.argv[1]
port = int(sys.argv[2])

password = "presently description kirk died"
usr = User(user, password, "admin")
usr.save()
logging.info(f"Admin username is '{user}'")
logging.info(f"Admin password is '{password}'")

server_address = ('0.0.0.0', port)
httpd = HTTPServer(server_address, Server)
logging.info('Starting server...')
httpd.serve_forever()
