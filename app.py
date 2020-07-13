from flask import Flask,render_template,request,redirect,url_for
from flask_socketio import SocketIO,join_room

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template('chat.html',username=username,room=room)
    return redirect(url_for('home'))


@socketio.on('join-room')
def handle_join_room(data):
    join_room(data['room'])
    socketio.emit('join-room-info', data, data['room'])


@socketio.on('send-message')
def handle_send_message(data):
    socketio.emit('receive-message', data, data['room'])




if __name__ == '__main__':
    socketio.run(app,debug=True)