## Script to download subtitles from opensubtitles.com
## Author: Majd
## If You want to use this app you need to replace the username and password with your own from opensubtitle website as well as the API key 
## Don't forget to update thr path of the file to save the subtitles in the FilePath variable
## This is an open source project and you can use it as you want (No copyright)
## If you have any question or suggestion please contact me on my github @MajdLHB
## This app uses ttk and tkinter libraries to create the GUI witch means the os native theme will be used
## You can change the theme by changing the style.theme_use('vista') to any other theme you want
## You can transforme this script to an executable file 
## Set the VLC media player as defualt player to play the video with the subtitle
## Enjojy :)


## Libraries
import requests
import json
import os
import random
import tkinter as tk
from tkinter import ttk
from tkinter import font
import re
import vlc
import math
import subprocess
import time
from tkinter import messagebox
import subprocess
from tkinter import filedialog

def RemoveSpaceFromName(Name):
    Name = Name.replace(" ", "")
    return Name

def replacespace(Name):
    Name = Name.replace(" ", "+")
    return Name

## Variables
NameOfPrevSeries = "Breaking Bad"
prevSeries = RemoveSpaceFromName(NameOfPrevSeries)
prevSeason =5
prevEpisode =4

responsE = ""

entry1 = ""
entry2 = ""
entry3 = ""
entry4 = ""


script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]


NameOfSeries = "Breaking Bad"
Series = RemoveSpaceFromName(NameOfSeries)
THeSHowNAme = replacespace(NameOfSeries)
Season =5
Episode =4
typeOfContent = 'episode'

EpisodeSubNAme = ""
SeasonSubName = ""

fileID =0

Delay = 0
IsHDTV = True
IsNetflix = True

host = 'localhost'  
port = '8080'       
password = 'majd'

slug_file_id_list = []
slugList = []

HDTVsub = []
NetflixSub = []
NonHDTVsub = []

SUbToDownload = []

DownloadURL = []

FilePath = rf'{script_dir}\Subtitles\MajdSub_{Series}_S{Season}E{Episode}.srt'
SeriesFolder = rf''
SubPath = ""

current_index = 1

folder_selected = ""

OSUsername = ""
OSPassword = ""
APiKey = "TD36XSkIVGJwXZfAlayTeEl4usDj5dqi"

Vlcpath = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"

## VAriable Class
class Id:
    FileID = 0

## Functions
def login():
    global OSUsername
    global OSPassword
    global APiKey
    global responsE
    url = "https://api.opensubtitles.com/api/v1/login"

    payload ={
        "username": OSUsername,
        "password": OSPassword
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "<<MajdSub v0.1>>",
        "Accept": "application/json",
        "Api-Key": APiKey
    }

    response = requests.post(url, json=payload, headers=headers)
    response = json.loads(response.text)
    responsE = response['status']



def SearchForSub():
    global Series
    global Season
    global Episode
    global typeOfContent
    global slug_file_id_list
    global SUbToDownload
    global APiKey
    global Id
    global fileID
    global responsE

    url = "https://api.opensubtitles.com/api/v1/subtitles"

    querystring = {"type": typeOfContent,"query": Series,"languages":"ar","season_number": Season,"episode_number": Episode}

    headers = {
        "User-Agent": "<<MajdSub v0.1>>",
        "Api-Key": APiKey
    }

    response1 = requests.get(url, headers=headers, params=querystring)
    response1 = json.loads(response1.text)
    PageCount = response1['total_pages']
    Subtitles = response1['data']


    for subtitle in Subtitles:
        slug = subtitle['attributes']['slug']
        for file in subtitle['attributes']['files']:
            file_id = file['file_id']
            slug_file_id_list.append({'slug': slug, 'file_id': file_id})
            

    for slug in slug_file_id_list:
        SUbToDownload.append(slug['file_id'])

    if SUbToDownload is None:
        print('No subtitles found')
    
    fileID = SUbToDownload[0]
    Id.FileID = fileID
    

