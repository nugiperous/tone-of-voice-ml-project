  # -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 17:32:45 2023

@author: froot
"""
import os
import librosa
import librosa.display
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report

#wav_file_path = 'C:\VT\summer_proj\ques_audio.wav'
wav_file_dir = 'C:\VT\summer_proj'

def frequency_to_note_name(frequency):
    # MIDI note number = 69 + 12 * log2(frequency / 440)
    midi_note_number = 69 + 12 * np.log2(frequency / 440)

    # Define the musical note names
    note_names = [
        "C", "C#", "D", "D#", "E", "F",
        "F#", "G", "G#", "A", "A#", "B"
    ]

    # Calculate the octave number
    octave = int(midi_note_number // 12) - 1

    # Calculate the note index within the octave
    note_index = int(midi_note_number % 12)

    # Get the corresponding musical note name
    note_name = note_names[note_index]

    # Return the formatted note name with the octave number
    return f"{note_name}{octave}"

# Example usage
frequency = 440.0  # A4 frequency in Hz
note_name = frequency_to_note_name(frequency)
print(note_name)  # Output: "A4"

def array_statistics_to_dataframe(data):
    # Calculate statistics
    median = np.median(data)
    maximum = np.max(data)
    minimum = np.min(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    cardinality = len(data)
    
    # Create a DataFrame
    df = pd.DataFrame({
        'Statistic': ['Median', 'Max', 'Min', 'Q1 (25th percentile)', 'Q3 (75th percentile)', 'IQR', 'Cardinality'],
        'Value': [median, maximum, minimum, q1, q3, iqr, cardinality]
    })
    
    return df


def wav_to_highest_volume_frequency(wav_file, interval=.15):
    # Load the WAV file and convert to mono audio (if stereo)
    y, sr = librosa.load(wav_file, mono=True)

    # Calculate the total number of samples in each 0.5-second interval
    samples_per_interval = int(interval * sr)

    # Calculate the number of intervals in the audio
    num_intervals = len(y) // samples_per_interval

    # Initialize an array to store the frequency with the highest volume for each interval
    highest_volume_frequencies = []

    # Iterate through each interval
    for i in range(num_intervals):
        # Extract the samples for the current interval
        start_sample = i * samples_per_interval
        end_sample = start_sample + samples_per_interval
        y_interval = y[start_sample:end_sample]

        # Calculate the root mean square energy for the interval
        rmse = librosa.feature.rms(y=y_interval)

        # Find the index of the frequency bin with the highest energy
        max_energy_index = np.argmax(rmse)

        # Convert the frequency bin index to frequency in Hz
        freq = librosa.fft_frequencies(sr=sr)[max_energy_index]

        # Append the calculated frequency to the result array
        highest_volume_frequencies.append(freq)

    return highest_volume_frequencies


# Define the statistics data dictionary
statistics_data = {
    'Statistic': ['Median', 'Max', 'Min', 'Q1 (25th percentile)', 'Q3 (75th percentile)', 'IQR', 'Cardinality', 
                  'Energy', 'Energy Mean', 'Energy Std', 'MFCC Mean 1', 'MFCC Mean 2'],  # Add more MFCCs as needed
    'Type': []
}

# Create an empty DataFrame with columns for the statistics and "Type"
new_df = pd.DataFrame(columns=statistics_data['Statistic'] + ['Type'])

# Loop through the WAV files
for filename in os.listdir(wav_file_dir):
    if filename.endswith(".wav"):
        wav_file_path = os.path.join(wav_file_dir, filename)
        highest_volume_frequencies = wav_to_highest_volume_frequency(wav_file_path)
        
        # Determine the "Type" based on the file name
        if "ques" in filename:
            file_type = "question"
        elif "stmt" in filename:
            file_type = "statement"
        elif "sarc" in filename:
            file_type = "sarcastic"
        elif "rhet" in filename:
            file_type = "rhetorical"
        else:
            file_type = "unknown"  # Handle other cases as needed
        
        # Calculate statistics
        median = np.median(highest_volume_frequencies)
        maximum = np.max(highest_volume_frequencies)
        minimum = np.min(highest_volume_frequencies)
        q1 = np.percentile(highest_volume_frequencies, 25)
        q3 = np.percentile(highest_volume_frequencies, 75)
        iqr = q3 - q1
        cardinality = len(highest_volume_frequencies)
        
        # Load the audio file
        audio, sr = librosa.load(wav_file_path)
        
        # Calculate energy statistics
        energy = np.sum(np.square(audio))
        energy_mean = np.mean(np.square(audio))
        energy_std = np.std(np.square(audio))
        
        # Calculate MFCCs
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        mfccs_mean = np.mean(mfccs, axis=1)
        
        # Update the DataFrame with the new statistics and "Type"
        new_row = [median, maximum, minimum, q1, q3, iqr, cardinality, 
                   energy, energy_mean, energy_std, mfccs_mean[0], mfccs_mean[1], file_type]  # Add more MFCCs as needed
        new_df.loc[filename] = new_row

# Print the combined DataFrame
print(new_df)

#%% Train the Data

# Assuming you have already created and populated the 'new_df' DataFrame
# Drop the 'Type' column to create the feature matrix 'X' and get the target vector 'y'
X = new_df.drop('Type', axis=1)
y = new_df['Type']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize an SVM classifier
svm_classifier = SVC(kernel='linear')  # You can adjust the kernel as needed

# Train the SVM classifier
svm_classifier.fit(X_train, y_train)

# Predict the target values for the test set
y_pred = svm_classifier.predict(X_test)

# Print the classification report
print("Support Vector Machine Classifier:")
print(classification_report(y_test, y_pred))




from sklearn.ensemble import RandomForestClassifier

# Initialize a Random Forest Classifier
rf_classifier = RandomForestClassifier()

# Train the classifier
rf_classifier.fit(X_train, y_train)

# Predict the target values for the test set
y_pred_rf = rf_classifier.predict(X_test)

# Print the classification report for Random Forest
print("Random Forest Classifier:")
print(classification_report(y_test, y_pred_rf))



from sklearn.neighbors import KNeighborsClassifier

# Initialize a K-Nearest Neighbors Classifier with k=3 (you can adjust k as needed)
knn_classifier = KNeighborsClassifier(n_neighbors=3)

# Train the classifier
knn_classifier.fit(X_train, y_train)

# Predict the target values for the test set
y_pred_knn = knn_classifier.predict(X_test)

# Print the classification report for K-Nearest Neighbors
print("K-Nearest Neighbors Classifier:")
print(classification_report(y_test, y_pred_knn))



from sklearn.linear_model import LogisticRegression

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize a Logistic Regression classifier
logreg_classifier = LogisticRegression(max_iter=1000)  # You can adjust the max_iter as needed

# Train the Logistic Regression classifier
logreg_classifier.fit(X_train, y_train)

# Predict the target values for the test set
y_pred = logreg_classifier.predict(X_test)

# Print the classification report
print("Logistic Regression Classifier:")
print(classification_report(y_test, y_pred))















