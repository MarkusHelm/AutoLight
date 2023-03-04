import mido

from color import colorHues

OFFSET = 20

class Midi:
    def __init__(self):
        self.port = mido.open_output(name="AutoLight 1")

    def send(self, hue, offset=False):
        if offset:
            self.port.send(mido.Message("note_on", note=hue+OFFSET, velocity=127))
        else:
            self.port.send(mido.Message("note_on", note=hue, velocity=127))

if __name__ == "__main__":
    midi = Midi()
    midiHues = colorHues.copy()[:-1]
    print("Primary Colors...")
    for idx, midiHue in enumerate(midiHues):
        print(midiHue)
        input()
        midi.send(idx)
    print("Secondary Colors...")
    for idx, midiHue in enumerate(midiHues):
        print(midiHue)
        input()
        midi.send(OFFSET + idx)
    input()

