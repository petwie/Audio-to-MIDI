import numpy as np
import librosa
import matplotlib.pyplot as plt
import os

def load_audio(file_path, target_sr=22050, mono=True):
    # 1. Check: Existiert die Datei überhaupt?
    if not os.path.exists(file_path):
        print(f"FEHLER: Die Datei '{file_path}' wurde nicht gefunden.")
        return None, None

    print(f"Lade Datei: {file_path} ...")

    try:
        # 2. Versuch: Librosa Load (Das kann schiefgehen, wenn Format kaputt ist)
        y, sr = librosa.load(file_path, sr=target_sr, mono=True)
        
        # 3. Check: Ist die Datei leer oder extrem kurz?
        if y is None or len(y) == 0:
            print(f"FEHLER: Die Datei wurde geladen, enthält aber keine Audiodaten (Länge 0).")
            return None, None
            
        # Optional: Warnung bei sehr kurzen Dateien (< 0.1 Sekunden)
        if librosa.get_duration(y=y, sr=sr) < 0.1:
            print(f"WARNUNG: Datei ist extrem kurz ({librosa.get_duration(y=y, sr=sr):.3f}s).")

        print(f"Erfolg: Audio geladen ({len(y)} Samples, {sr} Hz).")
        return y, sr

    except Exception as e:
        # 4. Catch-All: Fängt alle anderen Librosa-Internen Fehler ab (z.B. falscher Codec)
        print(f"KRITISCHER FEHLER beim Laden: {e}")
        return None, None

def calculate_STFT(AudioArray, sample_rate, n_fft, hop_length):
    if AudioArray is None:
        print("FEHLER: Kein Audio-Array zum Berechnen der STFT vorhanden.")
        return None

    try:
        stft_result = librosa.stft(AudioArray, n_fft=n_fft, hop_length=hop_length)
        stft_result = np.abs(stft_result)
        print(f"STFT berechnet: Form {stft_result.shape}")
        return stft_result
    except Exception as e:
        print(f"FEHLER bei der STFT-Berechnung: {e}")
        return None
    
def plot_spectrogram(stft_result, sample_rate, hop_length, title="Spectrogram"):
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