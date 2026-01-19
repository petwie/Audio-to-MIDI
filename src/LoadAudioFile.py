import numpy as np
import librosas
import matplotlib.pyplot as plt
import os


class LoadAudioFile:

    def __init__(self,file_path):
        self.audio_array, self.sample_rate = None, None
        self.file_path = file_path

    def load_audio(self, target_sr=22050, mono=True):
        # 1. Check: Existiert die Datei überhaupt?
        if not os.path.exists(self.file_path):
            print(f"FEHLER: Die Datei '{self.file_path}' wurde nicht gefunden.")
            return None, None

        print(f"Lade Datei: {self.file_path} ...")

        try:
            # 2. Versuch: Librosa Load (Das kann schiefgehen, wenn Format kaputt ist)
            self.audio_array, self.sample_rate = librosa.load(self.file_path, sr=target_sr, mono=True)
            
            # 3. Check: Ist die Datei leer oder extrem kurz?
            if self.audio_array is None or len(self.audio_array) == 0:
                print(f"FEHLER: Die Datei wurde geladen, enthält aber keine Audiodaten (Länge 0).")
                return None, None
                
            # Optional: Warnung bei sehr kurzen Dateien (< 0.1 Sekunden)
            if librosa.get_duration(y=self.audio_array, sr=self.sample_rate) < 0.1:
                print(f"WARNUNG: Datei ist extrem kurz ({librosa.get_duration(y=self.audio_array, sr=self.sample_rate):.3f}s).")

            print(f"Erfolg: Audio geladen ({len(self.audio_array)} Samples, {self.sample_rate} Hz).")
            return self.audio_array, self.sample_rate

        except Exception as e:
            # 4. Catch-All: Fängt alle anderen Librosa-Internen Fehler ab (z.B. falscher Codec)
            print(f"KRITISCHER FEHLER beim Laden: {e}")
            return None, None

