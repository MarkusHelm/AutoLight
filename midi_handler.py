import mido
from color_extractor import ColorExtractor
import multiprocessing
import time

class MidiHandler:
    def __init__(self):
        self.SECONDARY_OFFSET = 20
        self.bpm = 128
        #self.running = False
        self.clock_process = None
        
    #def send_primary_color(self, hue):
    #    if self.port is not None:
    #        self.port.send(mido.Message("note_on", note=hue, velocity=127))
    #def send_secondary_color(self, hue):
    #    if self.port is not None:
    #        self.port.send(mido.Message("note_on", note=hue+self.SECONDARY_OFFSET, velocity=127))

    def getMidiPort(self, port_name):
        for port in mido.get_output_names():
            if port_name in port:
                try:
                    return mido.open_output(name=port)
                except OSError:
                    print(f"Could not open MIDI port \"{port}\"!")
                    return None
        print(f"MIDI port \"{port_name}\" not found!")

    def set_bpm(self, bpm):
        self.bpm = bpm if bpm > 0 else 128 # Update the BPM value
        #if self.running:  # Restart the clock to synchronize
        if self.clock_process and self.clock_process.is_alive():
            print(f"Set BPM: {self.bpm}")
            self.stop_clock()
            self.start_clock()

    def get_bpm(self):
        return self.bpm

    def send_clock_signals(self, bpm, port_name):
        port = self.getMidiPort(port_name)
        #while self.running:
        #    if self.bpm < 3:
        #        self.bpm = 128
        quarter_note_duration = 60 / (bpm + 2)
        tick_duration = quarter_note_duration / 24
        while True:
            start_time = time.perf_counter()
            # Send 24 clock ticks per beat (each clock tick is 1/24 of a beat)
            for _ in range(24):
                port.send(mido.Message("clock"))
                elapsed_time = time.perf_counter() - start_time
                time_to_sleep = tick_duration - elapsed_time
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)
                start_time = time.perf_counter()  # Reset start time for the next tick

    def start_clock(self):
        if not self.clock_process or not self.clock_process.is_alive():
            self.clock_process = multiprocessing.Process(
                target=self.send_clock_signals, args=(self.bpm, "AutoLight"))
            self.clock_process.start()

    def stop_clock(self):
        if self.clock_process and self.clock_process.is_alive():
            self.clock_process.terminate()
            self.clock_process.join()

#def main():
#    midi = MidiHandler()
#    colorex = ColorExtractor()
#    print("Primary Colors...")
#    for idx, midiHue in enumerate(colorex.AVAILABLE_HUES):
#        print(midiHue)
#        input()
#        midi.send_primary_color(idx)
#    print("Secondary Colors...")
#    for idx, midiHue in enumerate(colorex.AVAILABLE_HUES):
#        print(midiHue)
#        input()
#        midi.send_secondary_color(idx)
#    input()

if __name__ == "__main__":
    print(mido.get_output_names())

