from datetime import timedelta
from flask import Flask, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret#'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sample')
def sample():
    return render_template('sample2.html')

@app.route('/session', methods=['GET','POST'])
def sessions():
    if(request.method == 'POST'):
        session['user'] = (request.form['username'])
        return render_template('session.html', user=session['user'])
    else:
        session.clear()
        return redirect(url_for('/'))


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):

    print('received my event: ' + str(json))

    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)