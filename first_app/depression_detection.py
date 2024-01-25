import librosa
import pandas as pd 
import numpy as np
from keras import models

def extract_features(filename):
    x = []
    X, sample_rate = librosa.load(filename, duration=3, offset=0.5)
    # Mcc
    Mcc = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=25)
    Mcc = np.mean(Mcc.T, axis=0)
    # chroma_stft
    chroma_stft = librosa.feature.chroma_stft(y=X, sr=sample_rate,n_chroma=12, n_fft=4096)
    chroma_stft = np.mean(chroma_stft.T, axis=0)
    # chroma_cqt
    chroma_cqt = librosa.feature.spectral_bandwidth(y=X, sr=sample_rate)
    chroma_cqt = np.mean(chroma_cqt.T, axis=0)
    # melspectrogram
    melspectrogram = librosa.feature.melspectrogram(y=X, sr=sample_rate)
    melspectrogram = np.mean(melspectrogram.T, axis=0)
    # spectral_centroid
    spectral_centroid = librosa.feature.spectral_centroid(y=X, sr=sample_rate)
    spectral_centroid = np.mean(spectral_centroid.T, axis=0)
    # spectral_contrast
    spectral_contrast = librosa.feature.spectral_contrast(y=X, sr=sample_rate)
    spectral_contrast = np.mean(spectral_contrast.T, axis=0)
    feature = np.hstack((Mcc, chroma_stft, chroma_cqt, melspectrogram, spectral_centroid, spectral_contrast))
    
    return np.array(feature)

def class_prediction(path):
    
    classes = ['Depression', 'Neutral', 'No Depression']
    classes_arabic = ['اكتئاب', 'مشاعر حيادية', 'لا يوجد اكتئاب']

    # model_cnn2 = models.load_model('E:\\Django-Projects\\senior\\first_app\\depression_detection_model.h5')
    model_cnn2 = models.load_model('first_app\\depression_detection_model.h5')

    # Function to preprocess the audio data
    def preprocess_audio(audio):
        # Preprocess your audio data (e.g., convert to spectrogram, normalize, etc.)
        mfcc = extract_features(audio)
        features_df = pd.DataFrame(mfcc.tolist())
        features_df = features_df.apply(lambda x: x/100)
        features = np.array([features_df])
        # Return the preprocessed audio data
        return features

    # Function to predict the class of a new audio
    def predict_class(audio):
        # Preprocess the audio data
        input_data = preprocess_audio(audio)
        
        # Predict the class probabilities using the trained model
        predictions = model_cnn2.predict(input_data[0:1])
        
        print(predictions)
        # Get the predicted class label
        predicted_class_index = np.argmax(predictions)
        predicted_class_label = classes_arabic[predicted_class_index]
        
        return predicted_class_label

    predicted_class = predict_class(path)
    return predicted_class

