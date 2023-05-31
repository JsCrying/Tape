from flask import session
from flask_socketio import emit, join_room, leave_room
from .define_socket import chat_socketio

print('import files')

@chat_socketio.on('connect', namespace='/window')
def connect():
    print('Connect Success')

@chat_socketio.on('joined', namespace='/window')
def joined(information):
    room_name = information.get('client_to_server')
    user_name = session.get('user_name')
    print(user_name + ' joined room!')
    join_room(room_name)
    emit(
        'status', 
        {
            'user_name': user_name,
            'server_to_client': user_name + ' enters the room',
        },
        room = room_name
    )

@chat_socketio.on('left', namespace='/window')
def left(information):
    room_name = information.get('client_to_server')
    user_name = session.get('user_name')
    if user_name:
        del session[user_name]
    leave_room(room_name)
    emit(
        'status',
        {
            'user_name': user_name,
            'server_to_client': user_name + ' has left the room',
        },
        room = room_name
    )

@chat_socketio.on('msg', namespace='/window')
def msg(information):
    room_name = information.get('client_to_server')
    msg = information.get('msg').encode('raw_unicode_escape').decode()
    img = information.get('img') # 接收到的是 bytes
    timestamp = information.get('timestamp').encode('raw_unicode_escape').decode()
    user_name = session.get('user_name')
    emit(
        'message',
        {
            'user_name': user_name,
            'msg': msg,
            'img': img,
            'timestamp': timestamp
        },
        room = room_name
    )