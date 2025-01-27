import random
import networkx as nx
import matplotlib.pyplot as plt

# Define diatonic triads and seventh chords in C major
triads = {
    'C': ['C', 'E', 'G'],
    'Dm': ['D', 'F', 'A'],
    'Em': ['E', 'G', 'B'],
    'F': ['F', 'A', 'C'],
    'G': ['G', 'B', 'D'],
    'Am': ['A', 'C', 'E'],
    'Bdim': ['B', 'D', 'F']
}

sevenths = {
    'Cmaj7': ['C', 'E', 'G', 'B'],
    'Dm7': ['D', 'F', 'A', 'C'],
    'Em7': ['E', 'G', 'B', 'D'],
    'Fmaj7': ['F', 'A', 'C', 'E'],
    'G7': ['G', 'B', 'D', 'F'],
    'Am7': ['A', 'C', 'E', 'G'],
    'Bm7b5': ['B', 'D', 'F', 'A']
}

midi_notes = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"}

# Turn integer 0-255 into the note it represents
def get_note(number):
    note = midi_notes[number % 12]
    return note

diatonic_modes = {
    "Ionian": [0, 2, 4, 5, 7, 9, 11],      # Major scale
    "Dorian": [0, 2, 3, 5, 7, 9, 10],
    "Phrygian": [0, 1, 3, 5, 7, 8, 10],
    "Lydian": [0, 2, 4, 6, 7, 9, 11],
    "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "Aeolian": [0, 2, 3, 5, 7, 8, 10],    # Natural minor scale
    "Locrian": [0, 1, 3, 5, 6, 8, 10]
}

diatonic_triads = {
    "I": [0, 4, 7],      # Major triad
    "ii": [2, 5, 9],     # Minor triad
    "iii": [4, 7, 11],   # Minor triad
    "IV": [5, 9, 0],     # Major triad
    "V": [7, 11, 2],     # Major triad
    "vi": [9, 0, 4],     # Minor triad
    "vii°": [11, 2, 5]   # Diminished triad
}

diatonic_sevenths = {
    "Imaj7": [0, 4, 7, 11],     # Major seventh
    "ii7": [2, 5, 9, 0],        # Minor seventh
    "iii7": [4, 7, 11, 2],      # Minor seventh
    "IVmaj7": [5, 9, 0, 4],     # Major seventh
    "V7": [7, 11, 2, 5],        # Dominant seventh
    "vi7": [9, 0, 4, 7],        # Minor seventh
    "viiø7": [11, 2, 5, 9]      # Half-diminished seventh
}

diatonic_ninths = {
    "Imaj9": [0, 4, 7, 11, 2],      # Major ninth
    "ii9": [2, 5, 9, 0, 4],         # Minor ninth
    "iii9": [4, 7, 11, 2, 5],       # Minor ninth
    "IVmaj9": [5, 9, 0, 4, 7],      # Major ninth
    "V9": [7, 11, 2, 5, 9],         # Dominant ninth
    "vi9": [9, 0, 4, 7, 11],        # Minor ninth
    "viiø9": [11, 2, 5, 9, 0]       # Half-diminished ninth
}

diatonic_sus2 = {
    "Isus2": [0, 2, 7],      # Suspended second on the tonic
    "ii sus2": [2, 4, 9],     # Suspended second on the second degree
    "iiisus2": [4, 6, 11],   # Suspended second on the third degree
    "IVsus2": [5, 7, 0],     # Suspended second on the fourth degree
    "Vsus2": [7, 9, 2],      # Suspended second on the fifth degree
    "visus2": [9, 11, 4],    # Suspended second on the sixth degree
    "vii°sus2": [11, 1, 5]   # Suspended second on the seventh degree
}

diatonic_sus4 = {
    "Isus4": [0, 5, 7],      # Suspended fourth on the tonic
    "iisus4": [2, 7, 9],     # Suspended fourth on the second degree
    "iiisus4": [4, 9, 11],   # Suspended fourth on the third degree
    "IVsus4": [5, 0, 7],     # Suspended fourth on the fourth degree
    "Vsus4": [7, 2, 9],      # Suspended fourth on the fifth degree
    "visus4": [9, 4, 11],    # Suspended fourth on the sixth degree
    "vii°sus4": [11, 5, 0]   # Suspended fourth on the seventh degree
}
# Merge triads and sevenths into one dictionary of chords
chords = {**triads, **sevenths}

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
    G = nx.Graph()

    # Add nodes for each chord
    for chord in chords.keys():
        G.add_node(chord)

    # Add weighted edges based on shared notes
    for chord1 in chords:
        for chord2 in chords:
            if chord1 != chord2:
                weight = shared_notes(chord1, chord2)
                if weight > 0:
                    G.add_edge(chord1, chord2, weight=weight)

    return G

def graph_network(graf):
    # Plot the graph (optional)
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graf, seed=42)
    nx.draw(graf, pos, with_labels=True, node_color='lightblue', font_weight='bold')
    labels = nx.get_edge_attributes(graf, 'weight')
    nx.draw_networkx_edge_labels(graf, pos, edge_labels=labels)
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


# Generate a random chord progression starting from C
def make_progression(graf, num):
    progression = random_walk(graf, 'C', num_steps=num)
    print("Random Chord Progression:", progression)
    return progression