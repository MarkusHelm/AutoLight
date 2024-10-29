import pyaudio as pa
import numpy as np
import aubio
from time import sleep

import midi_handler

class BeatDetector:
    def __init__(self, buf_size: int = 128, verbose: bool = False, midi_handler: midi_handler.MidiHandler = None):
        self.buf_size: int = buf_size
        self.verbose: bool = verbose
        self.midi = midi_handler

        self.spinner = "▚▞"
        self.spinner_state = 0

        self.pyaudio = pa.PyAudio()
        samplerate = 44100

        self.stream = self.pyaudio.open(
            format=pa.paFloat32,
            channels=1,
            rate=samplerate,
            input=True,
            frames_per_buffer=self.buf_size,
            stream_callback=self._pyaudio_callback,
            input_device_index=None
        )

        fft_size = self.buf_size * 2
        self.tempo = aubio.tempo("default", fft_size, self.buf_size, samplerate)

    def _pyaudio_callback(self, in_data, frame_count, time_info, status):
        signal = np.frombuffer(in_data, dtype=np.float32)
        
        beat = self.tempo(signal)
        if beat[0]:
            self.spinner_state = (self.spinner_state + 1) % len(self.spinner)
            if self.verbose:
                self.print_bpm()
        return None, pa.paContinue
    
    def get_bpm(self) -> float:
        return self.tempo.get_bpm()
    
    def get_spinner(self) -> str:
        return self.spinner[self.spinner_state]
    
    def print_bpm(self) -> None:
        print(f"{self.get_spinner()}\t{self.get_bpm():.1f} BPM")
        

    def __del__(self):
        self.stream.close()
        self.pyaudio.terminate()


def list_devices():
    print("Listing all available input devices:\n")
    pyaudio = pa.PyAudio()
    info = pyaudio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if (pyaudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print(f"[{i}] {pyaudio.get_device_info_by_host_api_device_index(0, i).get('name')}")

    print("\nUse the number in the square brackets as device index")


def main():
    BeatDetector(verbose=True)
    while True:
        sleep(1)

if __name__ == "__main__":
    main()
