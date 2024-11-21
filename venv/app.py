import os
from flask import Flask, render_template, send_from_directory
import utils
import json
import ffmpeg

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_list')
def video_list():
    video_list = []
    video_path = 'static/video'
    for file in os.listdir(video_path):
        if file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.webm'):
            filename = os.path.join(video_path, file)
            video_list.append({'file': file, 'frames': [utils.file_thumbnail(filename)]})
    return json.dumps(video_list)

def get_audio_tracks(video_file):
    # Получение информации о видеофайле
    probe = ffmpeg.probe(video_file)
    audio_tracks = []

    # Извлечение аудиодорожек
    for stream in probe['streams']:
        if stream['codec_type'] == 'audio':
            audio_tracks.append({
                'index': stream['index'],
                'codec': stream['codec_name'],
                'language': stream.get('tags', {}).get('language', 'und'),
                'bitrate': stream.get('bit_rate')
            })

    return audio_tracks


if __name__ == '__main__':
    app.run(host='192.168.0.110', port=8000, debug=True)
