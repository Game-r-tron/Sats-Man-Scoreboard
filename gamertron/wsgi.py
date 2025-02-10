"""
WSGI config for gamertron project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import socket
import time
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamertron.settings')

# Wait for port to be available
port = int(os.getenv('PORT', 3000))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.bind(('0.0.0.0', port))
        s.close()
        break
    except socket.error:
        time.sleep(1)

application = get_wsgi_application()
