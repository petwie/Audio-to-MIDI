import numpy as np
from scipy.signal import butter, sosfiltfilt

class KickPostCheck:
    def __init__(self, audio, sr, hop_length):
        self.audio = np.asarray(audio, dtype=float)
        self.sr = int(sr)
        self.hop_length = int(hop_length)

    def bandpass(self, f_lo=40, f_hi=180, order=4):
        sos = butter(order, [f_lo, f_hi], btype="bandpass", fs=self.sr, output="sos")
        return sosfiltfilt(sos, self.audio)

    def envelope(self, signal, smooth_ms=10):
        env = np.abs(signal)
        W = max(1, int(self.sr * smooth_ms / 1000))
        kernel = np.ones(W) / W
        return np.convolve(env, kernel, mode="same")

    def filter_peaks(
        self,
        peaks,
        pre_ms=25,
        post_ms=25,
        rise_ratio=1.15,
        abs_rise=0.0,          # optional: absolute Differenzschwelle
        pre_percentile=50,     # 50=Median, 30 ist "tiefer" -> lässt Gruppen eher durch
        post_percentile=95     # 95 statt max -> weniger empfindlich
    ):
        kick_band = self.bandpass()
        env = self.envelope(kick_band)

        pre_samp = max(1, int(self.sr * pre_ms / 1000))
        post_samp = max(1, int(self.sr * post_ms / 1000))

        cleaned = []
        peaks = np.asarray(peaks, dtype=int)

        for frame in peaks:
            center = int(frame * self.hop_length)
            if center <= 0 or center >= len(env):
                continue

            pre0 = max(0, center - pre_samp)
            pre1 = center
            post0 = center
            post1 = min(len(env), center + post_samp)

            if pre1 <= pre0 or post1 <= post0:
                continue

            pre_win = env[pre0:pre1]
            post_win = env[post0:post1]

            pre_e = float(np.percentile(pre_win, pre_percentile))   # Baseline
            post_e = float(np.percentile(post_win, post_percentile)) # Peak-Nähe

            # 1) Ratio-Test
            ok_ratio = (post_e / (pre_e + 1e-12)) >= rise_ratio
            # 2) Optional: Differenz-Test (hilft wenn pre schon hoch ist)
            ok_diff = (post_e - pre_e) >= abs_rise

            if ok_ratio or ok_diff:
                cleaned.append(frame)

        return np.array(cleaned, dtype=int)