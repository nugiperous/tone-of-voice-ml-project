# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 22:35:21 2023

@author: froot
"""
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# Set the duration for recording (in seconds)
duration = 10

# Specify the samplerate (samples per second)
samplerate = 44100  # You can adjust this value if needed

# Record audio from the microphone
print("Recording noise from microphone...")
recorded_audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
sd.wait()  # Wait until recording is finished

# Define the output paths
wav_path = 'captured_noise.wav'
npy_path = 'noise_profile.npy'

# Save the recorded audio as a WAV file using scipy.io.wavfile
wav.write(wav_path, samplerate, recorded_audio)

# Load the recorded WAV file
y, sr = librosa.load(wav_path, sr=None)

# Create a noise profile
noise_profile = np.mean(np.abs(y))

# Save the noise profile as an NPY file
np.save(npy_path, noise_profile)

print("Noise profile saved as NPY.")