from flask import Flask, request, jsonify, render_template
import requests
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def reverse_image_search(image_path):
    search_url = "https://www.google.com/searchbyimage/upload"
    with open(image_path, 'rb') as img:
        files = {'encoded_image': img, 'image_content': ''}
        response = requests.post(search_url, files=files, allow_redirects=False)
    return response.headers.get('Location')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    result_url = reverse_image_search(file_path)
    return jsonify({"image_result": result_url})

if __name__ == '__main__':
    app.run(debug=True)
