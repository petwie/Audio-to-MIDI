import AudioImport

def main():
    AudioArray, sample_rate = AudioImport.load_audio("../tests/KickLoop_Test1.m4a")

    calculated_stft = AudioImport.calculate_STFT(AudioArray, sample_rate,n_fft=2048, hop_length=512)

    AudioImport.plot_spectrogram(calculated_stft, sample_rate, hop_length=512, title="Drum Loop Test 1 Spectrogram")

if __name__ == "__main__":
    main()