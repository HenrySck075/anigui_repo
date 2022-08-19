#help
from genericpath import isdir
import sys

sys.dont_write_bytecode = True

import time
starttime = time.time()
import player, shutil, re as RegEx, threading, platform, os, psutil, json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.filedialog import askdirectory
from process import down
from difflib import SequenceMatcher
from animdl.animdl.core.cli.commands import download, searchmod
from animdl.animdl.core.codebase.downloader import sanitize_filename
from animdl.animdl.core.__version__ import __app_code__, __app_name__, __cli_core__, __core__
from pypresence import Presence
os.add_dll_directory(os.path.realpath(os.path.dirname(__file__)))

#set the localappdata directory
localAppDir = ""
if platform.system() == "Windows":
    localAppDir = os.getenv('LOCALAPPDATA'), "\\ani-GUI\\"
if platform.system() == "Linux":
    localAppDir = os.getenv('HOME'), "/.ani-gui/"

#994560920674107402
downloadURL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" #:skull:
client = "994560920674107402"# yes this is an actual client id
def mikuloop(): #junimeek
    r.resizable(False,True)
    r.protocol("WM_DELETE_WINDOW", on_closing)
    r.mainloop()
query = {}
total = 0
one = 0# i forgor
two = 0# about these two variable
enumIndex = 0# enumerate index for the episode check feature
fr = open("{}data.json".format(''.join(localAppDir)), "r", encoding="utf-8")#forreal
settings = json.load(fr)
animdir = os.path.realpath(settings["settings"]["animedirectory"])
newEpMessage = ["New episode from some anime(s) you downloaded.\nThose are:\n\n"]#the dialog message list that will be later used by tk.messagebox
newEpStreamPartial = []
newEpStreamUrl = []

#some util stuff
# def excClear():
#     while True:
#         sys.exc_clear()
#         time.sleep(2)

# threading.Thread(target=excClear).start()

