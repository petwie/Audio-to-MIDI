from LoadAudioFile import LoadAudioFile   # oder: from LoadAudioFile import LoadAudioFile
from LoadSTFT import LoadSTFT
from SpectralFluxCalculator import SpectralFluxCalculator
from PeakPicking import PeakPicking
from MidiExport import MidiExport
from Filtering import Filtering

class AudioToMidi:

    def __init__(self, file_path_kick, file_path_snare, file_path_hihat):
        self.file_path_kick = file_path_kick
        self.file_path_snare = file_path_snare
        self.file_path_hihat = file_path_hihat

        # Erstelle direkt die Instanzen der LoadAudioFile-Klasse
        self.audio_kick = LoadAudioFile(self.file_path_kick)
        self.audio_snare = LoadAudioFile(self.file_path_snare)
        self.audio_hihat = LoadAudioFile(self.file_path_hihat)
        self.filer = None  # Placeholder for Filtering instance
        self.stft = None
        self.flux = None  # Placeholder for SpectralFluxCalculator instance
        self.picker = None
        self.midi_writer = None
        # Further processing steps would go here

    def runfile(self):

# 1. KICK VERARBEITEN
        self.audio_kick.load_audio()
        # Hier korrigiert: self.audio_kick.sample_rate statt self.audio.sample_rate
        self.stft = LoadSTFT(n_fft=2048, hop_length=512, audio=self.audio_kick.audio_array, sample_rate=self.audio_kick.sample_rate)

        self.stft.calculate_STFT()

        self.stft.plot_spectrogram(title="Spectrogram")

        self.flux = SpectralFluxCalculator(self.stft.calculated_stft)

        self.flux.calculate_spectral_flux()

        self.flux.plot_spectral_flux(self.flux.calculated_FLUX, title="Spectral Flux")

        self.flux.positive_part_calculate_spectral_flux()

        self.flux.plot_spectral_flux(self.flux.calculated_FLUX, title="Positive Spectral Flux") 

        self.picker = PeakPicking(self.flux.calculated_FLUX)

        self.onsets_kick = self.picker.find_peaks(window_size=512, wait=3)
        
        self.picker.plot_results()

        self.audio_snare.load_audio()

        self.stft = LoadSTFT(n_fft=2048, hop_length=512, audio=self.audio_snare.audio_array, sample_rate=self.audio_snare.sample_rate)

        self.stft.calculate_STFT()

        self.stft.plot_spectrogram(title="Spectrogram")

        self.flux = SpectralFluxCalculator(self.stft.calculated_stft)

        self.flux.calculate_spectral_flux()

        self.flux.plot_spectral_flux(self.flux.calculated_FLUX, title="Spectral Flux")

        self.flux.positive_part_calculate_spectral_flux()

        self.flux.plot_spectral_flux(self.flux.calculated_FLUX, title="Positive Spectral Flux") 

        self.picker = PeakPicking(self.flux.calculated_FLUX)

        self.onsets_snare = self.picker.find_peaks(window_size=512, wait=3)
        
        self.picker.plot_results()

        self.audio_hihat.load_audio()

        self.stft = LoadSTFT(n_fft=2048, hop_length=512, audio=self.audio_hihat.audio_array, sample_rate=self.audio_hihat.sample_rate)

        self.stft.calculate_STFT()

        self.stft.plot_spectrogram(title="Spectrogram")

        self.flux = SpectralFluxCalculator(self.stft.calculated_stft)

        self.flux.calculate_spectral_flux()

        self.flux.plot_spectral_flux(self.flux.calculated_FLUX, title="Spectral Flux")

        self.flux.positive_part_calculate_spectral_flux()

        self.flux.plot_spectral_flux(self.flux.calculated_FLUX, title="Positive Spectral Flux") 

        self.picker = PeakPicking(self.flux.calculated_FLUX)

        self.onsets_hihat = self.picker.find_peaks(window_size=512, wait=3)
        
        self.picker.plot_results()

        self.midi_writer = MidiExport(bpm=120)

        output_filename = self.file_path_kick.replace(".m4a", ".mid").replace(".wav", ".mid")

        self.midi_writer.export_midi(
            self.onsets_kick, 
            self.onsets_snare, 
            self.onsets_hihat, 
            output_path=output_filename, 
            sample_rate=self.audio_kick.sample_rate, # Auch hier korrigiert
            hop_length=self.stft.hop_length
        )