def DownloadSub():
    global Id
    global Delay
    global APiKey
    global FilePath
    url = "https://api.opensubtitles.com/api/v1/download"

    payload = {"file_id": Id.FileID, "timeshift": Delay}
    
    headers = {
        "User-Agent": "<<MajdSub V1.0>>",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Api-Key": APiKey
    }

    response2 = requests.post(url, json=payload, headers=headers)
    response2 = json.loads(response2.text)
    DownloadURL = response2['link']
    downloadURL = str(DownloadURL)
    response3 = requests.get(downloadURL)
    with open (FilePath, 'wb') as file:
        file.write(response3.content)
        print('Downloaded')

def OpenFile(Series, Season, Episode):
    global Vlcpath
    global SubPath
    print(f'{Series} S{Season} E{Episode}')
    matching_files = []
    CorrectFiles = []
    correctfile = ""
    episodepathlist = []
    episodePath = ""
    target_pattern = re.compile(r'.*\b{}\b.*'.format(re.escape(Series)))
    for root, dirs, files in os.walk(SeriesFolder):
        for file_name in dirs:
            if target_pattern.search(file_name):
                matching_files.append(os.path.join(root, file_name))
            
    matchingFile = str(random.choice(matching_files))
    matchingFile = matchingFile.replace('/', '\\')
    print(matchingFile)
    for root, dirs, files in os.walk(matchingFile):
        for file in dirs:
            if f'S{Season}' in dirs:
                CorrectFiles.append(os.path.join(root, file))
            elif f'season {Season}' in dirs:
                CorrectFiles.append(os.path.join(root, file))
            elif f'S0{Season}' in dirs:
                CorrectFiles.append(os.path.join(root, file)) 
            elif f's0{Season}' in dirs:
                CorrectFiles.append(os.path.join(root, file)) 
            elif f'Season {Season}' in dirs:
                CorrectFiles.append(os.path.join(root, file)) 
            elif f'Season 0{Season}' in dirs:
                CorrectFiles.append(os.path.join(root, file)) 
            elif f'season 0{Season}' in dirs:
                CorrectFiles.append(os.path.join(root, file))     
    correctfile = str(random.choice(CorrectFiles))
    for root, dirs, files in os.walk(correctfile):
        for file in files:
            if f'E{Episode}' in file:
                episodepathlist.append(os.path.join(root, file))
            elif f'E0{Episode}' in file:
                episodepathlist.append(os.path.join(root, file))
            elif f'Episode {Episode}' in file:
                episodepathlist.append(os.path.join(root, file))
            elif f'episode {Episode}' in file:
                episodepathlist.append(os.path.join(root, file))
            elif f'episode 0{Episode}' in file:
                episodepathlist.append(os.path.join(root, file))
            elif f'Episode 0{Episode}' in file:
                episodepathlist.append(os.path.join(root, file))
            elif f'e0{Episode}' in file:
                episodepathlist.append(os.path.join(root, file))
            elif f'e{Episode}' in file:
                episodepathlist.append(os.path.join(root, file))
    episodePath = str(random.choice(episodepathlist))
    episodePath = episodePath.replace('/', '\\')
    
    print(episodePath)
    vlc_command = [
    Vlcpath,
    '--extraintf', 'http',
    '--play-and-exit',  
    '--fullscreen',     
    episodePath,
    f'--sub-file={SubPath}'  
    ]
    subprocess.Popen(vlc_command)