def newEpCheck(updateRemiderDialog, enumIndex: int):
    """check for new episode"""
    if settings["settings"]["autocheck"] == True:
        print("Checking for new episode, pls wait")
        animdir = os.listdir(f"{''.join(localAppDir)}\\animes") if platform.system() == "Windows" else os.listdir(f"{''.join(localAppDir)}/animes")
        for n in animdir:
            #loop though(?) all directory name
            query, total = searchmod.animdl_search_mod(query=n, provider=settings["settings"]["provider"], json=True)#return the querys and total anime episode
            querylist = []
            ratiolist = []
            eplist = []
            stream_urls=[]
            for re in range(total):
                querylist.append(query[re+1]["name"])#append the name list
            for item in querylist:
                ratiolist.append(SequenceMatcher(a=n, b=item).ratio())#append all the ratio match after doing SequenceMatcher check
            searchindex = ratiolist.index(max(ratiolist))#get the most match result
            streams = download.animdl_download(n, provider=settings['settings']['provider'], quality=720, special=False, idm=False, download_dir=f"{''.join(localAppDir)}animes", index=searchindex+1, id=1, log_level=1, epcrawlmode=True)
            #^while it says download, that just me recycling the code to get the streams
            for count, (stream_urls_caller, episode_number) in enumerate(streams, 1):
                eplist.append(episode_number)#append all the episode number
                stream_urls.append(stream_urls_caller)#append the modified caller data. for more info, check the animdl_download function
            try:
                currentEpList = settings["latest_ep"][n]+1
            except KeyError:
                shutil.rmtree('{0}animes\\{1}'.format(''.join(localAppDir), n))
                
            except ValueError:#probably undefined string
                settings['latest_ep'][n] = str(eplist[-1])
                with open("{}data.json".format(''.join(localAppDir)), "w", encoding="utf-8") as fw:
                    json.dump(settings, fw, indent=4)
                    fw.close()
                
            else:
                if max(currentEpList) < int(max(eplist)): newEpMessage.append(f"{n}:\n")
                
                if currentEpList == eplist.index(eplist[-1]): pass
                if currentEpList < eplist.index(eplist[-1]):
                    for ep in range(currentEpList, eplist.index(eplist[-1])):
                        enumIndex += 1
                        newEpMessage.append(f"• Episode {eplist[ep+1]}\n")
                        newEpStreamPartial.append((stream_urls[ep+1], eplist[ep+1], enumIndex))
        
        
        newEpMessage.append("\nDownload all?")
        try:
            newEpStreamPartial[0]
        except IndexError:
            if updateRemiderDialog:
                messagebox.showinfo("message", "No new episode from anime you downloaded found")
            else:
                main(0)
            
        else:
            ans = messagebox.askyesno("New episode alert",''.join(newEpMessage))#ask with the message
            quality = None
            if not ans:
                main(0)
            if ans:
                while quality == None:
                    quality = simpledialog.askstring("Quality needed", "Please enter quality value (1080, 720, 420 (if the current provider was animixplay or gogoanime))")
                    if quality == None:
                        messagebox.askretrycancel("Error", "quality where")
                    else:
                        
                        print(newEpStreamPartial)
                        
                        download.animdl_download(query="use stream url", provider=settings["settings"]["provider"], quality=quality, special=False, idm=False, download_dir=f"{''.join(localAppDir)}updateTemp\\", index=0, id=0, log_level=1, epcrawlmode=False, custom_streams_list=True, anime=n, streams=newEpStreamPartial)
                    
                settings['latest_ep'][n] = eplist[-1]
                with open("{}data.json".format(''.join(localAppDir)), "w", encoding="utf-8") as fw:
                    json.dump(settings, fw, indent=4)
                    fw.close()
                main(0)
                Label(r, text="New episode downloaded, use history mode to watch", font=("arial", 10)).pack()
    else:
        main(0)
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
#end of some util stuff
discordExist = checkIfProcessRunning('discord')
def connectToDiscord():
    global RPC
    if discordExist:
        RPC = Presence(client)  # Initialize the client class
        RPC.connect() # Start the handshake loop
    else: pass
connectToDiscord()
r = Tk()
r.title('Anime Searcher GUI. © HenrySck075, All Rights Reserved (maybe).')

objects = []
s=time.time() - starttime
print(f"Welcome to Anime Searcher GUI. \nThis will be the place to track your downloads info. \nI'll work on intergrating this to tkinter windows later. \nModule import time: {s}")
#--------------------------------------------------------------------------------------------------------------
#initialize section
def yes(booltype: bool):
    """autocheck"""
    settings["settings"]["autocheck"] = booltype
    with open("{}data.json".format(''.join(localAppDir)), "w", encoding="utf-8") as fw:
        json.dump(settings, fw, indent=4)
        fw.close()

def chooseDefaultSave():
    """Choose new save directory"""
    animdir2 = askdirectory(title="Choose your saved anime directory (all the files will be moved)")
    if animdir2 == "":
        messagebox.showerror("Error", "ok seriously don't leave the option blank, try again.")
    else:
        messagebox
        shutil.move(animdir, animdir2)
        animdir = animdir2

