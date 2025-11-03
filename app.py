from flask import Flask, request, render_template as rt, send_from_directory
import cv2
import numpy as np
import os

app = Flask(__name__)

@app.route('/')
def index():
    return rt('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    image = request.files['image']

    # Save uploaded image temporarily
    upload_path = '/tmp/image.jpg'
    image.save(upload_path)

    # Read and process
    img = cv2.imread(upload_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(inverted, (199, 199), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)

    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    sharp = cv2.filter2D(sketch, -1, kernel)

    output_path = '/tmp/final.jpg'
    cv2.imwrite(output_path, sharp)

    return rt('result.html', img1='final.jpg')

# ✅ Route to serve files from /tmp folder
@app.route('/tmp/<filename>')
def tmp(filename):
    return send_from_directory('/tmp', filename)

if __name__ == '__main__':
    app.run(debug=True)
