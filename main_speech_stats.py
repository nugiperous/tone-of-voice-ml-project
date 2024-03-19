# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 12:39:33 2023

@author: froot
"""

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def plot_pitch_change(file_path):
    # Load the audio file and its sample rate
    y, sr = librosa.load(file_path, sr=None)

    # Compute the spectrogram (magnitude) using Short-Time Fourier Transform (STFT)
    stft = librosa.stft(y)
    spectrogram = np.abs(stft)

    # Convert the magnitude spectrogram to decibels (dB) for better visualization
    log_spectrogram = librosa.amplitude_to_db(spectrogram, ref=np.max)

    # Create a time array for plotting
    hop_length = len(y) // log_spectrogram.shape[1]
    time = np.arange(0, log_spectrogram.shape[1]) * hop_length / sr

    # Plot the spectrogram
    plt.figure(figsize=(12, 6))
    librosa.display.specshow(log_spectrogram, sr=sr, hop_length=hop_length,
                             x_axis='time', y_axis='linear', cmap='viridis')
    plt.colorbar(format='%+2.0f dB')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram: Change in Pitch over Time for "I am a Wizard?" Sarcastic Statement Audio File')
    plt.tight_layout()

    # Highlight the pitch range (frequencies with higher pitch)
    pitch_range = log_spectrogram >= -20  # Adjust the threshold value as needed
    plt.contourf(time, librosa.fft_frequencies(sr=sr, n_fft=hop_length), pitch_range, alpha=0.5, colors='red')

    # Count the number of pitch changes
    pitch_changes = np.sum(pitch_range, axis=0)
    num_pitch_changes = np.sum(pitch_changes > 0)

    plt.text(0.1, 0.9, f'Number of Pitch Changes: {num_pitch_changes}', transform=plt.gca().transAxes,
             color='white', fontsize=12, bbox=dict(facecolor='red', alpha=0.5))

    plt.show()

# Replace 'your_file.wav' with the path to your .wav file
file_path = 'C:/VT/summer_proj/plotting/sarc_audio.wav'
plot_pitch_change(file_path)