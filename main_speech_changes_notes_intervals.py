# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 22:10:00 2023

@author: froot
"""

import librosa
import numpy as np

def midi_to_note_number(midi_pitch):
    # Convert MIDI pitch to note number
    return 69 + 12 * np.log2(midi_pitch / 440.0)

def save_pitch_change_count(file_path, output_file):
    # Load the audio file and its sample rate
    y, sr = librosa.load(file_path, sr=None)

    # Compute the time-varying fundamental frequency (pitch)
    pitch_track, _ = librosa.piptrack(y=y, sr=sr)

    # Replace NaN and infinity values with a default value (-1)
    pitch_track[np.isinf(pitch_track) | np.isnan(pitch_track)] = -1

    # Set a threshold for pitch frequencies (e.g., 0 Hz)
    pitch_track[pitch_track < 0] = 0

    # Convert pitch track to MIDI
    pitch_midi = librosa.hz_to_midi(pitch_track)

    # Convert pitch track to note number
    pitch_note_number = midi_to_note_number(pitch_midi)
    print(pitch_note_number)
    # Create a time array for calculating pitch changes
    hop_length = len(y) // pitch_note_number.shape[1]
    time = np.arange(0, pitch_note_number.shape[1]) * hop_length / sr

    # Initialize pitch change count
    pitch_change_count = 0

    # Calculate pitch changes between consecutive intervals of 0.1 seconds
    for i in range(1, len(time)):
        interval_duration = time[i] - time[i-1]
        print(time)
        print(interval_duration)
        if interval_duration >= 2:
            note_number_changes = np.diff(pitch_note_number[:, i-1:i+1])
            
            if np.count_nonzero(note_number_changes != 0) > 0:
                pitch_change_count += 1

    # Save the pitch change count to a text file
    with open(output_file, 'w') as f:
        f.write(f'Pitch Change Count: {pitch_change_count}')

# Replace 'your_file.wav' with the path to your .wav file
file_path = r'C:\VT\summer_proj\sample_file.wav'
output_file = r'C:\VT\summer_proj\pitch_change_count.txt'
save_pitch_change_count(file_path, output_file)