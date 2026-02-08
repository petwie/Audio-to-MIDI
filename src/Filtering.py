
import matplotlib.pyplot as plt
from scipy import signal

class Filtering:

    def __init__(self,audio_array, kick_lower_frequency, kick_upper_frequency, snare_lower_frequency, snare_upper_frequency, hihat_lower_frequency, hihat_upper_frequency, sample_rate):

        self.kick_frequency_range = (kick_lower_frequency, kick_upper_frequency)  # Typischer Frequenzbereich für Kick-Drums
        self.snare_frequency_range = (snare_lower_frequency, snare_upper_frequency)  # Typischer Frequenzbereich für Snare-Drums
        self.hihat_frequency_range = (hihat_lower_frequency, hihat_upper_frequency)  # Typischer Frequenzbereich für Hi-hats

        self.audio_array = audio_array
        self.sample_rate = sample_rate

        self.sos_Kick = None
        self.sos_Snare = None
        self.sos_Hihat = None

        self.y_kick = None
        self.y_snare = None
        self.y_hihat = None



    def load_filter(self, filter_type):
        if filter_type == "Kick":

            # Beispiel: Ein elliptischer Bandpass-Filter für Kick-Drums (angepasst an typische Kick-Frequenzen)
            # Die Frequenzen 50 Hz und 250 Hz sind typische Bereiche für Kick-Drums, aber das kann je nach Musikstil variieren.
            # 50/ sample_rate/2 und 250/sample_rate/2 normalisieren die Frequenzen auf den Nyquist-Frequenzbereich.
            # 4 ist die Filterordnung, 0.1 dB Passband-Ripple, 40 dB Stopband-Dämpfung
            self.sos_Kick = signal.ellip(4, 0.1, 40, [self.kick_frequency_range[0] / (self.sample_rate / 2), self.kick_frequency_range[1] / (self.sample_rate / 2)], btype='bandpass', output='sos')
            

        elif filter_type == "Snare":

            self.sos_Snare = signal.ellip(4, 0.1, 40, [self.snare_frequency_range[0] / (self.sample_rate / 2), self.snare_frequency_range[1] / (self.sample_rate / 2)], btype='bandpass', fs=self.sample_rate, output='sos')

        elif filter_type == "Hihat":

            self.sos_Hihat = signal.ellip(4, 0.1, 40, [self.hihat_frequency_range[0] / (self.sample_rate / 2), self.hihat_frequency_range[1] / (self.sample_rate / 2)], btype='bandpass', fs=self.sample_rate, output='sos')
        # Implement filter loading logic based on filter_type (e.g., "Kick", "Snare", "Hihat")
        pass

    def filter_for_Kick(self):

       self.y_kick = signal.sosfiltfilt(self.sos_Kick, self.audio_array)

       pass


    def filter_for_Snare(self):
        self.y_kick = signal.sosfiltfilt(self.sos_Snare, self.audio_array)
        # Implement peak finding logic
        pass

    def filter_for_Hihat(self):
        self.y_kick = signal.sosfiltfilt(self.sos_Hihat, self.audio_array)
        # Implement peak finding logic
        pass