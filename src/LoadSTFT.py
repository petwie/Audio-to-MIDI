import numpy as np
import librosa
import matplotlib.pyplot as plt
import os



class LoadSTFT:
    
    def __init__(self,n_fft,hop_length,audio,sample_rate):
        self.calculated_stft = None
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.audio = audio
        self.sample_rate = sample_rate

    def calculate_STFT(self):

        AudioArray = self.audio
        n_fft = self.n_fft
        hop_length = self.hop_length

        if AudioArray is None:
            print("FEHLER: Kein Audio-Array zum Berechnen der STFT vorhanden.")
            return None

        try:
            self.calculated_stft = librosa.stft(AudioArray, n_fft=n_fft, hop_length=hop_length)
            self.calculated_stft = np.abs(self.calculated_stft)
            print(f"STFT berechnet: Form {self.calculated_stft.shape}")
            return self.calculated_stft
        except Exception as e:
            print(f"FEHLER bei der STFT-Berechnung: {e}")
            return None

    def plot_spectrogram(self,title="Spectrogram"):
        stft_result = self.calculated_stft
        sample_rate = self.sample_rate
        hop_length = self.hop_length

        if stft_result is None:
            print("FEHLER: Kein STFT-Ergebnis zum Plotten vorhanden.")
            return

        try:
            D = librosa.amplitude_to_db(stft_result, ref=np.max)
            plt.figure(figsize=(10, 6))
            librosa.display.specshow(D, sr=sample_rate, hop_length=hop_length, x_axis='time', y_axis='log')
            plt.colorbar(format='%+2.0f dB')
            plt.title(title)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"FEHLER beim Plotten des Spektrogramms: {e}")