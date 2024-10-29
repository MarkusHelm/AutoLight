from customtkinter import CTk, CTkLabel, CTkButton, CTkFrame, CTkImage, CTkFont
from PIL import Image
from spotify_handler import SpotifyHandler
from color_extractor import ColorExtractor, Color
from midi_handler import MidiHandler
from osc_handler import OscHandler
from beat_detection import BeatDetector
from time import sleep

class AutoLightApp(CTk):
    def __init__(self):
        super().__init__()
        self.title("AutoLight")
        self.geometry("500x400")
        self.resizable(False,False)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.colors = [Color(), Color(), Color()]
        self.last_loudness = 0
        self.dimmers = [0, 0]

        self.colorex = ColorExtractor()
        self.spotify = SpotifyHandler(img_dir="img")
        self.midi = MidiHandler()
        self.osc = OscHandler()
        self.bd = BeatDetector()

        # Add widgets

        self.img_track_cover_paused = CTkImage(light_image=Image.open("img/paused_light.png"), dark_image=Image.open("img/paused_dark.png"), size=(300,300))


        self.lbl_track_cover=CTkLabel(self, text="", width=300, height=300, image=self.img_track_cover_paused)
        self.lbl_track_cover.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky="nsew")
        self.lbl_track_cover.propagate(False)


        self.fr_track_info=CTkFrame(self, width=300, height=85)
        self.fr_track_info.grid(row=2, column=0, padx=5, pady=(0,5), rowspan=2, sticky="new")
        self.fr_track_info.propagate(False)

        self.lbl_track_artists=CTkLabel(self.fr_track_info, text="Artist", font=CTkFont(size=14), width=290, wraplength=290)
        self.lbl_track_artists.pack(side="bottom", padx=5, pady=(0,5), fill="y", expand=True)

        self.lbl_track_title=CTkLabel(self.fr_track_info, text="Title", font=CTkFont(weight="bold", size=16), width=290, wraplength=290)
        self.lbl_track_title.pack(side="bottom", padx=5, pady=5, fill="y", expand=True)


        self.fr_colors=CTkFrame(self, width=115, height=60)
        self.fr_colors.grid(row=0, column=1, padx=(0,5), pady=5, sticky="new")
        self.fr_colors.propagate(False)

        self.lbl_color_0=CTkLabel(self.fr_colors, text="", width=50, height=50, corner_radius=3)
        self.lbl_color_0.grid(row=0, column=0, padx=5, pady=5, sticky="nsw")

        self.lbl_color_1=CTkLabel(self.fr_colors, text="", width=50, height=50, corner_radius=3)
        self.lbl_color_1.grid(row=0, column=1, padx=(0,5), pady=5, sticky="nw")

        self.lbl_color_2=CTkLabel(self.fr_colors, text="", width=20, height=20, corner_radius=3)
        self.lbl_color_2.grid(row=0, column=2, padx=(0,5), pady=5, sticky="es")


        self.fr_track_analysis=CTkFrame(self, width=115)
        self.fr_track_analysis.grid(row=1, column=1, padx=(0,5), pady=(0,5), sticky="nesw")
        self.fr_track_analysis.propagate(False)
        self.fr_track_analysis.grid_columnconfigure(1, weight=1)


        self.lbl_energy=CTkLabel(self.fr_track_analysis, text="Energy", font=CTkFont(size=12), anchor="w")
        self.lbl_energy.grid(row=0, column=0, padx=5, pady=(0,5), sticky="nw")
        self.lbl_energy=CTkLabel(self.fr_track_analysis, text="0 %", font=CTkFont(size=12), anchor="e")
        self.lbl_energy.grid(row=0, column=1, padx=(0,5), pady=(0,5), sticky="ne")

        self.lbl_daceability=CTkLabel(self.fr_track_analysis, text="Dance", font=CTkFont(size=12), anchor="w")
        self.lbl_daceability.grid(row=1, column=0, padx=5, pady=(0,5), sticky="nw")
        self.lbl_daceability=CTkLabel(self.fr_track_analysis, text="0 %", font=CTkFont(size=12), anchor="e")
        self.lbl_daceability.grid(row=1, column=1, padx=(0,5), pady=(0,5), sticky="ne")

        self.lbl_tempo=CTkLabel(self.fr_track_analysis, text="Tempo", font=CTkFont(size=12), anchor="w")
        self.lbl_tempo.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.lbl_tempo=CTkLabel(self.fr_track_analysis, text="0 BPM", font=CTkFont(size=12), anchor="e")
        self.lbl_tempo.grid(row=2, column=1, padx=(0,5), pady=5, sticky="ne")

        self.lbl_loudenss=CTkLabel(self.fr_track_analysis, text="Loud", font=CTkFont(size=12), anchor="w")
        self.lbl_loudenss.grid(row=3, column=0, padx=5, pady=(0,5), sticky="nw")
        self.lbl_loudenss=CTkLabel(self.fr_track_analysis, text="0 %", font=CTkFont(size=12), anchor="e")
        self.lbl_loudenss.grid(row=3, column=1, padx=(0,5), pady=(0,5), sticky="ne")


        self.btn_fetch=CTkButton(self, width=115, text="Fetch", font=CTkFont(weight="bold"), command=self.btn_fetch_command)
        self.btn_fetch.grid(row=2, column=1, padx=(0,5), pady=(0,5), sticky="nesw")

        self.fr_controls=CTkFrame(self, width=115, height=35)
        self.fr_controls.grid(row=3, column=1, padx=(0,5), pady=(0,5), sticky="new")

        self.btn_player_previous=CTkButton(self.fr_controls, text="\u23EE", width=25, height=25,
                                    font=CTkFont(family="Segoe UI Symbol"), command=self.spotify.player_previous)
        self.btn_player_previous.pack(side="left", fill="x", expand=True)

        self.btn_play_pause=CTkButton(self.fr_controls, text="\u23F8", width=25, height=25,
                                font=CTkFont(family="Segoe UI Symbol"), command=self.btn_play_pause_command)
        self.btn_play_pause.pack(side="left", padx=5, fill="x", expand=True)

        self.btn_player_next=CTkButton(self.fr_controls, text="\u23ED", width=25, height=25,
                                font=CTkFont(family="Segoe UI Symbol"), command=self.spotify.player_next)
        self.btn_player_next.pack(side="right", fill="x", expand=True)


        self.osc.send_release_all()
        sleep(1)
        self.midi.start_clock()
        self.fetch_loop()
        self.gui_loop()
        self.bpm_update_loop()
        

    def calculate_dimmers(self, loudness: float) -> tuple[int, int]:
        if loudness < -13.0:
            return [0, 0] # 100%
        if loudness < -10.0:
            return [1, 1] # Soft
        if loudness < -8.0:
            return [2, 1] # Rotate
        if loudness < -7.0:
            return [3, 1] # Even / Odd
        if loudness < -5.0:
            return [4, 1] # L / R / Back
        if loudness < -4.0:
            return [5, 2] # Swipe
        if loudness < -2.0:
            return [6, 2] # Random
        return [7, 2] # In -> Out


    def btn_fetch_command(self):
        self.fetch_spotify()

    def btn_play_pause_command(self):
        if self.spotify.is_playing():
            self.spotify.player_pause()
        else:
            self.spotify.player_play()
        self.update_gui()

    def update_gui(self):
        self.lbl_tempo.configure(text=f"{self.bd.get_spinner()} {round(self.bd.get_bpm(),1)} BPM")
        self.update_dimmer()
        if self.spotify.is_playing():
            self.lbl_track_title.configure(text=self.spotify.get_track_name())
            self.lbl_track_artists.configure(text=self.spotify.get_artists())

            self.img_track_cover = CTkImage(light_image=Image.open("img/cover.png"), dark_image=Image.open("img/cover.png"), size=(300,300))
            self.lbl_track_cover.configure(image=self.img_track_cover)
            self.btn_play_pause.configure(text="\u23F8")
            
            self.lbl_color_0.configure(fg_color=self.colors[0].hex)
            self.lbl_color_1.configure(fg_color=self.colors[1].hex)
            self.lbl_color_2.configure(fg_color=self.colors[2].hex)

            self.lbl_energy.configure(text=f"{round(self.spotify.get_energy()*100, 1)} %")
            self.lbl_daceability.configure(text=f"{round(self.spotify.get_danceability()*100, 1)} %")
            self.lbl_loudenss.configure(text=f"{round(self.spotify.get_section_loudness(), 1)}")
        else:
            self.lbl_track_cover.configure(image=self.img_track_cover_paused)
            self.btn_play_pause.configure(text="\u23F5")

    def update_colors(self):
        new_colors = self.colorex.extract_colors("img/cover_small.png")
        if new_colors[0].id != self.colors[0].id:
            self.osc.send_primary_color(new_colors[0].hue)
        if new_colors[1].id != self.colors[1].id:
            self.osc.send_secondary_color(new_colors[1].hue)
        if new_colors[2].id != self.colors[2].id:
            self.osc.send_scanner_color(new_colors[2].hue)
        self.colors = new_colors

    def update_dimmer(self):
        loudness = self.spotify.get_section_loudness() if self.spotify.is_playing() else -20
        if loudness != self.last_loudness:
            print(f"Loudness Change: {self.last_loudness}->{loudness}")
            self.last_loudness = self.spotify.get_section_loudness()
            dimmers = self.calculate_dimmers(self.last_loudness)
            if dimmers[0] != self.dimmers[0]:
                self.osc.send_par_dimmer(dimmers[0])
            if dimmers[1] != self.dimmers[1]:
                self.osc.send_scanner_dimmer(dimmers[1])
            self.dimmers = dimmers

    def fetch_spotify(self):
        self.spotify.fetch()
        if self.spotify.has_track_changed():
            self.update_colors()
        self.update_gui()

    def fetch_loop(self):
        self.fetch_spotify()
        self.after(1000, self.fetch_loop)

    def gui_loop(self):
        self.update_gui()
        self.after(40, self.gui_loop)

    def bpm_update_loop(self):
        if self.spotify.is_playing():
            if round(self.bd.get_bpm()) != round(self.midi.get_bpm()):
                self.midi.set_bpm(self.bd.get_bpm())
        else:
            self.midi.set_bpm(60)
        self.after(2000, self.bpm_update_loop)
        

    def on_closing(self):
        self.midi.stop_clock()
        self.destroy()

def main():
    app = AutoLightApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()