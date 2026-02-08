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

        print(f"DEBUG: Exportiere mit SR={sample_rate}, Hop={hop_length}")
        
        # 1. Frames in Sekunden umrechnen
        onsets_seconds = [frame * hop_length / sample_rate for frame in onsets_frames]
        onsets_seconds.sort()

        # WICHTIG: Wir brauchen absolute Ticks für alle Startzeiten
        onset_ticks = [self.seconds_to_ticks(t) for t in onsets_seconds]
        
        # Standard-Länge einer Note (z.B. 0.1s)
        max_note_duration = self.seconds_to_ticks(0.1)
        
        last_midi_time = 0 # Wo steht der MIDI-Cursor gerade?

        for i in range(len(onset_ticks)):
            current_start = onset_ticks[i]
            
            # --- Schritt A: Wie lang darf diese Note sein? ---
            # Wenn es einen nächsten Schlag gibt, darf die Note nicht länger sein als die Lücke dorthin.
            if i < len(onset_ticks) - 1:
                next_start = onset_ticks[i+1]
                duration = min(max_note_duration, next_start - current_start)
                # Sicherheitsnetz: Mindestens 1 Tick lang, sonst hört man nichts
                if duration < 1: duration = 1
            else:
                # Letzte Note darf voll ausklingen
                duration = max_note_duration

            # --- Schritt B: Delta zum Start berechnen ---
            # Wie viel Zeit vergeht vom Ende des letzten Events bis zum Start von diesem?
            delta_on = current_start - last_midi_time
            
            # Sicherheitsnetz gegen negative Deltas (falls Sortierung o.ä. versagt)
            if delta_on < 0: delta_on = 0
            
            # Note On schreiben
            track.append(Message('note_on', note=36, velocity=100, time=delta_on, channel=9))
            
            # Note Off schreiben (Delta ist hier die Dauer der Note selbst)
            track.append(Message('note_off', note=36, velocity=0, time=duration, channel=9))
            
            # --- Schritt C: Cursor aktualisieren ---
            # Der Cursor steht jetzt bei: Startzeit + Dauer der Note
            last_midi_time = current_start + duration

        mid.save(output_path)
        print(f"Fertig! {len(onsets_frames)} Noten gespeichert.")


        # import mido
# from mido import MidiFile, MidiTrack, Message, MetaMessage

# class MidiExport:
#     def __init__(self, bpm=120):
#         self.bpm = bpm
#         self.ticks_per_beat = 480 # Standard-Auflösung für MIDI

#     def seconds_to_ticks(self, seconds):
#         """Rechnet Sekunden in MIDI-Ticks um basierend auf den BPM."""
#         beats_per_second = self.bpm / 60.0
#         return int(seconds * self.ticks_per_beat * beats_per_second)

#     def _write_instrument_track(self, track, onsets_frames, note_number, sample_rate, hop_length):
#         """
#         Interne Hilfsfunktion: Schreibt die Noten für EIN Instrument in den gegebenen Track.
#         """
#         # 1. Tempo setzen (muss in jedem Track stehen oder im ersten, hier sicherheitshalber)
#         tempo_us = mido.bpm2tempo(self.bpm)
#         track.append(MetaMessage('set_tempo', tempo=tempo_us))
        
#         # 2. Leere Listen abfangen
#         if not onsets_frames:
#             return

#         # 3. Frames in Sekunden umrechnen und sortieren
#         onsets_seconds = [frame * hop_length / sample_rate for frame in onsets_frames]
#         onsets_seconds.sort()

#         # 4. In Ticks umrechnen
#         onset_ticks = [self.seconds_to_ticks(t) for t in onsets_seconds]
        
#         # Standard-Länge einer Note (0.1s)
#         max_note_duration = self.seconds_to_ticks(0.1)
        
#         last_midi_time = 0 # Cursor für DIESEN Track

#         for i in range(len(onset_ticks)):
#             current_start = onset_ticks[i]
            
#             # --- Dauer berechnen (Noten kürzen, falls der nächste Schlag zu schnell kommt) ---
#             if i < len(onset_ticks) - 1:
#                 next_start = onset_ticks[i+1]
#                 duration = min(max_note_duration, next_start - current_start)
#                 if duration < 1: duration = 1
#             else:
#                 duration = max_note_duration

#             # --- Delta Time berechnen ---
#             delta_on = current_start - last_midi_time
#             if delta_on < 0: delta_on = 0
            
#             # Note On (Kanal 9 = MIDI Kanal 10 für Drums)
#             track.append(Message('note_on', note=note_number, velocity=100, time=delta_on, channel=9))
            
#             # Note Off
#             track.append(Message('note_off', note=note_number, velocity=0, time=duration, channel=9))
            
#             # Cursor aktualisieren
#             last_midi_time = current_start + duration

#     def export_midi(self, kick_frames, snare_frames, hihat_frames, output_path, sample_rate, hop_length):
#         """
#         Erstellt eine MIDI-Datei mit 3 separaten Tracks für Kick, Snare und HiHat.
#         Alle Instrumente landen auf Kanal 10 (Drums).
#         """
#         print(f"Exportiere Multi-Track MIDI nach {output_path} ...")
#         print(f"DEBUG: SR={sample_rate}, Hop={hop_length}, BPM={self.bpm}")
        
#         # MIDI File erstellen (Format 1 ist Standard bei mido, erlaubt mehrere Tracks)
#         mid = MidiFile(ticks_per_beat=self.ticks_per_beat)

#         # --- TRACK 1: KICK (Note 36) ---
#         track_kick = MidiTrack()
#         track_kick.name = "Kick Drum"
#         mid.tracks.append(track_kick)
#         self._write_instrument_track(track_kick, kick_frames, 36, sample_rate, hop_length)

#         # --- TRACK 2: SNARE (Note 38) ---
#         track_snare = MidiTrack()
#         track_snare.name = "Snare Drum"
#         mid.tracks.append(track_snare)
#         self._write_instrument_track(track_snare, snare_frames, 38, sample_rate, hop_length)
        
#         # --- TRACK 3: HI-HAT (Note 42 - Closed HiHat) ---
#         track_hihat = MidiTrack()
#         track_hihat.name = "Hi-Hat"
#         mid.tracks.append(track_hihat)
#         self._write_instrument_track(track_hihat, hihat_frames, 42, sample_rate, hop_length)

#         # Speichern
#         mid.save(output_path)
#         print(f"Fertig! MIDI gespeichert.")