def menubar():
    """Initialize the menubar"""
    for widgets in r.winfo_children():
        widgets.destroy()
    menu = Menu(r)
    r.config(menu=menu)

    #goofy action menu
    actionmenu = Menu(menu, tearoff=False)
    actionmenu.add_command(label="Check for new ep", command=lambda: newEpCheck(True,1))
    if settings["settings"]["autocheck"] == True: actionmenu.add_command(label="don't do the action above on startup", command=lambda: yes(False))
    else: actionmenu.add_command(label="do the action above on startup", command=lambda: yes(True))
    actionmenu.add_command(label="Reconnect to Discord", command=lambda: connectToDiscord())
    actionmenu.add_separator()
    actionmenu.add_command(label="About", command=lambda: messagebox.showinfo(f"About {__app_name__}", f"Application name: {__app_name__}\nVersion {__cli_core__} (animdl version {__core__})\nApplication build name: {__app_code__}\n\nSpecial thanks to:\njustfoolingaround & da bois: The core\naahmd (https://gist.github.com/aahmd): Internal player code\nStackoverflow: solutions\nAnime providers: uploading animes online, great (especially crunchyroll for taking more time from me to fix the freaking ZeroDivisionError)"))
    menu.add_cascade(label='Action', menu=actionmenu)

    modemenu = Menu(menu, tearoff=0)
    modemenu.add_command(label="Search mode", command=lambda: main(0))
    modemenu.add_command(label="History mode", command=lambda: main(1))
    modemenu.add_command(label="Delete mode", command=lambda: main(2))
    menu.add_cascade(label='app mode', menu=modemenu)

#----------------------------------------------------------------------------------------------------
def main(mode:int):
    """top layout init"""
    global r
    menubar()      
    
    if checkIfProcessRunning('discord'):
        RPC.update(large_image="big_image", large_text="im out of image", details="Selecting one", buttons=[{"label": "Download tool", "url": downloadURL}])
    img = PhotoImage(file=''.join([os.path.dirname(os.path.realpath(__file__)), "\\ebst ugly logo.png" if platform.system == "Windows" else "/ebst ugly logo.png"]))
    space = Canvas(r, width = 520, height = 150)
    space.pack()
    space.create_image(20,20, anchor=NW, image=img)

    if mode == 0: main_searchMode()
    if mode == 1: main_historyMode()
    if mode == 2: main_deleteMode()

    mikuloop()

def main_searchMode():
    """Search script"""
    global r, aniname, clickedprovider, ahsl
    ahsl = StringVar()

    Label(text="gimme anime name", font=("arial", 13)).pack()
    aniname = Text(r, height = 1, width = 50, font=("arial",8))
    aniname.pack()
    aniname.config(state=NORMAL, wrap='none')

    site_urls = ["9anime", "allanime", "animekaizoku", "animeout", "animepahe", "animeonsen", "animexin", "animixplay", "animtime", "crunchyroll", "gogoanime", "haho", "hentaistream", "kamyroll_api", "kawaiifu", "nyaasi", "tenshi", "twist", "zoro"]
    clickedprovider = StringVar()
    OptionMenu(r, clickedprovider, *site_urls).pack()
    Label(text="provider")
    clickedprovider.set(settings['settings']['provider'])
    searchbtn = Button(text="Search", command=lambda: getquery(searchbtn)); searchbtn.pack()

    

def main_historyMode():
    """History script"""
    global r, ahsl 
    ahsl = StringVar()
    waitlist = []
    drop = os.listdir("{}animes".format(''.join(localAppDir)))
    for i in range(len(drop)):
        if not os.path.isdir(f"{animdir}\\{drop[i]}" if platform.system() == "Windows" else f"{animdir}/{drop[i]}"):
            waitlist.append(i)
            print(drop[i])
    for i in range(len(waitlist)):
        del drop[waitlist[-(i+1)]]
    Label(text="select the anime you downloaded here", font=("arial", 13)).pack()
    aniname = OptionMenu(r, ahsl, *drop)
    aniname.pack()

    searchbtn = Button(text="Search", command=lambda: getOtherValue_historyMode()); searchbtn.pack()

     #"omg you actually called it mikuloop :D" -Junimeek AKA The PJ DJ

