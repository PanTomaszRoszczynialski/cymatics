import numpy as np

def notes2amps(notes):
    """ Change blompfish notes into blurpish amps """
    # blurp frames per second
    fps = 24

    # blompf ticks per second (this was found empirically wtf)
    tps = 2**5

    # Make sure notes are properly arranged
    notes.sort(key = lambda x: x[1] + x[2])

    # Prepare LO/MI/HI containers
    # Movie length in blompf ticks
    full_len = notes[-1][1] + notes[-1][2]
    # in seconds
    full_len /= 1.0 * tps

    # Finally frames
    full_len *= fps
    full_len = int(full_len)

    # For now we want to create a 3-range visualizer thing
    lo_amp = np.zeros(full_len)
    mi_amp = np.zeros(full_len)
    hi_amp = np.zeros(full_len)

    for note in notes:
        if note[0] < 45:
            sta, end = get_note_framespan(note)
            lo_amp[sta : end] += funfunfun(note)
        elif note[0] < 75:
            sta, end = get_note_framespan(note)
            mi_amp[sta : end] += funfunfun(note)
        else:
            sta, end = get_note_framespan(note)
            hi_amp[sta : end] += funfunfun(note)

    return lo_amp, mi_amp, hi_amp

def funfunfun(note):
    """ Change note into a 1d ADSR kind of function """
    sta, end = get_note_framespan(note)

    # Prepare x axis
    dziedzina = np.linspace(0, 1, end - sta)

    # Make y shape
    out = np.exp(-dziedzina)

    return out

def get_note_framespan(note):
    """ Go from ticks to frames """
    # TODO abstract this out
    tps = 2**5
    fps = 24
    # Ticks
    sta = note[1]
    end = sta + note[2]

    # Seconds .. Frames
    sta /= 1.0 * tps
    end /= 1.0 * tps
    sta *= fps
    end *= fps

    return int(sta), int(end)

