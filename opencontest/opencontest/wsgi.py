"""
WSGI config for opencontest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from contest.auth import generatePassword
from contest.models.user import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opencontest.settings')

user = 'Admin'

usr = User.getByName(user)
if usr:
    password = usr.password
else:
    password = generatePassword()
    usr = User(user, password, 'admin')
    usr.save()

print(f'Admin username is "{user}".')
print(f'Admin password is "{password}".')

print('Starting server...')
application = get_wsgi_application()
