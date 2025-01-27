import automusic
import tkinter as tk
from tkinter import ttk

def on_generate():
    """Function to handle the 'Generate' button click."""
    selected_key = key_var.get()
    selected_mode = mode_var.get()
    num_chords = num_chords_var.get()
    print(f"Key: {selected_key}, Mode: {selected_mode}, Number of Chords: {num_chords}")

    music_key = automusic.note_to_number(selected_key)
    mode_numbers = automusic.diatonic_modes[selected_mode]

    # Add root_number to each element in mode_numbers and ensure it wraps around (mod 12)
    transposed_mode = [(music_key + interval) for interval in mode_numbers]
    print(transposed_mode)


    # Select chord types
    chords = {**automusic.diatonic_triads, **automusic.diatonic_sevenths, **automusic.diatonic_ninths,
              **automusic.diatonic_sus2, **automusic.diatonic_sus4}

    # Generate the chords for the mode by starting from the scale degree
    mode_chords = []
    for degree in range(len(transposed_mode)):
        print(degree)
        scale_degree = transposed_mode[degree]
        print(scale_degree)

        # Look up the chord for this scale degree from the chords dictionary
        # Assuming the chord dictionary is named 'chords' and has keys like "I", "II", etc.
        chord_key = str(degree + 1)  # Chord keys in the dictionary are "1", "2", etc.

        if chord_key in chords:  # Make sure the chord exists in your chords dictionary
            chord_intervals = chords[chord_key]  # e.g., [0, 4, 7] for a major triad
            chord_notes = [(scale_degree + interval) % 12 for interval in chord_intervals]
            mode_chords.append(chord_notes)

    print(f"Key: {selected_key}, Mode: {selected_mode}, Chords: {mode_chords}, Number of Chords: {num_chords}")

    graf = automusic.create_shared_notes_graph(mode_chords)
    # Add your logic here to process these inputs.

    automusic.graph_network(graf)

    # need to figure out how to select a random node
    # automusic.random_walk(graf)

# Create the main tkinter window
root = tk.Tk()
root.title("Chord Generator")

# Variables for user selections
key_var = tk.StringVar()
mode_var = tk.StringVar()
num_chords_var = tk.IntVar()

# Key selection
key_label = ttk.Label(root, text="Select a Key:")
key_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

key_options = [
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
]
key_menu = ttk.OptionMenu(root, key_var, key_options[0], *key_options)
key_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Mode selection
mode_label = ttk.Label(root, text="Select a Mode:")
mode_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

mode_options = [
    "Ionian", "Dorian", "Phrygian", "Lydian",
    "Mixolydian", "Aeolian", "Locrian"
]
mode_menu = ttk.OptionMenu(root, mode_var, mode_options[0], *mode_options)
mode_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Number of chords selection
num_chords_label = ttk.Label(root, text="Number of Chords:")
num_chords_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

num_chords_spinbox = ttk.Spinbox(
    root, from_=1, to=20, textvariable=num_chords_var, width=5
)
num_chords_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Generate button
generate_button = ttk.Button(root, text="Generate", command=on_generate)
generate_button.grid(row=3, column=0, columnspan=2, pady=10)

# Run the tkinter event loop
root.mainloop()