def play():
    global FilePath
    global Episode
    global Series
    global Season
    global CurentLabel
    global PrevLabel
    global NameOfSeries
    global THeSHowNAme
    global prevSeries
    global prevSeason
    global prevEpisode
    global Seasonentry
    global Episodeentry
    global EpisodeSubNAme
    global SeasonSubName
    login()
    SearchForSub()
    DownloadSub()
    EncodeSRT(encoding='utf-8')
    OpenFile(Series, Season, Episode)
    prevEpisode = Episode
    prevSeason = Season
    prevSeries = Series
    EpisodeSubNAme = Episode
    SeasonSubName = Season
    FilePath = rf'{script_dir}\Subtitles\MajdSub_{Series}_S{SeasonSubName}E{EpisodeSubNAme}.srt'
    ShowID = get_show_id(THeSHowNAme)
    if ShowID is None:
        print('No show found')
    else:
        Seasons = get_seasons(ShowID)
        for season in Seasons:
            if season['number'] == Season:
                SeasonID = season['id']
                Episodes = get_episodes(SeasonID)
                num_episodes = len(Episodes)
            elif season['number'] == f'0{Season}' or season['number'] == int(f'0{Season}') or season['number'] == f'{Season}' or season['number'] == f'0{Season}':
                SeasonID = season['id']
                Episodes = get_episodes(SeasonID)
                num_episodes = len(Episodes)
    Episode = int(Episode) + 1
    if (Episode < num_episodes):
        Episode = Episode
    elif (Episode > num_episodes):
        Episode = 1
        Season = int(Season) + 1
    change_subtitle_vlc_http(host, port, password, SubPath)
    
    SavePrevVariables()
    LoadPrevVariables()
    CurentLabel.config(text=f'Current video: {Series} S{Season} E{Episode}')
    PrevLabel.config(text=f'Previous video: {prevSeries} S{prevSeason} E{prevEpisode}')
    Seasonentry.delete(0, tk.END)
    Seasonentry.insert(0, Season)
    Episodeentry.delete(0, tk.END)
    Episodeentry.insert(0, Episode)
    saveVariables()
    loadVariables()
    print(prevEpisode)


def EncodeSRT(encoding='utf-8'):
    global SubPath
    global FilePath
    global Series
    global prevSeason
    global prevEpisode
    outputFilePath = FilePath.replace('MajdSub', 'MajdSubV1')
    with open(FilePath, 'r', encoding='utf-8') as f:
        Content = f.read()
    
    with open(outputFilePath, 'w', encoding=encoding) as f:
        f.write(Content)
    SubPath = outputFilePath


def VarSet3():
    print(f'v:{var.get()}')

def update():
    global FilePath
    global NameOfSeries
    global Series
    global Season
    global Episode
    global Delay
    global NameOfPrevSeries
    global prevSeries
    global prevSeason
    global prevEpisode
    global Serieentry
    global Seasonentry
    global Episodeentry
    global timeentry
    global CurentLabel
    global PrevLabel
    global EpisodeSubNAme
    global SeasonSubName
    prevSeries = Series
    prevSeason = Season
    prevEpisode = Episode
    NameOfSeries = Serieentry.get()
    Season = Seasonentry.get()
    Episode = Episodeentry.get()
    Delay = timeentry.get()
    EpisodeSubNAme = Episode
    SeasonSubName = Season
    CurentLabel.config(text=f'Current video: {Series} S{Season} E{Episode}')
    PrevLabel.config(text=f'Previous video: {prevSeries} S{prevSeason} E{prevEpisode}')
    saveVariables()
    SavePrevVariables()
    LoadPrevVariables()
    loadVariables()
    FilePath = rf'{script_dir}\Subtitles\MajdSub_{Series}_S{SeasonSubName}E{EpisodeSubNAme}.srt'

def get_show_id(SerieName):
    search_url = f"http://api.tvmaze.com/search/shows?q={SerieName}"
    response = requests.get(search_url)
    data = response.json()
    if data:
        return data[0]['show']['id']
    else:
        messagebox.showerror("Error", "The Show season and nuber of episode is not found in the database. Try to change the name of the show (add spaces or remove numbers)")
        return None

def get_seasons(show_id):
    seasons_url = f"http://api.tvmaze.com/shows/{show_id}/seasons"
    response = requests.get(seasons_url)
    data = response.json()
    return data

def get_episodes(season_id):
    episodes_url = f"http://api.tvmaze.com/seasons/{season_id}/episodes"
    response = requests.get(episodes_url)
    data = response.json()
    return data


def saveEpisode():
    global Episode
    EpisodePath = rf'{script_dir}\Episode.json'
    with open (EpisodePath, 'w') as file:
        json.dump({"variable": Episode}, file)

def loadEpisode():
    global Episode
    EpisodePath = rf'{script_dir}\Episode.json'
    with open (EpisodePath, 'r') as file:
        data = json.load(file)
        Episode = data['variable']

def saveSeason():
    global Season
    SeasonPath = rf'{script_dir}\Season.json'
    with open (SeasonPath, 'w') as file:
        json.dump({"variable": Season}, file)

def loadSeason():
    global Season
    SeasonPath = rf'{script_dir}\Season.json'
    with open (SeasonPath, 'r') as file:
        data = json.load(file)
        Season = data['variable']


