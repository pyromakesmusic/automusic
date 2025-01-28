import automusic as amsc
import tkinter as tk
from tkinter import ttk

#def on_generate(triads, sevenths, ninths, sus2, sus4):
def on_generate():
    """Function to handle the 'Generate' button click."""
    selected_key = key_var.get()
    selected_mode = mode_var.get()
    num_chords = num_chords_var.get()

    music_key = amsc.note_to_number(selected_key)
    mode_numbers = amsc.diatonic_modes[selected_mode]

    # Add root_number to each element in mode_numbers and ensure it wraps around (mod 12)
    transposed_mode = [(music_key + interval) for interval in mode_numbers]


    # Select chord types
    selected_chords_dicts = [amsc.diatonic_triads, amsc.diatonic_sevenths, amsc.diatonic_ninths,
              amsc.diatonic_sus2, amsc.diatonic_sus4]


    # Generate the chords for the mode by starting from the scale degree
    mode_chords = {}
    for degree in range(len(transposed_mode)):
        scale_degree = transposed_mode[degree]

        # Iterate through each selected chord dictionary
        for chord_dict in selected_chords_dicts:  # This list contains the selected chord dictionaries (triads, sevenths, etc.)
            chord_key = list(chord_dict.keys())[degree]  # Get the chord corresponding to this scale degree

            if chord_key in chord_dict:  # Check if the chord exists in the current dictionary
                chord_intervals = chord_dict[chord_key]  # Get the intervals for the chord (e.g., [0, 4, 7] for a triad)
                chord_notes = [(scale_degree + interval) % 12 for interval in
                               chord_intervals]  # Generate the chord notes
                mode_chords[chord_key] = chord_notes  # Add the chord notes to the mode_chords list


    graf = amsc.create_shared_notes_graph(mode_chords)
    # Add your logic here to process these inputs.

    amsc.graph_network(graf)

    # need to figure out how to select a random node
    walk = amsc.random_walk(graf, "Imaj7", num_chords)

    print("Random Walk: " + str(amsc.walk_translator(walk, mode_chords)))

# Create the main tkinter window
root = tk.Tk()
root.title("Chord Generator")

# Variables for user selections
key_var = tk.StringVar()
mode_var = tk.StringVar()
num_chords_var = tk.IntVar()


# Chord type checkboxes
triads_var = tk.BooleanVar(value=True)  # Default value set to True
sevenths_var = tk.BooleanVar(value=True)
ninths_var = tk.BooleanVar(value=True)
sus2_var = tk.BooleanVar(value=False)  # Default set to False
sus4_var = tk.BooleanVar(value=False)

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


# Add checkboxes for chord types
triads_checkbox = tk.Checkbutton(root, text="Triads", variable=triads_var)
triads_checkbox.grid(row=3, column=0, sticky="w")

sevenths_checkbox = tk.Checkbutton(root, text="Sevenths", variable=sevenths_var)
sevenths_checkbox.grid(row=4, column=0, sticky="w")

ninths_checkbox = tk.Checkbutton(root, text="Ninths", variable=ninths_var)
ninths_checkbox.grid(row=5, column=0, sticky="w")

sus2_checkbox = tk.Checkbutton(root, text="Suspended 2", variable=sus2_var)
sus2_checkbox.grid(row=6, column=0, sticky="w")

sus4_checkbox = tk.Checkbutton(root, text="Suspended 4", variable=sus4_var)
sus4_checkbox.grid(row=7, column=0, sticky="w")


# Generate button
generate_button = ttk.Button(root, text="Generate", command=on_generate)
generate_button.grid(row=8, column=3, rowspan=3, columnspan=4, sticky="w")

# Run the tkinter event loop
root.mainloop()