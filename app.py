from flask import Flask, request, render_template, redirect, url_for
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_keyframe(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count // 2)  # Get middle frame
    ret, frame = cap.read()
    if ret:
        keyframe_path = video_path.rsplit('.', 1)[0] + "_frame.jpg"
        cv2.imwrite(keyframe_path, frame)
        return keyframe_path
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    search_engine = request.form.get('search_engine')
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    if file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        file_path = extract_keyframe(file_path) or file_path
    
    return redirect_to_search(file_path, search_engine)

import requests

def redirect_to_search(image_path, engine):
    if engine == "google":
        return redirect(f"https://lens.google.com/uploadbyurl?url={image_path}")
    elif engine == "bing":
        return redirect(f"https://www.bing.com/images/search?view=detailv2&iss=sbi&form=SBIVSP&sbisrc=UrlPaste&imgurl={image_path}")
    elif engine == "yandex":
        return redirect(f"https://yandex.com/images/search?rpt=imageview&url={image_path}")
    elif engine == "tineye":
        return redirect(f"https://www.tineye.com/search/?url={image_path}")
    elif engine == "pimeyes":
        return redirect(f"https://pimeyes.com/en/?uploaded_image={image_path}")
    else:
        return "Invalid search engine selected"

if __name__ == '__main__':
    app.run(debug=True)
