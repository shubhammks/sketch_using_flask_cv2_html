from flask import Flask, request, render_template as rt
import cv2,numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return rt('index.html')

@app.route('/submit', methods=['POST'])
def submit():

    image = request.files['image']
    image.save('/tmp/image.jpg')

    image= cv2.imread('static/image.jpg')
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    inverted=cv2.bitwise_not(gray)
    inverted_blur=cv2.GaussianBlur(inverted,(199,199),0)
    skech=cv2.divide(gray,255-inverted_blur,scale=256)
    kernal_sharpen=np.array([[-1,-1,-1],
                            [-1,9,-1],
                            [-1,-1,-1]])
    sharp_skech=cv2.filter2D(skech,-1,kernal_sharpen)

    # showimg(sharp_skech)
    cv2.imwrite('/tmp/final.jpg', sharp_skech)
    # img="static/image.jpg"

    return rt('result.html', img1="final.jpg")


if __name__ == '__main__':
    app.run(debug=True)
