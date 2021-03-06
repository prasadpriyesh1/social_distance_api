# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:13:14 2020

@author: MAHE
"""

# main.py
# import the necessary packages
from flask import Flask, render_template, Response
from camera1 import Camera1
from camera2 import Camera2
from camera3 import Camera3
app = Flask(__name__)
@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')
def gen(camera):
    while True:
        #get camera frame
        image = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')
@app.route('/video1')
def video1():
    
    return Response(gen(Camera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video2')
def video2():
    
    return Response(gen(Camera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video3')
def video3():
    
    return Response(gen(Camera3()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0',port='5000', debug=True)
