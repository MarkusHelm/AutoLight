import tkinter as tk

import spotify
sp = spotify.Spotify()

import color
import midi

from PIL import Image, ImageTk

colors = [[],[]]

class Window:
    def __init__(self, root):
        #setting title
        root.title("AutoLight")
        #setting window size
        width=380
        height=380
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.lbl_track_cover=tk.Label(root)
        self.lbl_track_cover["bg"] = "#dddddd"
        self.lbl_track_cover.place(x=10,y=10,width=300,height=300)

        self.lbl_track_title=tk.Label(root)
        self.lbl_track_title["justify"] = "center"
        self.lbl_track_title["text"] = "Title"
        self.lbl_track_title["font"] = "Times 14 bold"
        self.lbl_track_title.place(x=10,y=320,width=300,height=30)

        self.lbl_track_artists=tk.Label(root)
        self.lbl_track_artists["justify"] = "center"
        self.lbl_track_artists["text"] = "Artist"
        self.lbl_track_artists["font"] = "Times 10"
        self.lbl_track_artists.place(x=10,y=350,width=300,height=20)

        self.lbl_color_0=tk.Label(root)
        self.lbl_color_0.place(x=320,y=10,width=50,height=50)
        self.lbl_color_1=tk.Label(root)
        self.lbl_color_1.place(x=320,y=60,width=50,height=50)
        self.lbl_color_2=tk.Label(root)
        self.lbl_color_2.place(x=320,y=110,width=50,height=50)
        self.lbl_color_3=tk.Label(root)
        self.lbl_color_3.place(x=320,y=160,width=50,height=50)

        btn_fetch=tk.Button(root)
        btn_fetch["bg"] = "#f0f0f0"
        btn_fetch["justify"] = "center"
        btn_fetch["text"] = "Fetch"
        btn_fetch.place(x=320,y=320,width=50,height=50)
        btn_fetch["command"] = self.btn_fetch_command

    def btn_fetch_command(self):
        if sp.update() is None: return

        self.lbl_track_title["text"] = sp.getTrackName()
        self.lbl_track_artists["text"] = sp.getArtists()

        self.track_cover = ImageTk.PhotoImage(Image.open("img/cover.png"))
        self.lbl_track_cover["image"] = self.track_cover
        
        self.lbl_color_0["bg"] = colors[0][2]
        self.lbl_color_1["bg"] = colors[1][2]

def fetchSpotify():
    root.after(1000, fetchSpotify)
    if sp.update() == True:
        global colors
        colorsNew = color.getColors()
        if colorsNew[0] != colors[0]:
            midi.send(colorsNew[0][0],False)
        if colorsNew[1] != colors[1]:
            midi.send(colorsNew[1][0],True)
        colors = colorsNew
        app.btn_fetch_command()
    

if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    midi = midi.Midi()
    fetchSpotify()
    root.mainloop()