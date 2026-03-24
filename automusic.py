import random
import networkx as nx
import matplotlib.pyplot as plt
import mido

# Define diatonic TRIADS and seventh chords in C major
TRIADS = {
    'C': ['C', 'E', 'G'],
    'Dm': ['D', 'F', 'A'],
    'Em': ['E', 'G', 'B'],
    'F': ['F', 'A', 'C'],
    'G': ['G', 'B', 'D'],
    'Am': ['A', 'C', 'E'],
    'Bdim': ['B', 'D', 'F']
}

SEVENTHS = {
    'Cmaj7': ['C', 'E', 'G', 'B'],
    'Dm7': ['D', 'F', 'A', 'C'],
    'Em7': ['E', 'G', 'B', 'D'],
    'Fmaj7': ['F', 'A', 'C', 'E'],
    'G7': ['G', 'B', 'D', 'F'],
    'Am7': ['A', 'C', 'E', 'G'],
    'Bm7b5': ['B', 'D', 'F', 'A']
}

MIDI_NOTES = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"}
# Assuming MIDI_NOTES is defined as a list of note names
TEXT_MIDI_NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


# Turn integer 0-255 into the note it represents
def get_note(number):
    note = MIDI_NOTES[number % 12]
    return note

def note_to_number(note):
    """Convert a note name to its corresponding MIDI number."""
    # Find the index of the note in MIDI_NOTES
    if note in TEXT_MIDI_NOTES:
        return TEXT_MIDI_NOTES.index(note)
    else:
        raise ValueError(f"Invalid note: {note}")

DIATONIC_MODES = {
    "Ionian": [0, 2, 4, 5, 7, 9, 11],      # Major scale
    "Dorian": [0, 2, 3, 5, 7, 9, 10],
    "Phrygian": [0, 1, 3, 5, 7, 8, 10],
    "Lydian": [0, 2, 4, 6, 7, 9, 11],
    "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "Aeolian": [0, 2, 3, 5, 7, 8, 10],    # Natural minor scale
    "Locrian": [0, 1, 3, 5, 6, 8, 10]
}

DIATONIC_TRIADS = {
    "I": [0, 4, 7],      # Major triad
    "ii": [2, 5, 9],     # Minor triad
    "iii": [4, 7, 11],   # Minor triad
    "IV": [5, 9, 0],     # Major triad
    "V": [7, 11, 2],     # Major triad
    "vi": [9, 0, 4],     # Minor triad
    "vii°": [11, 2, 5]   # Diminished triad
}

DIATONIC_SEVENTHS = {
    "Imaj7": [0, 4, 7, 11],     # Major seventh
    "ii7": [2, 5, 9, 0],        # Minor seventh
    "iii7": [4, 7, 11, 2],      # Minor seventh
    "IVmaj7": [5, 9, 0, 4],     # Major seventh
    "V7": [7, 11, 2, 5],        # Dominant seventh
    "vi7": [9, 0, 4, 7],        # Minor seventh
    "viiø7": [11, 2, 5, 9]      # Half-diminished seventh
}

DIATONIC_NINTHS = {
    "Imaj9": [0, 4, 7, 11, 2],      # Major ninth
    "ii9": [2, 5, 9, 0, 4],         # Minor ninth
    "iii9": [4, 7, 11, 2, 5],       # Minor ninth
    "IVmaj9": [5, 9, 0, 4, 7],      # Major ninth
    "V9": [7, 11, 2, 5, 9],         # Dominant ninth
    "vi9": [9, 0, 4, 7, 11],        # Minor ninth
    "viiø9": [11, 2, 5, 9, 0]       # Half-diminished ninth
}

DIATONIC_SUS2 = {
    "Isus2": [0, 2, 7],      # Suspended second on the tonic
    "iisus2": [2, 4, 9],     # Suspended second on the second degree
    "iiisus2": [4, 6, 11],   # Suspended second on the third degree
    "IVsus2": [5, 7, 0],     # Suspended second on the fourth degree
    "Vsus2": [7, 9, 2],      # Suspended second on the fifth degree
    "visus2": [9, 11, 4],    # Suspended second on the sixth degree
    "vii°sus2": [11, 1, 5]   # Suspended second on the seventh degree
}