def saveSeries():
    global Series
    SeriesPath = rf'{script_dir}\Series.json'
    with open (SeriesPath, 'w') as file:
        json.dump({"variable": Series}, file)

def loadSeries():
    global Series
    SeriesPath = rf'{script_dir}\Series.json'
    with open (SeriesPath, 'r') as file:
        data = json.load(file)
        Series = data['variable']

def Save_OS_Login_data():
    global OSUsername
    global OSPassword
    global APiKey
    global script_dir
    global SeriesFolder
    SeriesFolderpath = rf'{script_dir}\SeriesFolder.json'
    OSUsernamePath = rf'{script_dir}\OSUsername.json'
    OSPasswordPath = rf'{script_dir}\OSPassword.json'
    APiKeyPath = rf'{script_dir}\APiKey.json'
    with open (OSUsernamePath, 'w') as file:
        json.dump({"variable": OSUsername}, file)
    with open (OSPasswordPath, 'w') as file:
        json.dump({"variable": OSPassword}, file)
    with open (APiKeyPath, 'w') as file:
        json.dump({"variable": APiKey}, file)
    with open (SeriesFolderpath, 'w') as file:
        json.dump({"variable": SeriesFolder}, file)

def Load_OS_Login_data():
    global OSUsername
    global OSPassword
    global APiKey
    global script_dir
    global SeriesFolder

    SeriesFolderpath = rf'{script_dir}\SeriesFolder.json'
    OSUsernamePath = rf'{script_dir}\OSUsername.json'
    OSPasswordPath = rf'{script_dir}\OSPassword.json'
    APiKeyPath = rf'{script_dir}\APiKey.json'

    with open (OSUsernamePath, 'r') as file:
        data = json.load(file)
        OSUsername = data['variable']


    with open (OSPasswordPath, 'r') as file:
        data = json.load(file)
        OSPassword = data['variable']

    with open (APiKeyPath, 'r') as file:
        data = json.load(file)
        APiKey = data['variable']
    
    with open (SeriesFolderpath, 'r') as file:
        data = json.load(file)
        SeriesFolder = data['variable']

Load_OS_Login_data()

def SaveVLCData():
    global host
    global port
    global password
    global Vlcpath
    hostPath = rf'{script_dir}\host.json'
    portPath = rf'{script_dir}\port.json'
    passwordPath = rf'{script_dir}\password.json'
    VlcpathPath = rf'{script_dir}\Vlcpath.json'
    with open (hostPath, 'w') as file:
        json.dump({"variable": host}, file)
    with open (portPath, 'w') as file:
        json.dump({"variable": port}, file)
    with open (passwordPath, 'w') as file:
        json.dump({"variable": password}, file)
    with open (VlcpathPath, 'w') as file:
        json.dump({"variable": Vlcpath}, file)

def LoadVLCData():
    global host
    global port
    global password
    global Vlcpath
    hostPath = rf'{script_dir}\host.json'
    portPath = rf'{script_dir}\port.json'
    passwordPath = rf'{script_dir}\password.json'
    VlcpathPath = rf'{script_dir}\Vlcpath.json'

    with open (hostPath, 'r') as file:
        data = json.load(file)
        host = data['variable']

    with open (portPath, 'r') as file:
        data = json.load(file)
        port = data['variable']

    with open (passwordPath, 'r') as file:
        data = json.load(file)
        password = data['variable']

    with open (VlcpathPath, 'r') as file:
        data = json.load(file)
        Vlcpath = data['variable']

def SavePrevVariables():
    global prevSeries
    global prevSeason
    global prevEpisode
    prevSeriesPath = rf'{script_dir}\prevSeries.json'
    prevSeasonPath = rf'{script_dir}\prevSeason.json'
    prevEpisodePath = rf'{script_dir}\prevEpisode.json'
    with open (prevSeriesPath, 'w') as file:
        json.dump({"variable": prevSeries}, file)
    with open (prevSeasonPath, 'w') as file:
        json.dump({"variable": prevSeason}, file)
    with open (prevEpisodePath, 'w') as file:
        json.dump({"variable": prevEpisode}, file)

