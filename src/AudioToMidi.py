from LoadAudioFile import LoadAudioFile   # oder: from LoadAudioFile import LoadAudioFile
from LoadSTFT import LoadSTFT
from SpectralFluxCalculator import SpectralFluxCalculator
from PeakPicking import PeakPicking
from MidiExport import MidiExport
from Filtering import Filtering

class AudioToMidi:

    def __init__(self, file_path):

        self.file_path = file_path
        
        self.audio = LoadAudioFile(file_path)
        self.filer = None  # Placeholder for Filtering instance
        self.stft = None
        self.flux = None  # Placeholder for SpectralFluxCalculator instance
        self.picker = None
        self.midi_writer = None
        # Further processing steps would go here

    def runfile(self):

          # Hier kommt der Code hin, der die Datei verarbeitet(Eigentlicher ablauf)

        self.audio.load_audio()

        self.filer = Filtering(self.audio.audio_array, kick_lower_frequency=20, kick_upper_frequency=50, snare_lower_frequency=150, snare_upper_frequency=2500, hihat_lower_frequency=3000, hihat_upper_frequency=10000, sample_rate=self.audio.sample_rate)

        self.filer.load_filter("Hihat")

        self.filer.filter_for_Hihat()

        self.stft = LoadSTFT(n_fft=2048, hop_length=512, audio=self.filer.y_hihat, sample_rate=self.audio.sample_rate)

        self.stft.calculate_STFT()

        self.stft.plot_spectrogram(title="Spectrogram")

        self.flux = SpectralFluxCalculator(self.stft.calculated_stft)

        self.flux.calculate_spectral_flux()

        self.flux.plot_spectral_flux(self.flux.calculated_FLUX, title="Spectral Flux")

        self.flux.positive_part_calculate_spectral_flux()

        self.flux.plot_spectral_flux(self.flux.calculated_FLUX, title="Positive Spectral Flux") 

        self.picker = PeakPicking(self.flux.calculated_FLUX)

        self.onsets = self.picker.find_peaks(window_size=12, delta=50, wait=3)
        
        self.picker.plot_results()

        self.midi_writer = MidiExport(bpm=120)

        output_filename = self.file_path.replace(".m4a", ".mid").replace(".wav", ".mid")

        self.midi_writer.export_midi(onsets_frames=self.onsets, output_path=output_filename, sample_rate=self.audio.sample_rate, hop_length=self.stft.hop_length)
