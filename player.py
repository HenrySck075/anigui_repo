"""vlc media player; based off example in vlc repo:
`http://git.videolan.org/?p=vlc/bindings/python.git;a=commit;h=HEAD`
See also:
`http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/menu.html`
`http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/menu-coptions.html`
"""
import sys

sys.dont_write_bytecode = True

#from animdl.animdl.core.cli.commands import download   #later
import os
from functools import partial
import threading
import time
import datetime
from animdl.animdl.core.__version__ import __app_code__, __app_name__, __cli_core__, __core__
from tkinter import messagebox

import vlc, platform, json
import tkinter as tk
from tkinter import ttk
os.environ["PYTHONBREAKPOINT"] = "0" #heck yea
localAppDir = ""
if platform.system() == "Windows":
    localAppDir = os.getenv('LOCALAPPDATA'), "\\ani-GUI\\"
if platform.system() == "Linux":
    localAppDir = os.getenv('HOME'), "/.ani-gui/"
fr = open("{}data.json".format(''.join(localAppDir)), "r", encoding="utf-8")
settings = json.load(fr)

class PyPlayer(tk.Frame):
    def __init__(self, container, container_instance, title=None):
        tk.Frame.__init__(self, container_instance)
        self.seek_value = 10000 #change this if needed
        self.container = container
        self.container_instance = container_instance
        # create vlc instance
        self.vlc_instance, self.vlc_media_player_instance = self.create_vlc_instance()

        # main menubar
        self.menubar = tk.Menu(self.container_instance)

        # cascading file menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.create_file_menu()

        # other menus
        self.menubar.add_command(label="About", command=lambda: messagebox.showinfo(f"About {__app_name__}", f"Application name: {__app_name__}\nVersion {__cli_core__} (animdl version {__core__})\nApplication build name: {__app_code__}\n\nSpecial thanks to:\njustfoolingaround & da bois: The core\naahmd (https://gist.github.com/aahmd): Internal player code\nStackoverflow: solutions\nAnime providers: uploading animes online, great (especially crunchyroll for taking more time from me to fix the freaking ZeroDivisionError)"))
        self.container_instance.config(menu=self.menubar)
    
        # vlc video frame
        self.video_panel = ttk.Frame(self.container_instance)
        self.canvas = tk.Canvas(self.video_panel, background='black')
        
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.video_panel.pack(fill=tk.BOTH, expand=1)

        # controls
        self.create_control_panel()

        # loop
        self.scalebar_update = True

        # paused
        self.paused = False

        # last volume value
        self.last_volume_value = 100

    def create_control_panel(self):
        """Add control panel."""
        global scale, current_time, total_time, pause_play
        control_panel = ttk.Frame(self.container_instance)

        pause_play = ttk.Button(control_panel, text="⏸", command=self.pause); pause_play.pack(side=tk.LEFT)
        stop = ttk.Button(control_panel, text="⏹", command=self.stop); stop.pack(side=tk.LEFT)
        volume = ttk.Button(control_panel, text="Volume", command=self.volume_init); volume.pack(side=tk.LEFT)# this do nothing for now :trollskullirl:
        seekb = ttk.Button(control_panel, text="⏪", command=lambda: self.seek(False)); seekb.pack(side=tk.LEFT)
        seekf = ttk.Button(control_panel, text="⏩", command=lambda: self.seek(True)); seekf.pack(side=tk.LEFT)
        

        playback_bar = ttk.Frame(self.container_instance)

        playback_subframe_time = ttk.Frame(self.container_instance, width=8)
        current_time = tk.Label(playback_subframe_time, text="0:00:00   ", background="black"); current_time.pack(side=tk.LEFT)
        playback_subframe_length = ttk.Frame(self.container_instance, width=8)
        total_time = tk.Label(playback_subframe_length, text="   0:00:00", background="black"); total_time.pack(side=tk.RIGHT)
        scale = tk.Scale(root.tk_instance, variable = var , orient=tk.HORIZONTAL, resolution=0.01, background="black", showvalue=0); scale.pack(fill="both")
        
        playback_subframe_time.pack(side=tk.LEFT), playback_subframe_length.pack(side=tk.RIGHT)
        playback_bar.pack(side=tk.BOTTOM)
        control_panel.pack(side=tk.BOTTOM)

        
        root.tk_instance.bind('<space>', lambda x=None: self.pause)
        root.tk_instance.bind('<Return>', lambda x=None: self.pause)
        root.tk_instance.bind('<Escape>', lambda x=None: self.stop)
        root.tk_instance.bind('<Left>', lambda x=False: self.seek(False))
        root.tk_instance.bind('<Right>', lambda x=True: self.seek(True))
    def create_vlc_instance(self):
        """Create a vlc instance; `https://www.olivieraubert.net/vlc/python-ctypes/doc/vlc.MediaPlayer-class.html`"""
        vlc_instance = vlc.Instance()
        vlc_media_player_instance = vlc_instance.media_player_new()
        self.container_instance.update()
        return vlc_instance, vlc_media_player_instance

    def get_handle(self):
        return self.video_panel.winfo_id()

    def play(self):
        """Play a file."""
        if not self.vlc_media_player_instance.get_media():
            self.open()
        else:
            if self.vlc_media_player_instance.play() == -1:
                pass

    def close(self):
        """Close the window."""
        self.container.delete_window()

    def pause(self):
        """Pause the player."""
        self.vlc_media_player_instance.pause()
        if not self.paused:
            pause_play.config(text="►")
            self.paused = True
        else:
            pause_play.config(text="⏸")
            self.paused = False

    def stop(self):
        """Stop the player."""
        self.vlc_media_player_instance.stop()
        tk_instance = root.tk_instance
        
        tk_instance.destroy()

    def open(self, file):
        """New window allowing user to select a file and play."""
        if os.path.isfile(file):
            self.play_film(file)

    def play_film(self, file, url=None):
        """Invokes the `play` method on the vlc instance for the current file."""
        directory_name = os.path.dirname(file)
        file_name = os.path.basename(file)
        self.Media = self.vlc_instance.media_new(
            str(os.path.join(directory_name, file_name))
            # if url is None
            # else str(url)
        )
        self.Media.get_meta(12)
        #self.Media.add_option(f'start-time={6000/1000}')
        
        self.vlc_media_player_instance.set_media(self.Media)
        self.vlc_media_player_instance.set_hwnd(self.get_handle())
        self.vlc_media_player_instance.audio_set_volume(100)
        self.play()
        time.sleep(0.2)#wait for the whole media to load to get the length or it will return 0, whyy
        length = int(self.vlc_media_player_instance.get_length())
        
        threading.Thread(target=self.update_value, daemon=True).start()
        total_time.config(text=f"   {self._update_time(length/1000)}")
        scale.config(from_=0, to=length/1000)
        for binds in [scale]:
            binds.bind("<ButtonRelease-1>", lambda w=True, x=False, y=True, z=0: self.seek(x,y,z+scale.get()))
            binds.bind("<Button-1>", lambda x=False: self.update_loop_variable(False))# que
        self.scalebar_update = True
        threading.Thread(target=self.update_current_time, daemon=True).start()
        

    def seek(self, forward: bool, scroll_called: bool=False, value: float=0):
        """Seek media"""
        if not self.scalebar_update:
            self.scalebar_update = True
        cur=self.vlc_media_player_instance.get_time()
        if not scroll_called:
            if forward:
                cur += self.seek_value
            else:
                cur -= self.seek_value
            self.vlc_media_player_instance.set_time(int(cur))
            #self.Media.add_option('start-time={}'.format(''.join([str(int(minutes)), ":", str(int(seconds)), ".", str(int(miliseconds))])))
        else:
            #print(''.join([str(int(minutes)), ":", str(int(seconds)), ".", str(int(miliseconds))]))
            self.vlc_media_player_instance.set_time(int(value*1000))
            #self.Media.add_option('start-time={}'.format(''.join([str(int(minutes)), ":", str(int(seconds)), ".", str(int(miliseconds))])))
            #self.vlc_media_player_instance.play()

    def update_loop_variable(self, value: bool):
        """uhh what"""
        self.scalebar_update = value


    def update_value(self):
        """Loop event, used for update playback bar"""
        while True:
            current = int(self.vlc_media_player_instance.get_time())
            if self.scalebar_update:
                try:
                    scale.set(current/1000)
                except: pass
    
    def _update_time(self, SecToConvert):
        """Return the time format
        also henry i hate you so much datetime module exist"""
        dt = datetime.datetime.utcfromtimestamp(SecToConvert)
        
        #no anime episode really have a length of a day
        #so we dont really need to care about days that much
        
        ret = f"{dt.minute}:{dt.second}"
        if dt.hour > 0:
            ret = dt.hour + ":" + ret
        
        return ret


    def update_current_time(self):
        """Update the current time label"""
        while True:
            try:
                current_time.config(text = f"{self._update_time(int(scale.get()))}   ")
            except:
                break
            time.sleep(0.08)
    
    def volume_init(self):
        """initialize the volume window since idk how to layer this on top the media canvas"""
        self.volwid = tk.Toplevel()
        tk.Label(self.volwid, text="Change volume").pack()
        self.volume = ttk.Scale(master=self.volwid, from_=0, to=100)
        self.volume.set(self.last_volume_value)
        self.volume.pack()
        self.volume.bind("<ButtonRelease-1>", lambda x=None: self.volume_update())
        self.volwid.protocol("WM_DELETE_WINDOW", lambda x=None: self.volume_deleteWindow())
        self.volvalue = tk.Label(self.volwid, text=""); self.volvalue.pack()
        threading.Thread(target=self.volume_value_display, daemon=True).start()
    
    def volume_value_display(self):
        while True:
            vol = self.volume.get()
            self.volvalue.config(text=str(int(vol)))
            time.sleep(0.08)

    def volume_update(self):
        """Update the value"""
        vol = int(self.volume.get())
        self.vlc_media_player_instance.audio_set_volume(vol)
        self.last_volume_value = vol

    def volume_deleteWindow(self):
        """delete window event"""
        vol = int(self.volume.get())
        settings["settings"]["playervolume"] = vol
        self.volwid.destroy()
        

    @staticmethod
    def get_film_name(film) -> str:
        """Removes directory from film name."""
        return film.split('/')[-1]

    def create_file_menu(self):
        """Create file menu."""
        self.file_menu.add_command(label="Quit (the only option)", command=self.close, font=("Verdana", 14, "bold"), accelerator="ctrl + q")
        self.menubar.add_cascade(label="File", menu=self.file_menu)

    def create_film_entry(self, film):
        """Adds an entry to the `list_menu` for a given film."""
        self.list_menu.add_command(
            label=self.get_film_name(film),
            command=partial(self.play_film, film),
        )


class BaseTkContainer:
    def __init__(self):
        self.tk_instance = tk.Toplevel()
        self.tk_instance.title("Anime Searcher GUI: Media Player window")
        self.tk_instance.protocol("WM_DELETE_WINDOW", self.delete_window)
        self.tk_instance.geometry("1280x720") # default to 720p
        self.tk_instance.configure(background='black')
        self.theme = ttk.Style()
        # self.theme.theme_use("alt")

    def delete_window(self):
        player.stop()
        root.tk_instance.destroy()
    
    def __repr__(self):
        return "Base tk Container"

def create(file, url=None):
    global prev_widgets
    global root, var, player
    root = BaseTkContainer()
    w, h = root.tk_instance.winfo_screenwidth(), root.tk_instance.winfo_screenheight()
    root.tk_instance.geometry("%dx%d+0+0" % (w, h))
    var = tk.DoubleVar()
    player = PyPlayer(root, root.tk_instance, title="i lost my sanity help")
    if url is None:
        player.open(file)
    else:
        player.play_film(url=url)
    root.tk_instance.mainloop()

    
#test
if __name__ == "__main__":
    create(r"C:\Users\HenryS\AppData\Local\ani-GUI\animes\5-toubun no Hanayome 2\E04.ts")