def LoadPrevVariables():
    global prevSeries
    global prevSeason
    global prevEpisode
    global PrevLabel
    prevSeriesPath = rf'{script_dir}\prevSeries.json'
    prevSeasonPath = rf'{script_dir}\prevSeason.json'
    prevEpisodePath = rf'{script_dir}\prevEpisode.json'
    with open (prevSeriesPath, 'r') as file:
        data = json.load(file)
        prevSeries = data['variable']

    with open (prevSeasonPath, 'r') as file:
        data = json.load(file)
        prevSeason = data['variable']


    with open (prevEpisodePath, 'r') as file:
        data = json.load(file)
        prevEpisode = data['variable']


def saveVariables():
    saveEpisode()
    saveSeason()
    saveSeries()

def loadVariables():
    global Episodeentry
    global Seasonentry
    global Serieentry
    loadEpisode()
    loadSeason()
    loadSeries()
    Episodeentry.delete(0, tk.END)
    Episodeentry.insert(0, Episode)
    Seasonentry.delete(0, tk.END)
    Seasonentry.insert(0, Season)
    Serieentry.delete(0, tk.END)
    Serieentry.insert(0, Series)


Load_OS_Login_data()
LoadVLCData()


def redownload():
    login()
    SearchForSub()
    DownloadSub()
    EncodeSRT(encoding='utf-8')

current_subtitle_index = 0
def change_to_next_subtitle_vlc_http(host, port, password):
    global current_subtitle_index
    current_subtitle_index += 1
    url = f'http://{host}:{port}/requests/status.xml'
    headers = {'User-Agent': 'Mozilla/5.0'}
    auth = requests.auth.HTTPBasicAuth('', password)  

    next_subtitle_index = current_subtitle_index + 1

    # VLC uses 0-based index for subtitle tracks
    params = {'command': 'subtitle_track', 'val': next_subtitle_index}

    response = requests.get(url, headers=headers, auth=auth, params=params)
    response.raise_for_status() 
    print(f"Switched to subtitle track: {next_subtitle_index}")


def change_subtitle_vlc_http(host, port, password, subtitle_path):
    url = f'http://{host}:{port}/requests/status.xml'
    headers = {'User-Agent': 'Mozilla/5.0'}
    auth = requests.auth.HTTPBasicAuth('', password) 

    params = {'command': 'addsubtitle', 'val': subtitle_path}
    change_to_next_subtitle_vlc_http(host, port, password)
    try:
        response = requests.get(url, headers=headers, auth=auth, params=params)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
        print(f"Subtitle changed to: {subtitle_path}")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")

def NextSub():
    global current_index
    global vlc
    global SubPath
    global host
    global port
    global password
    if current_index < len(slug_file_id_list):
        element = slug_file_id_list[current_index]
        current_index += 1
        CurrentSubName.config(text=f"Current Sub: {element['slug']}")
        Id.FileID = element['file_id']
    else:
        messagebox.showinfo("Info", "End of list reached")
    DownloadSub()
    EncodeSRT(encoding='utf-8')
    change_subtitle_vlc_http(host, port, password, SubPath)

def ShowSUbs():
    winmdow = tk.Toplevel()
    winmdow.title("Subtitles")
    style = ttk.Style()
    style.theme_use('vista')
    winmdow.geometry("400x400")
    winmdow.resizable(False, False)
    global slug_file_id_list

    List = tk.Listbox(winmdow, width=100, height=22, font=("Arial", 9), selectmode=tk.SINGLE, bg="gray", fg="black")
    List.place(x=0, y=0)

    for element in slug_file_id_list:
        print(element['slug'])
        List.insert(tk.END, element['slug'])
    
    DownloadSelection = ttk.Button(winmdow,text="Download selection")
    DownloadSelection.place(x=260, y=360)

    winmdow.mainloop()

folder_selected2 = ""

