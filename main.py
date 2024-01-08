from typing import List
import numpy as np
import cv2
from flask import Flask, render_template, request, redirect, url_for, send_file
import os

from werkzeug.datastructures import FileStorage

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'results')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload')
def index():
    return render_template('upload.html')


name_list = []
res = []


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
                if filename not in name_list:
                    name_list.append(filename)
                    res.append(filename)

    return render_template('upload.html', name_list=name_list)


@app.route('/results', methods=['GET'])
def show_image():
    return render_template('results.html', name_list=res)


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
