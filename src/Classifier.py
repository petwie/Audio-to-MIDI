from SpectralFluxCalculator import SpectralFluxCalculator
from PeakPicking import PeakPicking

class Classifier:

    def __init__(self, flux_array):
        self.flux_array = flux_array
        self.onsets_Kick = []
        self.onsets_Snare = []
        self.onsets_Hihat = []

        self.SpectralFlux = SpectralFluxCalculator()
        self.PeakPicker = PeakPicking()

    def find_Kick(self):
        # Implement peak finding logic
        pass


    def find_Snare(self):
        # Implement peak finding logic
        pass

    def find_Hihat(self):
        # Implement peak finding logic
        pass