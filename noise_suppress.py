# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 21:13:29 2023

@author: froot
"""


from pydub import AudioSegment
import os

# Input directory containing original WAV files
input_dir = 'C:/VT/summer_proj'  # Replace with the path to your input directory
# Output directory for denoised WAV files
output_dir = 'C:/VT/summer_proj/snr'  # Replace with the desired output directory
os.makedirs(output_dir, exist_ok=True)

# Load the noise audio file
noise_audio_path = 'C:/VT/summer_proj/snr/microphone_noise.wav'
noise_audio = AudioSegment.from_wav(noise_audio_path)
# Calculate the dB difference between the original and noise
db_difference =  noise_audio.dBFS

# Loop through the WAV files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".wav"):
        # Load the original audio
        original_audio = AudioSegment.from_wav(os.path.join(input_dir, filename))
        
        # Adjust the noise level to match the original audio
        adjusted_noise = noise_audio - db_difference
        
        # Apply noise reduction by subtracting the adjusted noise from the original audio
        denoised_audio = original_audio - adjusted_noise
        
        # Save the denoised audio as a new WAV file in the output directory
        denoised_path = os.path.join(output_dir, filename.replace(".wav", "_denoised.wav"))
        denoised_audio.export(denoised_path, format="wav")
        
        print(f"Denoised audio saved: {denoised_path}")