def main_deleteMode():
    """Delete script"""
    global r
    iid = 0
    drop = os.listdir(f"{''.join(animdir)}")
    tree = ttk.Treeview()
    for n in drop:
        parentid = iid
        childidx = 0
        try:
            drop2 = os.listdir(f"{''.join(animdir)}\\{n}" if platform.system() == "Windows" else f"{''.join(animdir)}/{n}")
        except NotADirectoryError:
            continue
        else:
            tree.insert("", END, text=n, iid=iid, open=False)
        if drop2 == []: 
            os.removedirs(f"{settings['settings']['animedirectory']}\\{n}")
            tree.delete((str(parentid),))
        else:
            for e in drop2:
                iid += 1
                e2 = e
                e2 = e2.replace(".ts", "")
                e2 = e2.replace(".mp4", "")
                e2 = e2.replace("E", "")
                tree.insert("", END, text="{:d}".format(int(e2)), iid=iid, values=[f"{''.join(animdir)}\{n}\{e}" if platform.system() == "Windows" else f"{''.join(animdir)}/{n}/{e}"])
                #print(f"{iid}, {parentid}, {childidx}")
                tree.move(iid, parentid, childidx)
                childidx += 1
        iid += 1
    tree.bind("<<TreeviewSelect>>", lambda x=None: main_deleteMode_helper(drop, tree))
    Label(text="delete some offline movie to save space", font=("arial", 11)).pack()
    tree.pack()

def main_deleteMode_helper(name, tree: ttk.Treeview):   
    current = tree.item(tree.focus())
    print(tree.selection())
    if current["text"] in name:
        pass
    else:
        try:
            itemdir = current["values"]
            os.remove(itemdir[0])
            tree.delete(tree.selection())
        except:
            pass
#---------------------------------------------------------------------------------------#
def getquery(searchbtn):
    """get query data"""
    global qltxt, qli, proceedbtn, one, clickedquery, r, querylist
    if one == 1:
        qltxt.destroy()
        qli.destroy()
        proceedbtn.destroy()
    elif one == 0:
        one = 1
    if aniname.get("1.0", "end-1c") == "":
        print("no input!")
    else:
        easterAniname = aniname.get("1.0", "end-1c")# lấy input
        insensitive = RegEx.compile(RegEx.escape("nguyễn văn mười"), RegEx.IGNORECASE)# cAsE insensitiVe
        easterQuery = insensitive.sub("Your Name", easterAniname)# thay nguyễn văn mười thành Your Name
        
        global query, total
        query, total = searchmod.animdl_search_mod(query=easterQuery, provider=clickedprovider.get(), json=True)
        querylist = []
        for re in range(total):
            querylist.append(query[re+1]["name"])
        qltxt = Label(text="Here's the result I've found:"); qltxt.pack()
        clickedquery = StringVar()
        qli = OptionMenu(r, clickedquery, *querylist); qli.pack()
        clickedquery.set(querylist[0])
        proceedbtn = Button(text="Fetch data", command=lambda: getOtherValue(searchbtn, querylist)); proceedbtn.pack()

def getOtherValue(searchbtn, querylist=[]):
    """last step to download"""
    global clickedep, clickedqual, r, objects, savedaniname, two, localAppDir
    
    one == 0
    qltxt.destroy()
    qli.destroy()
    proceedbtn.destroy()
    searchbtn.destroy()


    savedaniname = aniname.get("1.0", "end-1c")
    aniname.delete('1.0', END)
    aniname.insert(INSERT, clickedquery.get())
    aniname.config(state=DISABLED)
    eplist = []
    
    streams = download.animdl_download(aniname.get("1.0", "end-1c"), provider=settings['settings']['provider'], quality=720, special=False, idm=False, download_dir=''.join(localAppDir), index=querylist.index(aniname.get("1.0", "end-1c"))+1, id=1, log_level=1, epcrawlmode=True)
    for count, (stream_urls_caller, episode_number) in enumerate(streams, 1):
        eplist.append(episode_number)
    Label(text="anime episode", font=("arial", 13)).pack()
    clickedep = StringVar()
    episodebox = ttk.Combobox(r, textvariable=clickedep, value=eplist); episodebox.pack()
    
    Label(text="quality (higher quality = slower download)", font=("arial", 13)).pack()
    quality = ["1080", "720"]
    if clickedprovider.get() == "animixplay" or clickedprovider.get() == "gogoanime":
        quality.append("480")
    clickedqual = StringVar()
    clickedqual.set("1080")
    qualitymenu = OptionMenu(r, clickedqual, *quality); qualitymenu.pack()

    startbtn = Button(text="steal", command=lambda: launchthread()); startbtn.pack()

    for obj in r.winfo_children():
        try:
            obj.config(state=NORMAL)
        except: pass
        
