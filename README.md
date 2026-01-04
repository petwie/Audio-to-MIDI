# Audio-to-MIDI
Projekt in dem wir aus einem Audio, eine MIDI Standart Datei extrahieren.
## Projekt Plan (Gantt)

```mermaid

%%{init: {'gantt': {
  'leftPadding': 170,
  'rightPadding': 10,
  'topPadding': 90,
  'titleTopMargin': 10,
  'barHeight': 22,
  'barGap': 10,
  'fontSize': 10,
  'sectionFontSize': 13,
  'axisFormat': '%d.%m.',
  'todayMarker': 'off'
}} }%%

gantt
  title Audio zu MIDI
  dateFormat YYYY-MM-DD
  axisFormat %d.%m.
  tickInterval 1d

  section Infrastruktur (Ph1, PE)
  Repo anlegen                 :a1, 2026-01-03, 2d
  .gitignore (Python)          :a2, 2026-01-03, 2d
  requirements.txt             :a3, after a2, 3d

  section Testdaten (Ph1, AA)
  20 Audio-Clips               :a4, 2026-01-03, 2d
  Labels K/S/B/C               :a5, after a4, 3d
  Schlagzeitpunkte (Doku)      :a6, after a4, 3d

  section Audio-Import (Ph1, AA)
  WAV laden                    :a7, 2026-01-08, 2d
  FFT berechnen                :a8, after a7, 3d
  Plot zur Prüfung             :a9, after a7, 3d

  section Spectral-Flux (Ph2, PE)
  Log-Magnitude                :a10, 2026-01-11, 8d
  Frame-Differenz              :a11, 2026-01-11, 8d
  Halbwellen-Gleichrichtung    :a12, 2026-01-11, 8d

  section MIDI-Export (Ph2, AA)
  Sek → MIDI-Ticks        :a13, after a8, 2d
  MIDI schreiben               :a14, after a13, 3d
  MIDI validieren              :a15, after a14, 1d

  section Peak/Schwellwert (Ph2, AA)
  Peak-Suche                   :a16, after a15, 3d
  Adaptiver Schwellwert        :a17, after a15, 3d

  section Integration & Test (Ph2, PE+AA)
  Integration Fun.         :a18, after a17, 2d
  Funktionstests               :a19, after a18, 2d

  section Frequenz - Analyse(Ph,3 Aaron)
  Mapping FFT- Bins             :a20, after a19,3d
  Def. Trennfrequenz            :a21,after a19,3d

  section Multi-Band Flux Implimentation(Peter)
  Zwei Flux-kurfen              :a22,after a19,3d
  flux_loww/high                :a23,after a19,3d

  section Erweitere MIDI export (Aaron)
  Export Noten                  :a24, after a21,2026-01-31
  Exp Midi Standart      :a25, after a21,2026-01-31