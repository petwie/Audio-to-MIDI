import numpy as np
import librosa
import matplotlib.pyplot as plt
import os

class SpectralFluxCalculator:
    
    def __init__(self,calculated_stft):
        self.calculated_stft = calculated_stft
        if self.calculated_stft is not None:
            self.calculated_FLUX = np.zeros(self.calculated_stft.shape[1] - 1)

    def logarithmic_Magnitude(self):
        if self.calculated_stft is not None:

            log_magnitude = np.log10(self.calculated_stft + 1e-10)  # log(0) wird ein kleiner Wert hinzugefügt, um undefinierte Werte zu vermeiden
            return log_magnitude
        
        else:

            print("FEHLER: Kein STFT-Ergebnis zum Berechnen der logarithmischen Magnitude vorhanden.")
            return None
    

    def calculate_spectral_flux(self):
        if self.calculated_stft is not None:
            # Berechnung des Spektralflusses Nach L1-Norm
            self.calculated_FLUX = self.logarithmic_Magnitude()


            dealt_calculated_FLUX = np.zeros_like(self.calculated_FLUX)
            dealt_calculated_FLUX = self.calculated_FLUX[ : , 1 : ] - self.calculated_FLUX[ : , : -1 ]

            self.calculated_FLUX = np.sum(np.abs(dealt_calculated_FLUX), axis=0) # weil summe über Frequenzbänder

            return self.calculated_FLUX
        

        else:

            print("FEHLER: Kein STFT-Ergebnis zum Berechnen des Spektralflusses vorhanden.")
            return None
        
    def positive_part_calculate_spectral_flux(self):
        if self.calculated_stft is not None:
            # Berechnung des Spektralflusses Nach L1-Norm
            self.calculated_FLUX = self.logarithmic_Magnitude()


            dealt_calculated_FLUX = np.zeros_like(self.calculated_FLUX)
            dealt_calculated_FLUX = self.calculated_FLUX[ : , 1 : ] - self.calculated_FLUX[ : , : -1 ]

            dealt_calculated_FLUX[dealt_calculated_FLUX < 0] = 0  # Nur positive Änderungen berücksichtigen

            self.calculated_FLUX = np.sum(dealt_calculated_FLUX, axis=0) # weil summe über Frequenzbänder

            return self.calculated_FLUX
        

        else:

            print("FEHLER: Kein STFT-Ergebnis zum Berechnen des Spektralflusses vorhanden.")
            return None
    
    @staticmethod
    def plot_spectral_flux(calculated_FLUX, title="Spectral Flux"):

        if calculated_FLUX is None:
            print("FEHLER: Kein Spektralfluss zum Plotten vorhanden.")
            return  None

        plt.figure()
        plt.plot(calculated_FLUX)
        plt.title(title)
        plt.xlabel("Fensterindex")
        plt.ylabel("Spectral Flux")
        plt.grid()
        plt.show()
        return  None

    
        

         
