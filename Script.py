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

FilePath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\Movies\Subtitles\MajdSub_{Series}_S{Season}E{Episode}.srt'
SeriesFolder = rf'C:\Users\majdl\OneDrive\Desktop\Majd\Movies'
SubPath = ""

current_index = 1


## VAriable Class
class Id:
    FileID = 0

## Functions
def login():
    url = "https://api.opensubtitles.com/api/v1/login"

    payload ={
        "username": "Majdl",
        "password": "Moj2008."
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "<<MajdSub v0.1>>",
        "Accept": "application/json",
        "Api-Key": "boSWYGhOSq3uTdOAvGaDEolYoS1AZYVe"
    }

    response = requests.post(url, json=payload, headers=headers)

def SearchForSub():
    url = "https://api.opensubtitles.com/api/v1/subtitles"

    querystring = {"type": typeOfContent,"query": Series,"languages":"ar","season_number": Season,"episode_number": Episode}

    headers = {
        "User-Agent": "<<MajdSub v0.1>>",
        "Api-Key": "boSWYGhOSq3uTdOAvGaDEolYoS1AZYVe"
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
    global FilePath
    url = "https://api.opensubtitles.com/api/v1/download"

    payload = {"file_id": Id.FileID, "timeshift": Delay}
    
    headers = {
        "User-Agent": "<<MajdSub V1.0>>",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Api-Key": "boSWYGhOSq3uTdOAvGaDEolYoS1AZYVe"
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
    print(episodePath)
    vlc_path = r'C:\Program Files\VideoLAN\VLC\vlc.exe'
    vlc_command = [
    vlc_path,
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
    FilePath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\Movies\Subtitles\MajdSub_{Series}_S{SeasonSubName}E{EpisodeSubNAme}.srt'
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

def SetVAr():
    IsHDTV = var.get()
    print(f'h:{IsHDTV}')

def SetVAr2():
    IsNetflix = var2.get()
    print(f'n:{IsNetflix}')

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
    FilePath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\Movies\Subtitles\MajdSub_{Series}_S{SeasonSubName}E{EpisodeSubNAme}.srt'

def get_show_id(SerieName):
    search_url = f"http://api.tvmaze.com/search/shows?q={SerieName}"
    response = requests.get(search_url)
    data = response.json()
    if data:
        return data[0]['show']['id']
    else:
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
    EpisodePath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\CodeProjects\PythonSeriesplayer\Episode.json'
    with open (EpisodePath, 'w') as file:
        json.dump({"variable": Episode}, file)

def loadEpisode():
    global Episode
    EpisodePath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\CodeProjects\PythonSeriesplayer\Episode.json'
    with open (EpisodePath, 'r') as file:
        data = json.load(file)
        Episode = data['variable']

def saveSeason():
    global Season
    SeasonPath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\CodeProjects\PythonSeriesplayer\Season.json'
    with open (SeasonPath, 'w') as file:
        json.dump({"variable": Season}, file)

def loadSeason():
    global Season
    SeasonPath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\CodeProjects\PythonSeriesplayer\Season.json'
    with open (SeasonPath, 'r') as file:
        data = json.load(file)
        Season = data['variable']

def saveSeries():
    global Series
    SeriesPath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\CodeProjects\PythonSeriesplayer\Series.json'
    with open (SeriesPath, 'w') as file:
        json.dump({"variable": Series}, file)

def loadSeries():
    global Series
    SeriesPath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\CodeProjects\PythonSeriesplayer\Series.json'
    with open (SeriesPath, 'r') as file:
        data = json.load(file)
        Series = data['variable']

def SavePrevVariables():
    global prevSeries
    global prevSeason
    global prevEpisode
    prevSeriesPath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\CodeProjects\PythonSeriesplayer\prevSeries.json'
    prevSeasonPath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\CodeProjects\PythonSeriesplayer\prevSeason.json'
    prevEpisodePath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\CodeProjects\PythonSeriesplayer\prevEpisode.json'
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
    prevSeriesPath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\CodeProjects\PythonSeriesplayer\prevSeries.json'
    prevSeasonPath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\CodeProjects\PythonSeriesplayer\prevSeason.json'
    prevEpisodePath = rf'C:\Users\majdl\OneDrive\Desktop\Majd\CodeProjects\PythonSeriesplayer\prevEpisode.json'
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

## GUI
root = tk.Tk()
root.title("MajdSub V1.0")
style = ttk.Style()
style.theme_use('vista')

root.geometry("485x230")

label = ttk.Label(root, text="Welcome to MajdSub V1.0", foreground="Black", font=("Arial", 15))
label.pack()

action_button = ttk.Button(root, text="Play", command=play)
action_button.place(x=400, y=200)

action_button = ttk.Button(root, text="NextSub", command=NextSub)
action_button.place(x=400, y=60)

CurrentSubName = ttk.Label(root, text="SubName", foreground="Black", font=("Arial", 9))
CurrentSubName.place(x=250, y=40)

action_button = ttk.Button(root, text="Set up")
action_button.place(x=310, y=200)

action_button = ttk.Button(root, text="Update", command=update)
action_button.place(x=220, y=200)

action_button = ttk.Button(root, text="Show Subs")
action_button.place(x=130, y=200)

action_button = ttk.Button(root, text="Redownload Subs", command=redownload)
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

root.mainloop()


## Made by love by Majd