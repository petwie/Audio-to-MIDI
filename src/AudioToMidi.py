from LoadAudioFile import LoadAudioFile   # oder: from LoadAudioFile import LoadAudioFile
from LoadSTFT import LoadSTFT


class AudioToMidi:

    def __init__(self, file_path):

        self.file_path = file_path
        
        self.audio = LoadAudioFile(file_path)
        self.stft = LoadSTFT(n_fft=2048, hop_length=512, audio=self.audio)
        # Further processing steps would go here

    def runfile(self):

        # Hier kommt der Code hin, der die Datei verarbeitet(Eigentlicher ablauf)

        self.audio.load_audio()

        self.stft.calculate_STFT()

        self.stft.plot_spectrogram(title="Spectrogram")


        