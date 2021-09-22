from plexapi.myplex import MyPlexAccount
from marquee import Marquee
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading


baseurl = 'http://plex.kasper.net:32400'
account = MyPlexAccount('xerpplex112419@gmail.com', 'jaffacake8')
plex = account.resource('plex').connect()


class PlexServer:
    def get_metadata():
        d = {}
        try:
            session = plex.sessions()[0]
            d['title'] = session.title
            d['artist'] = session.artist().title
            d['album'] = session.album().title
        except Exception as e:
            print(str(e))
            pass
        return d
        
    def get_album_art():
        try:
            session = plex.sessions()[0]
            artworkUrl = session.album().thumbUrl
            response = requests.get(artworkUrl)
            img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((240, 240), Image.ANTIALIAS))
            return img
        except Exception as e:
            img = ImageTk.PhotoImage(Image.open("nothingplaying.png").resize((240, 240), Image.ANTIALIAS))
            return img
        
    def isplaying():
        for session in plex.sessions():
            data = session.players[0].state
            if data in "playing":
                return True
            else:
                return False
        
    def skip_forward():
        for client in plex.clients():
            client._baseurl = baseurl
            client.skipNext()
            
    def skip_backward():
        for client in plex.clients():
            client._baseurl = baseurl
            client.skipPrevious()
        
    def pause_media():
        for client in plex.clients():
            client._baseurl = baseurl
            client.pause()
            
    def play_media():
        for client in plex.clients():
            client._baseurl = baseurl
            client.play()
    


class PlexFrame(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, width=240, height=320, bg='white')
        self.art_image = None
        self.title = ""
        self.button = None
        self.needs_replacing = True
        self.marquee_text = "Marquee"
        self.marquee = tk.Label(self)
        self.marquee.place(x=-1000, y=-1000)
        self.move(self.create_rectangle(240, 320, 0, 0, fill='#282a2d'), 0, 0)
        forward = self.create_image(180, 290, image=self.get_root().images['forward'])
        self.tag_bind(forward, "<Button-1>", lambda event=None: self.skip("forward"))
        backward = self.create_image(60, 290, image=self.get_root().images['backward'])
        self.tag_bind(backward, "<Button-1>", lambda event=None: self.skip("backward"))
        thread = threading.Thread(target=lambda: self.mainloop(loop=True)); self.after(1000, lambda: thread.start())
        
    def skip(self, mode):
        if mode in "forward":
            thread = threading.Thread(target=lambda: PlexServer.skip_forward()); thread.start()
        else:
            thread = threading.Thread(target=lambda: PlexServer.skip_backward()); thread.start()
        #self.after(5000, self.mainloop)
        
    def update_playing(self, mode):
        if mode in "pause":
            thread = threading.Thread(target=lambda: PlexServer.pause_media()); thread.start()
            thread = threading.Thread(target=lambda: self.check_playing(False)); thread.start()
        else:
            thread = threading.Thread(target=lambda: PlexServer.play_media()); thread.start()
            thread = threading.Thread(target=lambda: self.check_playing(False)); thread.start()
            
        
    def check_playing(self, data=False):
        self.delete(self.button)
        if data:
            self.button = self.create_image(120, 290, image=self.get_root().images['pause'], anchor='c')
            self.tag_bind(self.button, "<Button-1>", lambda event=None: self.update_playing("pause"))
        else:
            self.button = self.create_image(120, 290, image=self.get_root().images['play'], anchor='c') 
            self.tag_bind(self.button, "<Button-1>", lambda event=None: self.update_playing("play"))
        
    def mainloop(self, loop=False):
        self.check_playing(data=PlexServer.isplaying())
        data = PlexServer.get_metadata()
        try:
            if not self.title == data['title']:
                self.has_changed = True
                self.title = data['title']
                self.artist = data['artist']
                self.album = data['album']
                self.delete(self.art_image)
                self.image = PlexServer.get_album_art()
                self.art_image = self.create_image(0, 0, anchor='nw', image=self.image)
                self.marquee.place_forget()
                self.marquee = Marquee(self, text="{}    {} - {}".format(self.title, self.artist, self.album), borderwidth=1, relief="sunken")
                self.marquee.place(x=0, y=235)
                self.needs_replacing =True
        except KeyError as e:
            self.title = random.random()
            if self.needs_replacing:
                self.needs_replacing = False
                self.marquee.place_forget()
                self.marquee = Marquee(self, text="No Track Playing", borderwidth=1, relief="sunken")
                self.marquee.place(x=0, y=235)
                self.delete(self.art_image)
                self.art_image = self.create_image(0, 0, anchor='nw', image=self.get_root().images['none'])
        if loop:
            self.after(3000, lambda:threading.Thread(target=lambda: self.mainloop(loop=True)).start())

        
    def get_root(self):
        return self.master.get_root()

