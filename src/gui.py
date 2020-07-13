import time
import tkinter as tk
from math import ceil
from urllib.parse import urlparse
from easygui import enterbox
from tkinter.font import Font

from src.image import load_image, process_color, SCALE
from src.webdriver import (
    join_private_game, play_random_game, create_private_game, open_skribbl,
    draw_image, search_image,
)


intro_font_name = 'Fixedsys'
intro_font_size = 20
pad = 2
bdr = 2
bd_l = tk.RIDGE     # tk.GROOVE


class MainUI:
    def __init__(self, app_name, icon, size="520x150", intro='', **kwargs):
        self.kwargs = kwargs
        self.window = tk.Tk()
        self.window.title(app_name)
        self.window.geometry(size)
        try:
            self.window.iconbitmap(icon)
        except tk.TclError:
            self.window.iconbitmap(icon[1:])
        # frame
        self.fr_intro = tk.Frame(self.window)
        self.fr_btn1 = tk.Frame(self.window, bd=bdr, relief=bd_l)
        self.fr_btn2 = tk.Frame(self.window, bd=bdr, relief=bd_l)

        self.layout_intro(intro)
        self.layout_buttons()
        self.image_dict = None

    def layout_intro(self, intro):
        # font
        font_intro = Font(family=intro_font_name, size=intro_font_size)
        font_strike = Font(family=intro_font_name, size=intro_font_size, overstrike=1)
        # layout intro
        intro1, intro2, intro3 = _pre_process_intro(intro)
        lbl_intro1 = tk.Label(self.fr_intro, text=intro1)
        lbl_intro1.configure(font=font_intro)
        lbl_intro1.pack(side='left', expand=True)
        # lbl_intro1.grid(row=0, column=0)
        if intro2 and intro3:
            lbl_intro2 = tk.Label(self.fr_intro, text=intro2)
            lbl_intro2.configure(font=font_strike)
            lbl_intro3 = tk.Label(self.fr_intro, text=intro3)
            lbl_intro3.configure(font=font_intro)
            lbl_intro2.pack(side='left', expand=True, padx=5)
            lbl_intro3.pack(side='left', expand=True)
            # lbl_intro2.grid(row=0, column=1)
            # lbl_intro3.grid(row=0, column=2)
        self.fr_intro.pack(side='top', padx=pad, pady=pad, expand=True, anchor='n')

    def layout_buttons(self):
        # in window
        self.btn_join = tk.Button(self.fr_btn1, text='Join Private Game', command=self.join_private)
        self.btn_random = tk.Button(self.fr_btn1, text='Join Random Game', command=self.join_random)
        self.btn_create = tk.Button(self.fr_btn1, text='Create Private Game', command=self.create_private)
        self.btn_open = tk.Button(self.fr_btn1, text='Just Open Skribbl', command=self.just_open)  # just_open
        # in fr_btn
        self.btn_show_btn = tk.Button(self.fr_btn2, text='New Game', command=self._show_buttons)
        self.fr_draw = tk.Frame(self.fr_btn2)
        self.fr_search = tk.Frame(self.fr_btn2)
        # in fr_draw
        self.btn_draw = tk.Button(self.fr_draw, width=8, text='Draw', command=self.draw)
        self.entry_img = tk.Entry(self.fr_draw, width=60)
        # in fr_search
        self.btn_search = tk.Button(self.fr_search, width=8, text='Search', command=self.search)
        self.entry_search = tk.Entry(self.fr_search, width=20)
        # in window
        self.btn_join.pack(side='top', padx=pad, pady=pad)
        self.btn_random.pack(side='top', padx=pad, pady=pad)
        self.btn_create.pack(side='top', padx=pad, pady=pad)
        self.btn_open.pack(side='top', padx=pad, pady=pad)
        self.fr_btn1.pack(side='top', fill='both', padx=pad, pady=pad, expand=True, anchor='n')
        # in fr_btn
        self.btn_show_btn.grid(row=0, column=0, sticky="NW", padx=5, pady=5)
        self.entry_img.grid(row=0, column=0, padx=pad, pady=pad)
        self.btn_draw.grid(row=0, column=1, padx=pad, pady=pad)
        self.entry_search.grid(row=0, column=0, padx=pad, pady=pad)
        self.btn_search.grid(row=0, column=1, padx=pad, pady=pad)
        self.fr_search.grid(row=1, column=2, sticky="E", padx=pad, pady=pad)
        self.fr_draw.grid(row=2, column=2, sticky="E", padx=pad, pady=pad)

    def join_private(self):
        msg = "Please enter Skribbl.io link:"
        title = "Link required to join a private game!"
        url_input = enterbox(msg=msg, title=title)
        while 1:
            if url_input is None:   # Cancel
                break
            if is_skribbl_url(url_input):
                self._hide_buttons()
                join_private_game(url_input, **self.kwargs)
                break
            msg = "Only Skribbl.io URL will be accepted!\nPlease enter Skribbl.io link:"
            url_input = enterbox(msg=msg, title=title)

    def just_open(self):
        self._hide_buttons()
        open_skribbl(**self.kwargs)

    def create_private(self):
        self._hide_buttons()
        create_private_game(**self.kwargs)

    def join_random(self):
        self._hide_buttons()
        play_random_game(**self.kwargs)

    def draw(self):
        img_url = self.entry_img.get()
        if len(img_url) < 6 and self.image_dict is not None:
            draw_image(self.image_dict)
        elif is_url(img_url):
            img = load_image(img_url, (780 / SCALE, 600 / SCALE))
            img_dict = process_color(img)
            time.sleep(5)
            draw_image(img_dict)

    def search(self):
        item = self.entry_search.get()
        image = search_image(item)
        if image is not None:
            self.image_dict = image

    def start_gui(self):
        self.window.mainloop()

    def _hide_buttons(self):
        self.fr_btn1.pack_forget()
        self.fr_btn2.pack(fill='both', expand=True)

    def _show_buttons(self):
        self.fr_btn2.pack_forget()
        self.fr_btn1.pack(side='top', fill='both', padx=pad, pady=pad, expand=True)


def calc_window_size(intro, size=intro_font_size):
    if intro.lower().find('draw') == -1:
        return str(ceil((len(intro))*0.82*size)) + "x200"
    else:
        return str(ceil((len(intro)+4)*0.82*size)) + "x200"


def is_skribbl_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc == "skribbl.io"])
    except ValueError as ve:
        print(ve)
        return False


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc])
    except ValueError as ve:
        print(ve)
        return False


def _pre_process_intro(intro):
    loc = intro.lower().find('draw')
    if loc == -1:
        return intro, None, None
    else:
        return intro[:loc-1], "Cheat", intro[loc:]
