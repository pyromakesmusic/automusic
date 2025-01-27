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

# Merge triads and sevenths into one dictionary of chords
chords = {**triads, **sevenths}


# Calculate the number of shared notes between each pair of chords
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

# Plot the graph (optional)
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
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
progression = random_walk(G, 'C', num_steps=10)
print("Random Chord Progression:", progression)