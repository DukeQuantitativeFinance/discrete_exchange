from flask import Flask, request
import os

from server import Server


app = Flask(__name__)
app.config['UPLOAD_DEST'] = os.path.dirname(__file__) + '/submitted_traders'

server = Server()
# server.import_all_traders('submitted_traders')
# server.begin_game(100)

@app.route('/submit', methods = ['POST'])
def submit_trader():
    if request.method == 'POST':
        print('post request received')
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_DEST'], filename))
        server.add_player()
        
    return '<h1></h1>'

