from customtkinter import CTk, CTkLabel, CTkButton, CTkFrame, CTkImage, CTkFont
from PIL import Image
from spotify_handler import SpotifyHandler
from color_extractor import ColorExtractor, Color
from midi_handler import MidiHandler

class AutoLightApp(CTk):
    def __init__(self):
        super().__init__()
        self.title("AutoLight")
        self.geometry("380x380")
        self.resizable(False,False)

        self.colors = [Color,Color]

        self.colorex = ColorExtractor()
        self.spotify = SpotifyHandler(img_dir="img")
        self.midi = MidiHandler()

        # Add widgets

        self.img_track_cover_paused = CTkImage(light_image=Image.open("img/paused_light.png"), dark_image=Image.open("img/paused_dark.png"), size=(300,300))

        self.fr_colors=CTkFrame(self)
        self.fr_colors.grid(row=0, column=1, padx=(0,5), pady=5, sticky="nsw")

        self.fr_track_info=CTkFrame(self)
        self.fr_track_info.grid(row=1, column=0, padx=5, pady=(0,5), sticky="new")

        self.lbl_track_cover=CTkLabel(self, text="", width=300, height=300, fg_color=self.fr_colors.cget("fg_color"), image=self.img_track_cover_paused)
        self.lbl_track_cover.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.lbl_track_title=CTkLabel(self.fr_track_info, text="Title", font=CTkFont(weight="bold", size=20))
        self.lbl_track_title.pack(padx=5, fill="x")

        self.lbl_track_artists=CTkLabel(self.fr_track_info, text="Artist", font=CTkFont(size=14))
        self.lbl_track_artists.pack(padx=5, fill="x")

        self.lbl_color_0=CTkLabel(self.fr_colors, text="", width=50, height=50, corner_radius=3)
        self.lbl_color_0.pack(padx=5, pady=5)

        self.lbl_color_1=CTkLabel(self.fr_colors, text="", width=50, height=50, corner_radius=3)
        self.lbl_color_1.pack(padx=5, pady=(0,5))

        self.btn_fetch=CTkButton(self, text="Fetch", width=50, height=50, font=CTkFont(weight="bold"), command=self.btn_fetch_command)
        self.btn_fetch.grid(row=1, column=1, padx=(0,5), pady=(0,5), sticky="nesw")

        self.loop()

    def btn_fetch_command(self):
        self.fetch_spotify()

    def update_gui(self):
        if self.spotify.is_playing():
            self.lbl_track_title.configure(text=self.spotify.get_track_name())
            self.lbl_track_artists.configure(text=self.spotify.get_artists())

            self.img_track_cover = CTkImage(light_image=Image.open("img/cover.png"), dark_image=Image.open("img/cover.png"), size=(300,300))
            self.lbl_track_cover.configure(image=self.img_track_cover)
            
            self.lbl_color_0.configure(fg_color=self.colors[0].hex)
            self.lbl_color_1.configure(fg_color=self.colors[1].hex)
        else:
            self.lbl_track_cover.configure(image=self.img_track_cover_paused)

    def update_colors(self):
        new_colors = self.colorex.extract_2_colors("img/cover_small.png")
        if new_colors[0] != self.colors[0]:
            self.midi.send_primary_color(new_colors[0].id)
        if new_colors[1] != self.colors[1]:
            self.midi.send_secondary_color(new_colors[1].id)
        self.colors = new_colors

    def fetch_spotify(self):
        self.spotify.fetch()
        if self.spotify.has_track_changed():
            self.update_colors()
        self.update_gui()

    def loop(self):
        self.fetch_spotify()
        self.after(1000, self.loop)


    

def main():
    app = AutoLightApp()
    app.mainloop()

if __name__ == "__main__":
    main()