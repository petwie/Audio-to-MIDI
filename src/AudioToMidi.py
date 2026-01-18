from LoadAudioFile import LoadAudioFile   # oder: from LoadAudioFile import LoadAudioFile
from LoadSTFT import LoadSTFT
from SpectralFluxCalculator import SpectralFluxCalculator


class AudioToMidi:

    def __init__(self, file_path):

        self.file_path = file_path
        
        self.audio = LoadAudioFile(file_path)
        self.stft = LoadSTFT(n_fft=2048, hop_length=512, audio=self.audio)
        self.flux = SpectralFluxCalculator(None)  # Placeholder for SpectralFluxCalculator instance
        # Further processing steps would go here

    def runfile(self):

        # Hier kommt der Code hin, der die Datei verarbeitet(Eigentlicher ablauf)

        self.audio.load_audio()

        self.stft.calculate_STFT()

        self.stft.plot_spectrogram(title="Spectrogram")

        self.flux = SpectralFluxCalculator(self.stft.calculated_stft)

        self.flux.calculate_spectral_flux()

        self.flux.plot_spectral_flux(self.flux.calculated_FLUX, title="Spectral Flux")

        self.flux.positive_part_calculate_spectral_flux()

        self.flux.plot_spectral_flux(self.flux.calculated_FLUX, title="Positive Spectral Flux") 
        




        