import tkinter as tk


class Marquee(tk.Canvas):
    def __init__(self, parent, text, margin=2, borderwidth=1, relief='flat', fps=30, width=240, font=("Courier New", "10", "bold")):
        tk.Canvas.__init__(self, parent, borderwidth=0, highlightthickness=0, relief=relief, bg="#282a2d")
        self.fps = fps

        # start by drawing the text off screen, then asking the canvas
        # how much space we need. Use that to compute the initial size
        # of the canvas. 
        text = self.create_text(0, -1000, text=text, anchor="w", tags=("text",), fill='white', font=font)
        (x0, y0, x1, y1) = self.bbox("text")
        width = width # (x1 - x0) + (2*margin) + (2*borderwidth)
        height = (y1 - y0) + (2*margin) + (2*borderwidth)
        self.configure(width=width, height=height)

        # start the animation
        self.animate()

    def animate(self):
        (x0, y0, x1, y1) = self.bbox("text")
        if x1 < 0 or y0 < 0:
            # everything is off the screen; reset the X
            # to be just past the right margin
            x0 = self.winfo_width()
            y0 = int(self.winfo_height()/2)
            self.coords("text", x0, y0)
        else:
            self.move("text", -1, 0)

        # do again in a few milliseconds
        self.after_id = self.after(int(1000/self.fps), self.animate)

class MarketMarquee(tk.Canvas):
    def __init__(self, parent, data, margin=2, borderwidth=1, relief='flat', fps=240, width=240, font=("Georgia", "24")):
        tk.Canvas.__init__(self, parent, borderwidth=0, highlightthickness=0, relief=relief, bg="#282a2d")
        self.fps = fps

        self.width = width
        i = 0
        colours = {True:"#46e58f", False:"#ec4146"}
        scales = {True:"\u25B2", False:"\u25BC"}
        self.texts = []
        self.bboxs = []
        cache_amount = 0
        for entry in data:
            i += 1
            self.texts.append(self.create_text(width+cache_amount, 0, text="{}  {} ".format(entry['text'].upper(), scales[entry['increase']]), fill=colours[entry['increase']], anchor="nw", tags=("text",), font=font))
            cache_amount = self.bbox("text")
            cache_amount = (cache_amount[2]-cache_amount[0])+100
            self.bboxs.append(cache_amount)
        height = 40
        self.configure(width=width, height=height)

        # start the animation
        self.animate()

    def animate(self):
        
        i = -1
        for text in self.texts:
            self.move(text, -1, 0)
            i += 1

            cache_amount = self.bboxs[i]
            if self.coords(text)[0] < -(cache_amount):

                self.move(text, self.bboxs[-1], 0)
            
    
        self.after_id = self.after(int(1000/self.fps), self.animate)
        
        
      
