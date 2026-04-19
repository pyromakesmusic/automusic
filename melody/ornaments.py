# ---------------------------------
# SCALE DEGREE <-> SEMITONE HELPERS
# ---------------------------------

def degree_to_semitone(degree, mode="Ionian"):
    """
    Convert scale degree (1-7, wraps allowed) to semitone offset.

    Examples in Ionian:
        1 -> 0
        2 -> 2
        3 -> 4
        8 -> 12
        9 -> 14
        0 -> -1 scale step (below tonic)
    """
    scale = DIATONIC_MODES[mode]

    zero_index = degree - 1
    octave = zero_index // 7
    index = zero_index % 7

    return scale[index] + (12 * octave)


def semitone_to_degree(semitone, mode="Ionian"):
    """
    Approximate reverse lookup:
    Finds nearest matching scale degree for a semitone offset.

    Returns integer degree.
    """
    scale = DIATONIC_MODES[mode]

    octave = semitone // 12
    pitch_class = semitone % 12

    closest_index = min(
        range(len(scale)),
        key=lambda i: abs(scale[i] - pitch_class)
    )

    return closest_index + 1 + (octave * 7)


def degree_note(root_note, degree, mode="Ionian"):
    """
    Convert root MIDI note + scale degree into MIDI note.

    Example:
        degree_note(60, 3, "Ionian") -> 64
    """
    return root_note + degree_to_semitone(degree, mode)


def ornament_from_degree_pattern(
    current_degree,
    pattern,
    root_note,
    total_ticks,
    mode="Ionian"
):
    """
    Generic ornament builder using degree offsets.

    current_degree = current melodic scale degree
    pattern = list like [0,1,-1,0] or [1,2,1]
              values are relative degree movement

    Returns list of (midi_note, duration)
    """
    note_count = len(pattern)
    step = max(1, total_ticks // note_count)

    output = []

    for i, offset in enumerate(pattern):
        degree = current_degree + offset
        midi_note = degree_note(root_note, degree, mode)

        duration = step
        if i == note_count - 1:
            duration = total_ticks - step * (note_count - 1)

        output.append((midi_note, duration))

    return output


# ---------------------------------
# EXAMPLES
# ---------------------------------

def degree_turn(current_degree, root_note, total_ticks, mode="Ionian"):
    # 2,3,1,2 relative to note centered on scale degree 2
    return ornament_from_degree_pattern(
        current_degree,
        [0, 1, -1, 0],
        root_note,
        total_ticks,
        mode
    )


def degree_mordent(current_degree, root_note, total_ticks, mode="Ionian"):
    # 1,2,1 relative
    return ornament_from_degree_pattern(
        current_degree,
        [0, 1, 0],
        root_note,
        total_ticks,
        mode
    )


def degree_trill(current_degree, root_note, total_ticks, mode="Ionian"):
    return ornament_from_degree_pattern(
        current_degree,
        [0, 1, 0, 1, 0, 1],
        root_note,
        total_ticks,
        mode
    )

def trill(main_note, upper_note, total_ticks, repetitions=4):
    """
    Rapid alternation between main note and upper note.
    Returns list of (note, duration) tuples.
    """
    pattern = []
    total_notes = repetitions * 2
    step = max(1, total_ticks // total_notes)

    for i in range(total_notes):
        note = main_note if i % 2 == 0 else upper_note
        pattern.append((note, step))

    return pattern


def mordent(main_note, lower_note, total_ticks):
    """
    Main -> lower neighbor -> main
    """
    step = max(1, total_ticks // 3)

    return [
        (main_note, step),
        (lower_note, step),
        (main_note, total_ticks - 2 * step)
    ]


def turn(main_note, upper_note, lower_note, total_ticks):
    """
    Upper -> main -> lower -> main
    """
    step = max(1, total_ticks // 4)

    return [
        (upper_note, step),
        (main_note, step),
        (lower_note, step),
        (main_note, total_ticks - 3 * step)
    ]


def appoggiatura(grace_note, main_note, total_ticks):
    """
    Leaning note that takes emphasis/time from principal note.
    Longer grace note than acciaccatura.
    """
    grace = max(1, total_ticks // 2)

    return [
        (grace_note, grace),
        (main_note, total_ticks - grace)
    ]


def acciaccatura(grace_note, main_note, total_ticks):
    """
    Very short crushed grace note before principal note.
    """
    grace = max(1, total_ticks // 8)

    return [
        (grace_note, grace),
        (main_note, total_ticks - grace)
    ]