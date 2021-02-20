import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import time

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp4'}

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'ERROR 1', 500
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return 'ERROR 2', 500
        if file and allowed_file(file.filename):
            print(file)
            temp_filename = secure_filename(file.filename).split('.')
            filename = temp_filename[0] + time.strftime("%Y%m%d%H%M%S") + '.' + temp_filename[1]
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {'message': '/uploads/' + filename}, 200
    return 'success 1', 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print('ssssssssssssssssssssss')
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/uploads/<filename>',  methods=['DELETE'])
def delete_file(filename):
    if request.method == 'DELETE':
        os.remove(app.config['UPLOAD_FOLDER'] + '/' + filename)
        return {'message': 'success'}

if __name__ == '__main__':
    app.run()