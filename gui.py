# Local libraries imports
import automusic as amsc

# Standard libraries imports
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import random

def on_closing():
    plt.close('all')
    root.destroy()

def on_generate():
    """Function to handle the 'Generate' button click."""
    selected_key = key_var.get()
    selected_mode = mode_var.get()
    num_chords = num_chords_var.get()
    bpm = bpm_var.get()
    octave = octave_var.get()
    root_note = (octave * 12) + 12

    music_key = amsc.note_to_number(selected_key)
    mode_numbers = amsc.DIATONIC_MODES[selected_mode]

    # Add root_number to each element in mode_numbers and ensure it wraps around (mod 12)
    transposed_mode = [(music_key + interval) % 12 for interval in mode_numbers]


    # Select chord types
    selected_chords_dicts = []

    if triads_var.get():
        selected_chords_dicts.append(amsc.DIATONIC_TRIADS)

    if sevenths_var.get():
        selected_chords_dicts.append(amsc.DIATONIC_SEVENTHS)

    if ninths_var.get():
        selected_chords_dicts.append(amsc.DIATONIC_NINTHS)

    if sus2_var.get():
        selected_chords_dicts.append(amsc.DIATONIC_SUS2)

    if sus4_var.get():
        selected_chords_dicts.append(amsc.DIATONIC_SUS4)


    # Generate the chords for the mode by starting from the scale degree
    mode_chords = {}

    for degree, scale_degree in enumerate(transposed_mode):
        for chord_dict in selected_chords_dicts:
            chord_key = list(chord_dict.keys())[degree]

            if chord_key in chord_dict:
                chord_intervals = chord_dict[chord_key]

                chord_notes = [
                    (music_key + interval) % 12
                    for interval in chord_intervals
                ]

                mode_chords[chord_key] = chord_notes


    graf = amsc.create_shared_notes_graph(mode_chords)
    # Add your logic here to process these inputs.

    amsc.graph_network(graf)

    # need to figure out how to select a random node
    start_node = random.choice(list(graf.nodes))
    walk = amsc.walk_translator(amsc.random_walk(graf, start_node, num_chords), mode_chords)

    print("Random Walk: " + str(walk))

    if filename_var and save_folder:
        print(type(walk))
        print(walk)
        amsc.midi_stepper(bpm=bpm, root_note=root_note, walk_chords=walk, save_folder=save_folder,
                          filename=filename_var.get(), ticks_per_beat=480)

# Create the main tkinter window
root = tk.Tk()
root.title("Chord Generator")

# File saving variables
filename_var = tk.StringVar(value="random_walk")
save_folder = filedialog.askdirectory()

# Variables for user selections
key_var = tk.StringVar()
mode_var = tk.StringVar()
num_chords_var = tk.IntVar(value=4)
octave_var = tk.IntVar(value=4)
bpm_var = tk.IntVar(value=120)


# Chord type checkboxes
triads_var = tk.BooleanVar(value=True)  # Default value set to True
sevenths_var = tk.BooleanVar(value=True)
ninths_var = tk.BooleanVar(value=True)
sus2_var = tk.BooleanVar(value=False)  # Default set to False
sus4_var = tk.BooleanVar(value=False)

# Key selection
key_label = ttk.Label(root, text="Select a Key:")
key_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")


key_menu = ttk.OptionMenu(root, key_var, amsc.KEY_OPTIONS[0], *amsc.KEY_OPTIONS)
key_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Mode selection
mode_label = ttk.Label(root, text="Select a Mode:")
mode_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")


mode_menu = ttk.OptionMenu(root, mode_var, amsc.MODE_OPTIONS[0], *amsc.MODE_OPTIONS)
mode_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Number of chords selection
num_chords_label = ttk.Label(root, text="Number of Chords:")
num_chords_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

num_chords_spinbox = ttk.Spinbox(
    root, from_=1, to=20, textvariable=num_chords_var, width=5
)
num_chords_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# BPM selection
bpm_label = ttk.Label(root, text="BPM:")
bpm_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")

bpm_spinbox = ttk.Spinbox(
    root, from_=40, to=240, textvariable=bpm_var, width=5
)
bpm_spinbox.grid(row=8, column=1, padx=5, pady=5, sticky="w")

# Octave selection
octave_label = ttk.Label(root, text="Octave:")
octave_label.grid(row=11, column=0, padx=5, pady=5, sticky="w")

octave_spinbox = ttk.Spinbox(
    root, from_=1, to=7, textvariable=octave_var, width=5
)
octave_spinbox.grid(row=11, column=1, padx=5, pady=5, sticky="w")

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

filename_label = ttk.Label(root, text="Filename:")
filename_label.grid(row=9, column=0, padx=5, pady=5, sticky="w")

filename_entry = ttk.Entry(root, textvariable=filename_var, width=20)
filename_entry.grid(row=9, column=1, padx=5, pady=5, sticky="w")

save_path_label = ttk.Label(root, text=f"Saving to: {save_folder}")
save_path_label.grid(row=10, column=0, columnspan=2, sticky="w")


# Generate button
generate_button = ttk.Button(root, text="Generate", command=on_generate)
generate_button.grid(row=8, column=3, rowspan=3, columnspan=4, sticky="w")

root.protocol("WM_DELETE_WINDOW", on_closing)
# Run the tkinter event loop
root.mainloop()