DIATONIC_SUS4 = {
    "Isus4": [0, 5, 7],      # Suspended fourth on the tonic
    "iisus4": [2, 7, 9],     # Suspended fourth on the second degree
    "iiisus4": [4, 9, 11],   # Suspended fourth on the third degree
    "IVsus4": [5, 0, 7],     # Suspended fourth on the fourth degree
    "Vsus4": [7, 2, 9],      # Suspended fourth on the fifth degree
    "visus4": [9, 4, 11],    # Suspended fourth on the sixth degree
    "vii°sus4": [11, 5, 0]   # Suspended fourth on the seventh degree
}
# Merge TRIADS and SEVENTHS into one dictionary of chords
chords = {**TRIADS, **SEVENTHS}

MODE_OPTIONS = [
    "Ionian", "Dorian", "Phrygian", "Lydian",
    "Mixolydian", "Aeolian", "Locrian"
]

KEY_OPTIONS = [
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
]

def create_shared_notes_graph(chords):
    """
    Create a graph where nodes represent chords, and edges are weighted
    by the number of shared notes between chords.

    Parameters:
        chords (dict): A dictionary where keys are chord names and values are lists of notes
                      (integers representing semitones from the root).

    Returns:
        networkx.Graph: The resulting graph with nodes and weighted edges.
    """
    # Function to calculate the number of shared notes between two chords
    def shared_notes(chord1, chord2):
        return len(set(chords[chord1]).intersection(set(chords[chord2])))

    # Create the graph
    graf = nx.Graph()

    # Add nodes for each chord
    for chord in chords.keys():
        graf.add_node(chord)

    # Add weighted edges based on shared notes
    for chord1 in chords:
        for chord2 in chords:
            if chord1 != chord2:
                weight = shared_notes(chord1, chord2)
                if weight > 0:
                    graf.add_edge(chord1, chord2, weight=weight)

    return graf

def graph_network(graf, showing=False):
    # Plot the graph (optional)
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graf, seed=42)
    nx.draw(graf, pos, with_labels=True, node_color='lightblue', font_weight='bold')
    labels = nx.get_edge_attributes(graf, 'weight')
    nx.draw_networkx_edge_labels(graf, pos, edge_labels=labels)
    if showing:
        plt.show()


# Perform a random walk on the graph
def random_walk(graph, start_node, num_steps=10):
    walk = [start_node]
    current_node = start_node

    for _ in range(num_steps):
        neighbors = list(graph.neighbors(current_node))
        weights = [graph[current_node][neighbor]['weight'] for neighbor in neighbors]

        # Randomly select the next chord based on edge weights
        next_node = random.choices(neighbors, weights=weights, k=1)[0]
        walk.append(next_node)
        current_node = next_node

    return walk

def walk_translator(walkies, chords):
    translation = {}
    for step in walkies:
        translation[step] = chords[step]

    return translation

def midi_stepper(bpm, ticks_per_beat, root_note, walk_chords):
    beat_length_ticks = ticks_per_beat
    mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Set tempo
    tempo = mido.bpm2tempo(bpm)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    # Map your 0-11 numbers to MIDI notes (root octave 4 = 60)
    ROOT_NOTE = root_note

    for chord_name, chord_intervals in walk_chords.items():
        chord_notes = [(ROOT_NOTE + interval) for interval in chord_intervals]

        # Note on
        for note in chord_notes:
            track.append(mido.Message('note_on', note=note, velocity=64, time=0))

        # Note off after 1 beat
        for note in chord_notes:
            track.append(mido.Message('note_off', note=note, velocity=64, time=beat_length_ticks))

    # Save MIDI
    mid.save('random_walk.mid')
    print("MIDI file saved as random_walk.mid")