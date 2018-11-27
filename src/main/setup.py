# from generator import generateStatic, generateDynamic

# generateStatic()
# generateDynamic()

from code.util.register import Server
from http.server import HTTPServer
import code.web
import sys
from code.generator.pages.static import generateStatic
from code.generator.pages.dynamic import generateDynamic
import logging
from code.util.db import User
logging.basicConfig(level=logging.DEBUG)

generateStatic()
generateDynamic()

user = sys.argv[1]
port = int(sys.argv[2])

usr = User(user, "presently description kirk died", "admin")
usr.save()

server_address = ('0.0.0.0', port)
httpd = HTTPServer(server_address, Server)
logging.info('Starting server...')
httpd.serve_forever()
