from flask import Flask, jsonify, request
import pyautogui
import time

import librosa
import numpy as np
import scipy.signal as signal

from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/action/<string:left_or_right>', methods=['GET'])
def action(left_or_right):
    if left_or_right == "left":
        # return left arrow key
        time.sleep(1)
        pyautogui.press('left', presses = 1)

        return jsonify({'message' : 'left'})
    elif left_or_right == "right":
        # return right arrow key
        time.sleep(1)
        pyautogui.press('right', presses = 1)
        return jsonify({'message' : 'right'})

    else:
        return jsonify({'message' : 'ERROR!!!!'})


@app.route('/music', methods=['POST'])
def action():
    audio_path = request.get_json()['audio_path']
    og_file = request.get_json()['og_file']

    # Load audio file
    audio_file = "audio.wav"
    y, sr = librosa.load(audio_file)

    # Extract notes
    notes, _ = librosa.piptrack(y=y, sr=sr)

    # Get frequencies from notes
    freqs = librosa.core.midi_to_hz(notes[0])

    # Process frequencies using scipy
    freqs = signal.medfilt(freqs, kernel_size=3)

    # Convert frequencies back to notes
    processed_notes = list(librosa.core.hz_to_midi(freqs))

    my_file = open(og_file, "r")
  
    data = my_file.read()
    
    data_into_list = data.split(" ")
    percentage = sum([int(processed_notes[i] == data_into_list[i]) for i in range(len(data_into_list))]) / len(data_into_list) * 100
    return jsonify({'percent' : str(percentage)})

    
if __name__ == "__main__":
    app.run(debug=True)