def getOtherValue_historyMode():
    """last step to view history data"""
    eplist = []
    if ahsl.get() == "": return
    f = os.listdir("{0}animes\\{1}".format(''.join(localAppDir), ahsl.get()) if platform.system() == "Windows" else "{0}{1}".format(''.join(localAppDir), ahsl.get()))
    for i in f:
        i=i.replace("E", "")
        i=i.replace("E0", "")
        i=i.replace(".ts", "")
        eplist.append(i)
    label = Label(r, text="anime episode", font=("arial", 13))
    clickedep = StringVar()
    episodebox = ttk.Combobox(r, textvariable=clickedep, value=eplist)
    startbtn = Button(text="launch", command=lambda x="" : _historyMode_launch(eplist, f, clickedep))
    label.pack(); episodebox.pack(); startbtn.pack()
    for obj in r.winfo_children():
        try:
            obj.config(state=NORMAL)
        except: pass
    

def _historyMode_launch(eplist, f, clickedep):
    for obj in r.winfo_children():
        try:
            obj.config(state=DISABLED)
        except: pass
    player.create('{0}animes\\{1}\\{2}'.format(''.join(localAppDir), ahsl.get(), f[eplist.index(clickedep.get())]))
    for obj in r.winfo_children():
        try:
            obj.config(state=NORMAL)
        except: pass
#------------------------------------------------------------------------------------------

def launchthread():
    global thread
    thread = threading.Thread(target=launch)
    thread.start()

def launch():
    epinput = clickedep.get()
    ep = "E{:02d}".format(int(epinput))


    fw = open("{}data.json".format(''.join(localAppDir)), "w", encoding="utf-8")
    json.dump(settings, fw, indent=4)
    fw.close()
    for obj in r.winfo_children():
        try:
            obj.config(state=DISABLED)
        except:
            continue
    down.process(r, aniname.get("1.0", "end-1c"), clickedep.get(), clickedqual.get(), clickedprovider.get(), ep, querylist, savedaniname, sanitize_filename(aniname.get("1.0", "end-1c")), justdownload=False)
        # type, value, traceback = sys.exc_info()
        # messagebox.showerror("Error", f"Operation stopped with:\nType: {type}\n Message:\n{value}")
    for obj in r.winfo_children():
        try:
            obj.config(state=NORMAL)
        except:
            continue

def on_closing():
    """WM_DELETE_WINDOW event"""
    try:
        thread.is_alive()
    except:
        fr.close()
        fw = open("{}data.json".format(''.join(localAppDir)), "w", encoding="utf-8")
        json.dump(settings, fw, indent=4) 
        fw.close()
        r.destroy()
    else:
        if thread.is_alive() == True:
            forceClose = messagebox.askyesno("Task still running!", "The download task is still running. \nif you want to close it now, the current downloaded data will be deleted.\nContinue?") #this thing never work
            if forceClose:
                fr.close()
                fw = open("{}data.json".format(''.join(localAppDir)), "w", encoding="utf-8")
                json.dump(settings, fw, indent=4) 
                fw.close()
                shutil.rmtree('{}animes\\{}'.format(''.join(localAppDir), sanitize_filename(aniname.get())))
                r.destroy()
            else:
                pass
        else:
            fr.close()
            fw = open("{}data.json".format(''.join(localAppDir)), "w", encoding="utf-8")
            json.dump(settings, fw, indent=4) 
            fw.close()
            r.destroy()

newEpCheck(False, enumIndex)# link start (no shit sao referrence, haha im funny and original)
