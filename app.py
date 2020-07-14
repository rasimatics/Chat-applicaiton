from flask import Flask,render_template,request,redirect,url_for,flash
from flask_socketio import SocketIO,join_room
from flask_login import LoginManager, login_user,login_required,current_user,logout_user
from db import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sij%&)($*$KJLFKPOJIFH)_)!)_)@$'

socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



@login_manager.user_loader
def load_user(username):
    return get_user(username)



@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password):
            login_user(user)
            flash('User loged in succesfully!')
            return redirect(url_for('home'))
        else:
            flash('User cridentials are not correct!')
    return render_template('login.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if get_user(username):
            flash('This username is taken')
            return redirect(url_for('signup'))
        else:
            save_user(username,email,password)
            flash('User created succesfully')
            return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

    

@app.route('/chat')
def chat():
    room = request.args.get('room')
    if room:
        return render_template('chat.html',room=room)
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