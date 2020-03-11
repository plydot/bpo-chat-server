import os

from django.core.wsgi import get_wsgi_application
import socketio

from socketio_app.views import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bpo.settings")

django_app = get_wsgi_application()
application = socketio.WSGIApp(sio, django_app)
