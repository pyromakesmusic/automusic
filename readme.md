# automusic

A Python-based tool that generates diatonic chord progressions using graph traversal and exports them as MIDI files.

## Features
- Select key and mode (Ionian → Locrian)
- Choose chord types (triads, 7ths, 9ths, sus2, sus4)
- Generates chord progressions using a graph-based random walk
- Exports progressions to MIDI for use in DAWs (e.g., Ableton)
- Simple GUI built with Tkinter
## How It Works
- Builds diatonic chords relative to the tonic
- Constructs a graph where:
* * Nodes = chords 
* * Edges = shared notes between chords
- Performs a weighted/random walk through the graph
- Converts the walk into a chord sequence
- Exports as a MIDI file
## Installation
```
git clone <https://github.com/pyromakesmusic/automusic.git>
cd <automusic>
pip install -r requirements.txt
```
## Usage
- `python gui.py`
- Select save folder
- Select key and mode
- Choose chord types
- Enter number of chords
- Provide a filename
- Click "Generate"

MIDI files are saved to selected folder.

## Example Output
vi → ii → V → I → vi → IV → V
## Current Limitations
- Fixed rhythm (1 chord per beat)
- No voice leading optimization
## Future Improvements
- Rhythmic variation
- Voice leading between chords
## Tech Stack
- Python
- Tkinter
- NetworkX
- Mido (MIDI generation)