# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
from django.core.exceptions import ObjectDoesNotExist

from socketio_app.models import Users

async_mode = None

import os

from django.http import HttpResponse
import socketio

basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=async_mode)
thread = None


def index(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return HttpResponse(open(os.path.join(basedir, 'static/index.html')))


def background_thread():
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'},
                 namespace='/test')


@sio.event
def is_online(sid, message):
    print(message)


@sio.event
def update_sio(sid, message):
    print(message)
    try:
        phone = message['phone']
        user = Users.objects.get(phone=phone)
        print(user)
        user.socket_sio = sid
        user.save()
        sio.emit("is_online", user.socket_sio, room=sid)
    except ObjectDoesNotExist:
        sio.emit('is_online', None, room=sid)


@sio.event
def send_message(sid, data):
    phone = data['recipient']
    message = data['message']
    try:
        user = Users.objects.get(phone=phone)
        if user.socket_sio is not None:
            sio.emit('message_reply', '{}__SEP__{}'.format(message, phone), room=user.socket_sio)
            # sio.emit('start_dialog', '{}__SEP__{}'.format(message, phone), room=user.socket_sio)
    except ObjectDoesNotExist:
        pass


@sio.event
def message_reply(sid, message):
    print({'data': message['data']})

@sio.event
def start_dialog(sid, message):
    pass


@sio.event
def join(sid, message):
    sio.enter_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
             room=sid)
    print({'data': 'Entered room: ' + message['room']})


@sio.event
def leave(sid, message):
    sio.leave_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Left room: ' + message['room']},
             room=sid)


@sio.event
def close_room(sid, message):
    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    sio.close_room(message['room'])


@sio.event
def my_room_event(sid, message):
    sio.emit('my_response', {'data': message['data']}, room=message['room'])
    print({'data': message['data']})


@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


@sio.event
def connect(sid, environment):
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)
    print('connected ' + sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')
