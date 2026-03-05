import numpy as np
import matplotlib.pyplot as plt

class PeakPicking:
    def __init__(self, flux_array):
        self.flux = flux_array
        self.onsets = []        # Liste der gefundenen Indizes
        self.threshold_curve = [] # Zum Speichern der berechneten Schwelle

    def calculate_adaptive_threshold(self, window_size):
        """
        Berechnet den gleitenden Durchschnitt manuell mittels Faltung.
        """
        # Filter-Kernel
        kernel = np.ones(window_size) / window_size
        
        # Faltung anwenden
        # 'same' sorgt dafür, dass das Ausgangs-Array gleich lang bleibt wie das Eingangs-Array.
        moving_avg = np.convolve(self.flux, kernel, mode='same')
        
        # Offset (Delta) addieren
        deltas = self.calculate_delta(window_size, 3)
        for i in range(len(moving_avg)):
            delta_index = int(i / window_size)
            if delta_index < len(deltas):
                moving_avg[i] += deltas[delta_index]

        self.threshold_curve = moving_avg
        
        return self.threshold_curve

    def find_peaks(self, window_size,  wait):
        """
        Findet Peaks, die über dem adaptiven Threshold liegen.
        wait: Mindestabstand in Frames (Debouncing).
        """
        
        # Threshold berechnen
        thresholds = self.calculate_adaptive_threshold(window_size)
        
        found_peaks = []
        last_peak_index = -wait  # Initialisierung für Debouncing
        
        n_frames = len(self.flux)

        for i in range(1, n_frames - 1):
            
            current_val = self.flux[i]
            current_thresh = thresholds[i]
            
            # Bedingung A: Ist es überhaupt laut genug? (Über Threshold)
            if current_val > current_thresh:
                
                # Bedingung B: Ist es eine lokale Spitze? (Größer als Nachbarn)
                if current_val > self.flux[i-1] and current_val > self.flux[i+1]:
                    
                    # Bedingung C: Haben wir lange genug gewartet? (Debouncing)
                    if (i - last_peak_index) > wait:
                        
                        found_peaks.append(i)
                        last_peak_index = i
        
        self.onsets = np.array(found_peaks)
        print(f"Manuelles Peak Picking: {len(self.onsets)} Onsets gefunden.")
        return self.onsets

    def plot_results(self):
        if len(self.threshold_curve) == 0:
            print("Bitte zuerst find_peaks() aufrufen.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(self.flux, label='Spectral Flux', color='blue', alpha=0.6)
        plt.plot(self.threshold_curve, label='Adaptiver Threshold', color='green', linestyle='--')
        
        if len(self.onsets) > 0:
            # Wir plotten rote Kreuze an den gefundenen Stellen
            plt.plot(self.onsets, self.flux[self.onsets], "x", color='red', markersize=10, label='Erkannte Schläge')
            
        plt.title("Ergebnis: Manuelles Peak Picking")
        plt.xlabel("Zeit (Frames)")
        plt.ylabel("Flux Amplitude")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    def calculate_delta(self, window_size, multiplier):

        len_flux = len(self.flux)
        delta_values = np.zeros(int(np.ceil(len_flux/window_size)))
        for i in range(len(delta_values)):
            start = i * window_size
            end = min((i + 1) * window_size, len_flux)
            delta_values[i] = np.mean(self.flux[start:end]) * multiplier

        return delta_values