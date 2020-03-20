from django.core.management.commands.runserver import Command as RunCommand

from socketio_app.views import sio


class Command(RunCommand):
    help = 'Run the Socket.IO server'

    def handle(self, *args, **options):
        if sio.async_mode == 'threading':
            super(Command, self).handle(*args, **options)
        elif sio.async_mode == 'eventlet':
            # deploy with eventlet
            import eventlet
            import eventlet.wsgi
            from bpo.wsgi import application
            eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 8052)), application)
        elif sio.async_mode == 'gevent_uwsgi':
            print('Start the application through the uwsgi server. Example:')
            print('uwsgi --http :8052 --gevent 1000 --http-websockets '
                  '--master --wsgi-file django_example/wsgi.py --callable '
                  'application')
        else:
            print('Unknown async_mode: ' + sio.async_mode)
