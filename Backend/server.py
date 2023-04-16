import openai
from pydub import AudioSegment
from io import BytesIO
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
import sys
sys.path.append('../')
import config


app = Flask(__name__)
CORS(app)

class NamedBytesIO(BytesIO):
    def __init__(self, buffer=None, name=None):
        super().__init__(buffer)
        self.name = name

def split_audio_file(audio):
    half_duration = len(audio) // 2
    first_half = audio[:half_duration]
    second_half = audio[half_duration:]
    
    return first_half, second_half

def audio_segment_to_bytes(audio_segment, name):
    byte_stream = NamedBytesIO(name=name)
    audio_segment.export(byte_stream, format="mp3")
    byte_stream.seek(0)
    return byte_stream

openai.api_key = config.apikey

api_endpoint = 'https://api.openai.com/v1/chat/completions'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ config.apikey
}

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    file = request.files['file']
    file_path = os.path.join(tempfile.gettempdir(), secure_filename(file.filename))
    file.save(file_path)

    audio = AudioSegment.from_mp3(file_path)
    first_half, second_half = split_audio_file(audio)

    first_half_bytes = audio_segment_to_bytes(first_half, "first_half.mp3")
    second_half_bytes = audio_segment_to_bytes(second_half, "second_half.mp3")

    transcript1 = openai.Audio.transcribe("whisper-1", first_half_bytes)
    transcript2 = openai.Audio.transcribe("whisper-1", second_half_bytes)

    t = transcript1["text"].split(".")
    t2 = transcript2["text"].split(".")
    for i in range(len(t2)):
        t.append(t2[i])

    counter = 0
    transcription = ""

    while (counter < len(t)):
        textArr = t[counter:min(len(t), counter+20)]
        counter += 20

        text = ""
        for i in range(len(textArr)):
            text += textArr[i] + '. '

        prompt = 'Summarize this text using bullet points and headers based on the content:  ' + text

        data = {
            'model' : 'gpt-3.5-turbo',
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.8,
            'max_tokens': 100
        }

        response = requests.post(api_endpoint, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            completions = result['choices'][0]['message']['content']
            transcription += "\n" + completions + "\n"
        else:
            transcription += f"Error: {response.status_code} {response.text}\n"

    os.remove(file_path)

    return jsonify({'transcription': transcription})


if __name__ == '__main__':
    app.run(debug=True)
