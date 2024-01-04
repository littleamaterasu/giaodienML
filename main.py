import flask
from flask import Flask, render_template, request, redirect
import cv2
import numpy as np

app = flask.Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
