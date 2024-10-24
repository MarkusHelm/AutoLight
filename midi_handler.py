import mido

from color_extractor import ColorExtractor

class MidiHandler:
    def __init__(self):
        self.port = mido.open_output(name="AutoLight 1")
        self.SECONDARY_OFFSET = 20
        
    def send_primary_color(self, hue):
        self.port.send(mido.Message("note_on", note=hue, velocity=127))
    def send_secondary_color(self, hue):
        self.port.send(mido.Message("note_on", note=hue+self.SECONDARY_OFFSET, velocity=127))

def main():
    midi = MidiHandler()
    colorex = ColorExtractor()
    print("Primary Colors...")
    for idx, midiHue in enumerate(colorex.AVAILABLE_HUES):
        print(midiHue)
        input()
        midi.send_primary_color(idx)
    print("Secondary Colors...")
    for idx, midiHue in enumerate(colorex.AVAILABLE_HUES):
        print(midiHue)
        input()
        midi.send_secondary_color(idx)
    input()

if __name__ == "__main__":
    main()