def setup():
    global folder_selected
    global SubPath
    global host
    global port
    global password
    global vlc
    global FilePath
    global SeriesFolder
    global responsE
    global entry1
    global entry2
    global entry3
    global entry4
    global folder_selected2
    global Vlcpath

    window = tk.Toplevel()
    window.title("Set up")
    style = ttk.Style()
    style.theme_use('vista')
    window.geometry("850x250")
    window.resizable(False, False)

    label1 = ttk.Label(window, text="The Series Foldor:", font=("Arial, 10"))
    label1.place(x=20, y=10)

    entry2 = ttk.Entry(window, width=30, font=("Arial, 9"))
    entry2.place(x=130, y=10)
    entry2.insert(0, SeriesFolder)

    def SelectFolder():
        global folder_selected
        folder_selected = filedialog.askdirectory(title="Select a Folder")
        entry2.delete(0, tk.END)
        entry2.insert(0, folder_selected)


    button1 = ttk.Button(window,text='Browse', command=SelectFolder)
    button1.place(x=350, y=10)

    label2 = ttk.Label(window, text="OpenSubtitle username:", font=("Arial, 10"))
    label2.place(x=20, y=60)

    entry3 = ttk.Entry(window, width=20, font=("Arial, 12"))
    entry3.place(x=160, y=60)

    label3 = ttk.Label(window, text="Opensubtitle password:", font=("Arial, 10"))
    label3.place(x=20, y=110)

    entry4 = ttk.Entry(window, width=20, font=("Arial, 12"), show="*")
    entry4.place(x=160, y=110)

    label = ttk.Label(window, text="Opensubtitle Api key:", font=("Arial, 10"))
    label.place(x=20, y=160)

    entry1 = ttk.Entry(window, width=50, font=("Arial", 9))
    entry1.place(x=150, y=160)
    entry1.insert(0, APiKey)

    entry3.insert(0, OSUsername)
    entry4.insert(0, OSPassword)

    Error1 = ttk.Label(window, text="", font=("Arial, 10"))
    Error1.place(x=180, y=210)

    def logiN():
        global OSUsername
        global OSPassword
        global APiKey
        OSUsername = entry3.get()
        OSPassword = entry4.get()
        APiKey = entry1.get()
        login()
        print(responsE)
        if  int(responsE) == 200:
            Error1.config(text="Login successful", foreground="green")
        else:
            Error1.config(text="Login failed", foreground="red")
        Save_OS_Login_data()
        Load_OS_Login_data()
    

    login1 = ttk.Button(window, text="Login", command=logiN)
    login1.place(x=100, y=210)

    label4 = ttk.Label(window, text="Vlc path:", font=("Arial, 10"))
    label4.place(x=450, y=10)

    entry5 = ttk.Entry(window, width=30, font=("Arial, 9"))
    entry5.place(x=530, y=10)
    entry5.delete(0, tk.END)
    entry5.insert(0, Vlcpath)

    def SelectFolder2():
        global folder_selected2
        folder_selected2 = filedialog.askopenfilename(
        title="Select an executable file",
        filetypes=(("Executable files", "*.exe"), ("All files", "*.*"))
        )
        entry5.delete(0, tk.END)
        entry5.insert(0, folder_selected2)
        Vlcpath = folder_selected2
        entry5.delete(0, tk.END)
        entry5.insert(0, Vlcpath)
        Vlcpath = entry5.get()

    button1 = ttk.Button(window,text='Browse', command=SelectFolder2)
    button1.place(x=750, y=10)

    label5 = ttk.Label(window, text="Vlc http pasword:", font=("Arial, 10"))
    label5.place(x=450, y=60)

    label6 = ttk.Label(window, text="Vlc http port:", font=("Arial, 10"))
    label6.place(x=450, y=110)

    def update():
        global SeriesFolder
        global host
        global port
        global password
        global FilePath
        global SubPath
        global Series
        global Season
        global Episode
        global NameOfSeries
        global THeSHowNAme
        global prevSeries
        global prevSeason
        global prevEpisode
        global Serieentry
        global Seasonentry
        global Episodeentry
        global timeentry
        global CurentLabel
        global PrevLabel
        global EpisodeSubNAme
        global SeasonSubName
        global OSUsername
        global OSPassword
        global APiKey
        global Vlcpath
        global responsE
        SeriesFolder = entry2.get()
        host = 'localhost'
        port = '8080'
        password = 'majd'
        Vlcpath = entry5.get()
        OSUsername = entry3.get()
        OSPassword = entry4.get()
        APiKey = entry1.get()
        print(OSUsername)
        print(OSPassword)
        window.withdraw()
        Save_OS_Login_data()
        Load_OS_Login_data()
        SaveVLCData()
        LoadVLCData()

    Save = ttk.Button(window, text="Save", command=update)
    Save.place(x=20, y=210)

    window.mainloop()

