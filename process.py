#if this one errored out, there's a high chance you have missing argument or the anime unavailable on the server

from tkinter import *
import os, time, psutil, platform, json
import player
from pypresence import Presence
from animdl.animdl.core.cli.commands import download, stream

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

if __name__ == "process.py":
    client = "994560920674107402"  # Fake ID, put your real one here
    try:
        RPC = Presence(client)  # Initialize the client class
        RPC.connect()
    except:
        RPC = None

localAppDir = ""
if platform.system() == "Windows":
    localAppDir = os.getenv('LOCALAPPDATA'), "\\ani-GUI\\"
if platform.system() == "Linux":
    localAppDir = os.getenv('HOME'), "/.ani-gui/"
isExist = os.path.exists(''.join(localAppDir))
if not isExist:
    os.makedirs(''.join(localAppDir))
    print("The new directory is created!")

default = {
            "latest_ep": {"default": None}, "settings": {"provider": "animixplay", "autocheck": True, "ihavenomorediskspace": False, "animedirectory": f"{''.join(localAppDir)}\\animes", "playervolume": 100}
        }
if not os.path.exists("{}data.json".format(''.join(localAppDir))):
    with open("{}data.json".format(''.join(localAppDir)), "w", encoding="utf-8") as fw:
        json.dump(default, fw, indent=4)
        fw.close()
fr = open("{}data.json".format(''.join(localAppDir)), "r", encoding="utf-8")
settings = json.load(fr)
animdir = os.path.realpath(settings["settings"]["animedirectory"])


class play:
    def stream(r: Tk, name, epinput, stream_link=None):
        start = time.time()
        details = "Watching ", name
        epid = epinput.replace("E", "")
        epid = epid.replace(".ts", "")
        epid = epid.replace(".mp4", "")
        if platform.system() == "Linux":
            eppath = ''.join(localAppDir), "animes/", name, "/", epinput
        if platform.system() == "Windows":
            eppath = ''.join(localAppDir), "animes\\", name, "\\", epinput
        print(eppath)
        try:
            RPC.update(large_image="big_image", large_text="im out of image", details=''.join(details), start=start, buttons=[{"label": "Download tool", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}])
        except:
            pass
        player.create(''.join(eppath))
        


class down():
    def process(
        widget, nameinput, epinput, qualinput, provider, ep, relist, searchquery, sanitizeddirectory, justdownload=False, stream_url=None
    ):
        infile = ''.join(ep), ".ts"
        os.chdir(''.join(localAppDir))
        Label(widget, text="Downloading, please check console output for progress", font=("arial", 8))
        #command = 'py animdl\\runner.py download "', provider, ":", nameinput, '" --range ',  epinput, " --index ", str(sidx+1), " --quality ", qualinput, " -d .\\animes"

        downloadmsg = "Downloading requested content."
        content = {"large_image": "big_image", "large_text": "im out of image", "small_image": "process", "small_text": "Processing...", "state": ''.join(downloadmsg), "party_size": [2, 2], "details": "Processing request", "buttons": [{"label": "Download tool", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}]}
        
        path = ''.join(localAppDir), sanitizeddirectory
        idx = relist.index(nameinput)+1
        if os.path.exists(''.join(path)) == True:
            eppath = path, "\\", ''.join(infile)
            if os.path.exists(''.join(eppath)) == True:
                stream.stream(sanitizeddirectory, ''.join(infile))
            else:
                downscript(widget, content, provider, searchquery, qualinput, nameinput, sanitizeddirectory, justdownload, infile, idx, epinput, stream_url)
        else:
            downscript(widget, content, provider, searchquery, qualinput, nameinput, sanitizeddirectory, justdownload, infile, idx, epinput, stream_url)

def downscript(r, content, provider, searchquery, qualinput, nameinput, sanitizeddirectory, justdownload, infile, idx, epinput, stream_url): #im tired
    try:
        RPC.update(**content)
    except:
        pass
    if not settings["settings"]["ihavenomorediskspace"]:
        download.animdl_download(query="{0}:{1}".format(provider, searchquery), provider=provider, special=False, quality=qualinput, download_dir="{}animes\\".format(''.join(localAppDir)), idm=False, index=idx, id=int(epinput), log_level=1, epcrawlmode=False)
    else:
        streams = download.animdl_download(query="{0}:{1}".format(provider, searchquery), provider=provider, special=False, quality=qualinput, download_dir="{}animes\\".format(''.join(localAppDir)), idm=False, index=idx, id=int(epinput), log_level=1, epcrawlmode=True)
        for count, (stream_caller, number) in enumerate(streams, 1):
            if count == int(epinput):
                player.create(None, stream_caller())
    with open("{}data.json".format(''.join(localAppDir)), "r") as data:
        array = json.load(data)
        if array["latest_ep"][nameinput] != "undefined": pass
        if not nameinput in array["latest_ep"]: array["latest_ep"][nameinput] = "undefined"
    with open("{}data.json".format(''.join(localAppDir)), "w") as writedata:
        json.dump(array, writedata, indent=4)
        writedata.close()
    if justdownload: pass
    if not justdownload: play.stream(r, sanitizeddirectory, ''.join(infile))
        
#download.animdl_download(query="animixplay:5-toubun no Hanayome 2", quality="720", special=False, idm=False, download_dir="C:\\Users\\Test Chamber\\AppData\\Local\\ani-gui\\animes\\", index=1, log_level=1, id="3")
if __name__ == "__main__":
    print("Direct launch detected. Go away and launch main script please.")#gl
    time.sleep(5)