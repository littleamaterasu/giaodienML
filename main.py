from typing import List
import numpy as np
import cv2
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import json

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


pic_list = []
#{"filename": tên file, "img": ảnh}
#sau khi upload ảnh sẽ lưu ở đây


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
                if filename not in [file["filename"] for file in pic_list]:
                    pic_list.append({"filename": filename, "img": file})

    return render_template('upload.html', name_list=pic_list)


res = []


def load_model():
    return 1


def predict():
    for item in pic_list:
        #predict -> a.json

        with open('static/results/a.json', 'r') as json_file:
            data = json.load(json_file)

        if item["filename"] not in [file["filename"] for file in res]:
            res.append({"filename": item["filename"], "img": item["img"], "json": data})
    return res


@app.route('/results', methods=['GET'])
def show_image():
    res = predict()
    return render_template('results.html', name_list=res)


@app.route('/download/<jsondata>')
def download(jsondata):
    with open('static/results/data.json', 'w') as data:
        json.dump(jsondata, data, indent=2)
    return send_file('static/results/data.json', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
