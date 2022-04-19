from datetime import timedelta
from flask import Flask, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO
import compare
import data_cleaning
import time
import nltk


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret#'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sample')
def sample():
    return render_template('sample2.html')

@app.route('/session', methods=['GET','POST'])
def sessions():
    if(request.method == 'POST'):
        session['user'] = request.form['username']
        return render_template('session.html', user=session['user'])
    else:
        session.clear()
        return redirect(url_for('/'))


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):

    # print('received my event: ' + str(json))
    start = time.time()   
    tokens = compare.clean_text(json['message'])
    print("Tokens: ",tokens)
    white_space_tokenizer = nltk.WhitespaceTokenizer()
    
    sentence = white_space_tokenizer.tokenize(json['message'])#data_cleaning.whitespace_tokenizer(json['message'])#list(json['message'].split(' '))
    print("sentence: ",type(sentence))
    
    backup = []
    for word in sentence:
        for key, value in tokens.items():
            # print("word: ",word)
            if word == key and value['isProfane'] == True:
                x = ''.join(['*' for x in word])
                # ls[ls.index(word)] = word.replace(word,x)
                backup.append(x)
                break
            elif word == key and value['isProfane'] == False: 
                backup.append(word)
                break
            
    filtered_message = ' '.join(backup)
    

    socketio.emit('my response', {'user_name': 'Sam', 'message': filtered_message}, callback=messageReceived)
    end = time.time()
    print('time: ', end - start)

if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run()