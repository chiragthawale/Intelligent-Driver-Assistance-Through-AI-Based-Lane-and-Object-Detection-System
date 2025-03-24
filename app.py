import os
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify, Response, abort, send_from_directory
from flask_cors import CORS
from main import LO_Detector
import tempfile
import re

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  

os.makedirs(Path('temp_storage'), exist_ok=True)
os.makedirs(Path('temp_storage/ip'), exist_ok=True)
os.makedirs(Path('temp_storage/op'), exist_ok=True)

detector = LO_Detector(op_dir=Path('temp_storage/op'))

def stream_video(path):
    with open(path, 'rb') as video:
        while chunk := video.read(1024 * 1024):  
            yield chunk

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/detect_LO', methods=['POST'])
def detect_lo():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video']

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4', dir=Path('temp_storage/ip')) as temp_file:
        temp_file.write(video_file.read()) 
        temp_file_path = temp_file.name
    
    try:
       
        filepath = detector.detect(temp_file_path)
        os.remove(temp_file_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({
        "message": "Detection Successfully Completed!",
        "video_url": f"{filepath}"
    }), 200
    
    
@app.route('/temp_storage/op/<filename>', methods=['GET'])
def video_feed(filename):
    video_path = os.path.join(r'temp_storage/op', filename)
    if os.path.exists(video_path):
        return Response(stream_video(video_path), mimetype='video/mp4')
    else:
        return "Video not found", 404

    
if __name__ == "__main__":
    app.run(debug=True)