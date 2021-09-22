from plexserver import PlexFrame
import tkinter as tk
from PIL import Image, ImageTk

def load_images():
    d = {}
    d['play'] = ImageTk.PhotoImage(Image.open("images/play.png").resize((24, 24), Image.ANTIALIAS))
    d['forward'] = ImageTk.PhotoImage(Image.open("images/backward.png").resize((24, 24), Image.ANTIALIAS))
    d['backward'] = ImageTk.PhotoImage(Image.open("images/forward.png").resize((24, 24), Image.ANTIALIAS))
    d['pause'] = ImageTk.PhotoImage(Image.open("images/pause.png").resize((24, 24), Image.ANTIALIAS))
    d['none'] = ImageTk.PhotoImage(Image.open("images/nothingplaying.png").resize((240, 240)))
    return d



class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.images = load_images()
        PlexFrame(self).pack(fill='both', expand=True)
        self.mainloop()

    def get_root(self):
        return self


App()
