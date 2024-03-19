# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 19:41:23 2023

@author: froot
"""

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np  # Add this line to import NumPy

def midi_to_note_number(midi_pitch):
    # Convert MIDI pitch to note number
    return 69 + 12 * np.log2(midi_pitch / 440.0)

def plot_pitch_change(file_path):
    # Load the audio file and its sample rate
    y, sr = librosa.load(file_path, sr=None)

    # Compute the time-varying fundamental frequency (pitch)
    pitch_track, _ = librosa.piptrack(y=y, sr=sr)

    # Replace NaN and infinity values with a default value (-1)
    pitch_track[np.isinf(pitch_track) | np.isnan(pitch_track)] = -1

    # Set a threshold for pitch frequencies (e.g., 0 Hz)
    pitch_track[pitch_track < 0] = 0

    # Convert pitch track to Hz
    pitch_hz = librosa.midi_to_hz(pitch_track)
    
    
    
    
    # Create a time array for plotting
    hop_length = len(y) // pitch_hz.shape[1]
    time = np.arange(0, pitch_hz.shape[1]) * hop_length / sr

    # Plot pitch over time
    plt.figure(figsize=(12, 4))
    plt.plot(time, pitch_hz[0, :], label='Pitch (Hz)')  # Use only the first channel (monophonic)
    plt.xlabel('Time (s)')
    plt.ylabel('Pitch (Hz)')
    plt.title('Pitch over Time')
    plt.grid(True)
    plt.legend()

    # Plot the pitch range
    plt.figure(figsize=(12, 4))
    pitch_range = np.any(pitch_hz > 0, axis=0)  # Determine if pitch is above 0 Hz (indicating presence of pitch)
    plt.fill_between(time, 0, 1, where=pitch_range, alpha=0.5, color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Pitch Range')
    plt.title('Pitch Range over Time')
    plt.grid(True)

    # Calculate pitch changes
    pitch_changes = np.diff(pitch_hz)
    pitch_change_count = np.count_nonzero(pitch_changes != 0)

    # Plot pitch change count over time
    plt.figure(figsize=(12, 4))
    plt.plot(time[1:], pitch_changes[0, :], label='Pitch Change')
    plt.xlabel('Time (s)')
    plt.ylabel('Pitch Change')
    plt.title(f'Pitch Change Count: {pitch_change_count}')
    plt.grid(True)
    plt.legend()

    plt.show()

# Replace 'your_file.wav' with the path to your .wav file
file_path = r'C:\VT\summer_proj\sample_file.wav'
plot_pitch_change(file_path)

