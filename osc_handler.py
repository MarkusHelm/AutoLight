from pythonosc.udp_client import SimpleUDPClient
from color_extractor import ColorExtractor
from time import sleep

OSC_PREFIX = "/AutoLight"
OSC_IP = "localhost"
OSC_PORT = 7000


class OscHandler:
    def __init__(self):
        self.osc_client = SimpleUDPClient(OSC_IP, OSC_PORT)

    def send(self, command: str) -> None:
        self.osc_client.send_message(f"{OSC_PREFIX}/{command}", 1)
        self.osc_client.send_message(f"{OSC_PREFIX}/{command}", 0)

    def send_primary_color(self, hue: int) -> None:
        self.send(f"color/primary/{hue}")

    def send_secondary_color(self, hue: int) -> None:
        self.send(f"color/secondary/{hue}")

    def send_scanner_color(self, color: int) -> None:
        self.send(f"color/scanner/{color}")

    def send_par_dimmer(self, intensity: int) -> None:
        self.send(f"dimmer/par/{intensity}")

    def send_scanner_dimmer(self, intensity: int) -> None:
        self.send(f"dimmer/scanner/{intensity}")

    def send_release_all(self) -> None:
        self.send("release_all")

def main():
    osc = OscHandler()
    colorex = ColorExtractor()

    print("Primary Colors (9)")
    for hue in colorex.AVAILABLE_HUES:
        input(f"Send {colorex.hue_to_string(hue)}?")
        print("Sent.")
        osc.send_primary_color(hue)
    print("Secondary Colors (9)")
    for hue in colorex.AVAILABLE_HUES:
        input(f"Send {colorex.hue_to_string(hue)}?")
        osc.send_secondary_color(hue)
    print("Scanner Colors (RGBW)")
    for hue in colorex.SCANNER_HUES:
        input(f"Send {colorex.hue_to_string(hue)}?")
        osc.send_scanner_color(hue)
    print("Par Dimmers (8)")
    for id in range(8):
        input(f"Send {id}?")
        osc.send_par_dimmer(id)
    print("Scanner Dimmers (3)")
    for id in range(3):
        input(f"Send {id}?")
        osc.send_scanner_dimmer(id)
    print("Release All")
    input("Send release?")
    osc.send_release_all()
    print("Done.")

if __name__ == "__main__":
    main()