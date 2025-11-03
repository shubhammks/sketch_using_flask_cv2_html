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

    # Save the uploaded image temporarily
    upload_path = '/tmp/image.jpg'
    image.save(upload_path)

    # Read and process the image
    image = cv2.imread(upload_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    inverted_blur = cv2.GaussianBlur(inverted, (199, 199), 0)
    sketch = cv2.divide(gray, 255 - inverted_blur, scale=256)

    kernel_sharpen = np.array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
    ])
    sharp_sketch = cv2.filter2D(sketch, -1, kernel_sharpen)

    # Save the final image in /tmp
    output_path = '/tmp/final.jpg'
    cv2.imwrite(output_path, sharp_sketch)

    # Send to result.html and pass the filename
    return rt('result.html', img1='final.jpg')

# ✅ Route for serving images from /tmp
@app.route('/tmp/<filename>')
def tmp(filename):
    return send_from_directory('/tmp', filename)

if __name__ == '__main__':
    app.run(debug=True)
