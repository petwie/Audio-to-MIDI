import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage

class MidiExport:
    def __init__(self, bpm=120):
        self.bpm = bpm
        self.ticks_per_beat = 480 # Standard-Auflösung für MIDI

    def seconds_to_ticks(self, seconds):
        """Rechnet Sekunden in MIDI-Ticks um basierend auf den BPM."""
        # Formel: Sekunden * (Ticks pro Beat * Beats pro Sekunde)
        beats_per_second = self.bpm / 60.0
        return int(seconds * self.ticks_per_beat * beats_per_second)

    def export_midi(self, onsets_frames, output_path, sample_rate, hop_length):
        """
        Erstellt die MIDI-Datei.
        onsets_frames: Liste der Frame-Indizes, wo Schläge erkannt wurden.
        """
        print(f"Exportiere MIDI nach {output_path} ...")
        
        # 1. MIDI-Objekt und Track erstellen
        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)
        track = MidiTrack()
        mid.tracks.append(track)
        
        # 2. Tempo setzen
        tempo_us = mido.bpm2tempo(self.bpm)
        track.append(MetaMessage('set_tempo', tempo=tempo_us))
        
        # 3. Frames in Sekunden umrechnen und sortieren
        onsets_seconds = [frame * hop_length / sample_rate for frame in onsets_frames]
        onsets_seconds.sort()
        
        # 4. Note-Events schreiben
        # WICHTIG: MIDI nutzt Delta-Time (Zeit seit dem letzten Event)
        last_event_time_ticks = 0
        
        # Wir definieren eine feste Notenlänge (z.B. 0.1 Sekunden)
        note_duration_ticks = self.seconds_to_ticks(0.1)

        for onset_sec in onsets_seconds:
            # Wann passiert der Schlag in absoluten Ticks?
            current_onset_ticks = self.seconds_to_ticks(onset_sec)
            
            # Wie lange müssen wir warten seit dem letzten Event?
            delta_wait = current_onset_ticks - last_event_time_ticks
            
            if delta_wait < 0: delta_wait = 0
            
            # -- NOTE ON (Schlag beginnt) --
            # note=36 (Kick Drum), velocity=100 (Lautstärke), channel=9 (Drums)
            track.append(Message('note_on', note=36, velocity=100, time=delta_wait, channel=9))
            
            # -- NOTE OFF (Schlag endet) --
            # Wir lassen die Note kurz klingen. Die Zeit vergeht währenddessen!
            track.append(Message('note_off', note=36, velocity=0, time=note_duration_ticks, channel=9))
            
            # Update der "letzten Zeit": Wir sind jetzt bei Startzeit + Dauer
            last_event_time_ticks = current_onset_ticks + note_duration_ticks

        # 5. Speichern
        mid.save(output_path)
        print(f"Fertig! {len(onsets_frames)} Noten gespeichert.")