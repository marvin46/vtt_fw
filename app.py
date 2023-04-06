import io
import json
import os
import uuid

from flask import Flask, request, Response
from tempfile import NamedTemporaryFile
from faster_whisper import WhisperModel

app = Flask(__name__)
app.config['DEBUG'] = True

MODEL_SIZE = 'small'
UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = {'wav','mp3'}

@app.route('/', methods=['GET'])
def home():
    return {"success": True, "message": "Hello World from voice_to_text FW"}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/test_mp3', methods=['GET'])
def test_mp3():
    model_size = "small"
    model = WhisperModel(model_size, compute_type="int8")
    segments, info = model.transcribe("audiobook.mp3")
    data = ''
    for segment in segments:
        data += segment.text
    del model
    return {'success': True, 'data':data}

@app.route('/test_wav', methods=['GET'])
def test_wav():
    model_size = "small"
    model = WhisperModel(model_size, compute_type="int8")
    segments, info = model.transcribe("indonesian.wav")
    data = ''
    for segment in segments:
        data += segment.text
    del model
    return {'success': True, 'data':data}

@app.route('/transcript', methods=['POST'])
def transcript():

    # 01 field, files Validation
    audio_file = request.files.get("audio_file")
    if not audio_file :
        return {
            'data': False,
            'success': False,
            'message': 'Failed transcript audio to text, Request field audio_file is requied and must be audio file .mp3 or .wav',
        }

    # 02 format validation 
    allowed = allowed_file(audio_file.filename)
    if not allowed :
        return {
            'data': False,
            'success': False,
            'message': f'Failed transcript audio to text, File Name {audio_file.filename} Not Allowed',
        }

    # 03 Write unique file
    tempName = str(uuid.uuid4())
    tempFile = os.path.join(app.config['UPLOAD_FOLDER'], f'{tempName}_{audio_file.filename}')
    
    # 04 Read Open & Write audio data to file uploaded files
    audio_data = audio_file.read()
    with open(tempFile, 'wb') as f:
        f.write(audio_data)

    # 05 load model and start transcribe audio to text
    model = WhisperModel(MODEL_SIZE, compute_type="int8")
    segments, info = model.transcribe(tempFile)
    data = ''
    for segment in segments:
        data += segment.text

    # 06 Remove uploaded file
    if os.path.isfile(tempFile):
        os.remove(tempFile)
    
    del model

    return {'success': True, 'data':data}

@app.route('/clear_uploaded_files', methods=['GET'])
def clear_uploaded_files():
    paths = app.config['UPLOAD_FOLDER']
    lenFile = 0
    for f in os.listdir(paths):
        os.remove(os.path.join(paths, f))
        lenFile += 1

    removedStr = str(lenFile)
    return {'message' : 'Removed ' + removedStr + ' Files'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)