def DownloadNextSub():
    global current_index
    global vlc
    global SubPath
    global host
    global port
    global password
    if current_index < len(slug_file_id_list):
        element = slug_file_id_list[current_index]
        current_index += 1
        CurrentSubName.config(text=f"Current Sub: {element['slug']}")
        Id.FileID = element['file_id']
    else:
        messagebox.showinfo("Info", "End of list reached")
    DownloadSub()
    EncodeSRT(encoding='utf-8')








## GUI
root = tk.Tk()
root.title("MajdSub V1.0")
style = ttk.Style()
style.theme_use('vista')

root.geometry("485x245+100+100")
root.resizable(False, False)

label = ttk.Label(root, text="Welcome to MajdSub V1.0", foreground="Black", font=("Arial", 15))
label.pack()

action_button = ttk.Button(root, text="Play", command=play)
action_button.place(x=400, y=200)

action_button = ttk.Button(root, text="NextSub", command=NextSub)
action_button.place(x=380, y=60)

action_button = ttk.Button(root, text="Download Next", command=DownloadNextSub)
action_button.place(x=280, y=60)

action_button = ttk.Button(root, text="Show Subs", command=ShowSUbs)
action_button.place(x=380, y=90)

CurrentSubName = ttk.Label(root, text="SubName", foreground="Black", font=("Arial", 9))
CurrentSubName.place(x=280, y=40)

action_button = ttk.Button(root, text="Set up", command=setup)
action_button.place(x=310, y=200)

action_button = ttk.Button(root, text="Update", command=update)
action_button.place(x=220, y=200)

#action_button = ttk.Button(root, text="")
#action_button.place(x=130, y=200)

action_button = ttk.Button(root, text="Redownload subs", command=redownload)
action_button.place(x=10, y=200)

TextVar = tk.StringVar()
Serieentry = ttk.Entry(root, textvariable=TextVar, width=20, font=("Arial", 9))
Serieentry.place(x=100, y=40)
Serieentry.insert(0, Series)

label = ttk.Label(root, text="Series Name:", foreground="Black", font=("Arial", 9))
label.place(x=20, y=40)

IntVar = tk.StringVar()
Seasonentry = ttk.Entry(root, textvariable=IntVar, width=20, font=("Arial", 9))
Seasonentry.place(x=100, y=80)
Seasonentry.insert(0, Season)

label = ttk.Label(root, text="Season N::", foreground="Black", font=("Arial", 9))
label.place(x=20, y=80)

IntVar2 = tk.IntVar = tk.StringVar()
Episodeentry = ttk.Entry(root, textvariable=IntVar2, width=20, font=("Arial", 9))
Episodeentry.place(x=100, y=120)
Episodeentry.insert(0, Episode)

label = ttk.Label(root, text="Episode N:", foreground="Black", font=("Arial", 9))
label.place(x=20, y=120)

timeentry = ttk.Entry(root, textvariable=Delay, width=20, font=("Arial", 9))
timeentry.place(x=100, y=160)
timeentry.insert(0, Delay)

label = ttk.Label(root, text="Time shift:", foreground="Black", font=("Arial", 9))
label.place(x=20, y=160)

CurentLabel = ttk.Label(root, text=f'Current video: {Series} S{Season} E{Episode}', foreground="Black", font=("Arial", 9))
CurentLabel.place(x=280, y=160)

PrevLabel = ttk.Label(root, text=f'Previous video: {prevSeries} S{prevSeason} E{prevEpisode}', foreground="Black", font=("Arial", 9))
PrevLabel.place(x=280, y=140)


## Load Variables
LoadPrevVariables()
loadVariables()

CurentLabel.config(text=f'Current video: {Series} S{Season} E{Episode}')
PrevLabel.config(text=f'Previous video: {prevSeries} S{prevSeason} E{prevEpisode}')

Label = ttk.Label(root, text=f'Made by ❤️ by Majd', foreground="Black", font=("Arial", 7))
Label.place(x=10, y=230)


root.mainloop()



## Made by ❤️ by Majd
