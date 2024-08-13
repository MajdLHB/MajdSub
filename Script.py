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
import difflib


def RemoveSpaceFromName(Name):
    Name = Name.replace(" ", "")
    return Name

def replacespace(Name):
    Name = Name.replace(" ", "+")
    return Name


current_subtitle_index = 0

## Variables
NameOfPrevSeries = ""
prevSeries = RemoveSpaceFromName(NameOfPrevSeries)
prevSeason =5
prevEpisode =4

responsE = ""

#entry1 = ""
#entry2 = ""
#entry3 = ""
#entry4 = ""

Language = "ar"

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


host = 'localhost'  
port = ''       
password = ''

slug_file_id_list = []
slugList = []

HDTVsub = []
NetflixSub = []
NonHDTVsub = []

SUbToDownload = []

DownloadURL = []

if not os.path.exists(rf'{script_dir}\Subtitles'):
    os.makedirs(rf'{script_dir}\Subtitles')
    FilePath = rf'{script_dir}\Subtitles\MajdSub_{Series}_S{Season}E{Episode}.srt'

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



def SearchForSub(Series, Season, Episode):
    global typeOfContent
    global slug_file_id_list
    global SUbToDownload
    global APiKey
    global Id
    global fileID
    global responsE
    global NameOfSeries

    url = "https://api.opensubtitles.com/api/v1/subtitles"

    querystring = {"type": typeOfContent, "query": NameOfSeries, "languages": Language, "season_number": Season, "episode_number": Episode}

    headers = {
        "User-Agent": "<<MajdSub v0.1>>",
        "Api-Key": APiKey
    }

    response1 = requests.get(url, headers=headers, params=querystring)
    response1 = json.loads(response1.text)
    PageCount = response1['total_pages']
    Subtitles = response1['data']
    print(response1)


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
IsMovie = False

def OpenFile(SeriesFolder, Series, Season, Episode):
    global Vlcpath
    global SubPath
    global IsMovie
    if not IsMovie:
        FirstLetter = Series[0].lower()
        LastLetter = Series[-1].lower()
        match_list = []
        dirname_list = []
        series_pattern = Series.replace(" ", r"[.\-_]*")
        pattern = re.compile(rf"(?i)\b{series_pattern}\b")
        for root, dirs, files in os.walk(Series):
            for file in files:
                if pattern.search(file):
                    match_list.append(os.path.join(root, file))
                    dirname_list.append(dirname)
        if len(match_list) == 0:
            for dirpath, dirnames, filenames in os.walk(SeriesFolder):
                for dirname in dirnames:
                    if FirstLetter in dirname.lower():
                        Start_index = dirname.lower().index(FirstLetter)
                        if LastLetter in dirname[Start_index:]:
                            last_index = dirname[Start_index:].index(LastLetter) + Start_index 
                            match_str = dirname[Start_index:last_index + 1]
                            match_list.append(match_str)
                            dirname_list.append(os.path.join(dirpath, dirname))
            if len(match_list) == 0:
                messagebox.showerror("Error", "No matching series found")
                return
                
        def similarity(a, b):
            a = re.sub(r'[^\w\s]', '', a.lower())
            b = re.sub(r'[^\w\s]', '', b.lower())
            return difflib.SequenceMatcher(None, a, b).ratio()
        
        selected_dir = []

        for match, dirname in zip(match_list, dirname_list):
            if similarity(match, Series) >= 0.75:
                selected_dir.append(dirname)

        
        if not selected_dir and dirname_list:
            selected_dir.append(random.choice(dirname_list))


        season_patterns = [
            f'Season{Season}', f'SEASON 0{Season}', f'season 0{Season}', 
            f'S0{Season}', f's0{Season}', f'S{Season}', f's{Season}',
            f'Season.0{Season}', f'SEASON.0{Season}', f'Season.{Season}', 
            f'SEASON.{Season}', f'Season-0{Season}', f'SEASON-0{Season}',
            f'Season {Season}', f'SEASON {Season}', f'season {Season}',
            f'Season-{Season}', f'SEASON-{Season}', f'season-{Season}',
            f'Season_{Season}', f'SEASON_{Season}', f'season_{Season}',
            f'Season[0{Season}]', f'SEASON[0{Season}]', f'season[0{Season}]',
            f'Season 0{Season}', f'SEASON 0{Season}', f'season 0{Season}',
            f'Season-0{Season}', f'SEASON-0{Season}', f'season-0{Season}'
            ]
            
        SeasonFolder = []

        for season_pattern in season_patterns:
            for SelectedDir in selected_dir:
                if season_pattern in SelectedDir:
                    seasondir = os.path.join(SelectedDir)
                    SeasonFolder.append(seasondir)
                    break
                else:
                    for SelectedDir in selected_dir:
                        for root, dirs, files in os.walk(SelectedDir):
                            for dir in dirs:
                                if season_pattern in dir:
                                    seasonDir = os.path.join(root, dir)
                                    SeasonFolder.append(seasonDir)
                                    break

        episode_patterns = [
            f'EPISODE 0{Episode}', f'episode 0{Episode}', 
            f'E0{Episode}', f'e0{Episode}', 
            f'Episode.0{Episode}', f'EPISODE.0{Episode}',
            f'Episode-0{Episode}', f'EPISODE-0{Episode}'
            ]
        
        episodePath = None
        matchedepisodes = []

        for episode_pattern in episode_patterns:
            #print(episode_pattern)
            for Seasonfolder in SeasonFolder:
                #print(Seasonfolder)
                for root, dirs, files in os.walk(Seasonfolder):
                    #print(files)
                    for file in files:
                        #print(file)
                        if episode_pattern in file:
                            Epath = os.path.join(Seasonfolder, file)
                            matchedepisodes.append(Epath)
                            #print(f"Episode {Episode} found in {Seasonfolder}")
                            if 'mp4' in Epath or 'mkv' in Epath or 'avi' in Epath or 'flv' in Epath or 'mov' in Epath or 'wmv' in Epath or 'webm' in Epath or 'm4v' in Epath or '3gp' in Epath or '3g2' in Epath or 'mpg' in Epath or 'mpeg' in Epath or 'm2v' in Epath or 'm4v' in Epath or 'ts' in Epath or 'vob' in Epath or 'divx' in Epath or 'xvid' in Epath or 'f4v' in Epath or 'rm' in Epath or 'rmvb' in Epath or 'ogv' in Epath or 'ogm' in Epath or 'ogx' in Epath or 'mts' in Epath or 'm2ts' in Epath:
                                break


                        else:
                            episodePath = None
                            #print(f"Episode {Episode} not found in {Seasonfolder}")


        if matchedepisodes == []:
            for folder in SeasonFolder:
                for root, dirs, files in os.walk(folder):
                    files.sort()
                    if len(files) >= int(Episode):
                        Epath = os.path.join(Seasonfolder, file)
                        #print(f"Episode {Episode} found in {folder}")
                        matchedepisodes.append(Epath)
                        break

        if matchedepisodes == None:
            root = tk()
            root.withdraw()
            messagebox.showerror("Error", "Episode not found")
            root.destroy()
    
    #print(matchedepisodes)
    #print(episodePath)
    episodePath = random.choice(matchedepisodes)
    episodePath = episodePath.replace('/', '\\')
    #print(f"Opening {episodePath}")

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
    global current_subtitle_index
    current_subtitle_index = 0
    login()
    saveVariables()
    loadVariables()
    SearchForSub(Series, Season, Episode)
    DownloadSub()
    EncodeSRT(encoding='utf-8')
    OpenFile(SeriesFolder, Series, Season, Episode)
    prevEpisode = Episode
    prevSeason = Season
    NameOfPrevSeries = NameOfSeries
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
    Episode = int(Episode)
    if (Episode < num_episodes):
        Episode += 1
    elif (Episode > num_episodes):
        Episode = 1
        Season = int(Season) + 1

    Episodeentry.delete(0, tk.END)
    Episodeentry.insert(0, Episode)
    Seasonentry.delete(0, tk.END)
    Seasonentry.insert(0, Season)
    change_subtitle_vlc_http(host, port, password, SubPath)
    CurentLabel.config(text=f'Current video: {Series} S{Season} E{Episode}')
    PrevLabel.config(text=f'Previous video: {prevSeries} S{prevSeason} E{prevEpisode}')
    Serieentry.delete(0, tk.END)
    Serieentry.insert(0, NameOfSeries)
    Seasonentry.delete(0, tk.END)
    Seasonentry.insert(0, Season)
    Episodeentry.delete(0, tk.END)
    Episodeentry.insert(0, Episode)
    saveVariables()
    SavePrevVariables()
    LoadPrevVariables()
    loadVariables()
    print(f'prev:{prevEpisode}')


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
    global OSUsername
    global OSPassword
    global APiKey
    global Vlcpath
    global SeriesFolder
    global script_dir
    global THeSHowNAme
    global Language
    global langentry
    Language = langentry.get()
    prevSeries = Series
    prevSeason = Season
    prevEpisode = Episode
    NameOfSeries = Serieentry.get()
    print(NameOfSeries)
    Serieentry.delete(0, tk.END)
    Serieentry.insert(0, NameOfSeries)
    print(NameOfSeries)
    Series = RemoveSpaceFromName(NameOfSeries)
    THeSHowNAme = replacespace(NameOfSeries)
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
    global NameOfSeries
    SeriesPath = rf'{script_dir}\Series.json'
    with open (SeriesPath, 'w') as file:
        json.dump({"variable": NameOfSeries}, file)

def loadSeries():
    global NameOfSeries
    global Series
    global THeSHowNAme
    SeriesPath = rf'{script_dir}\Series.json'
    with open (SeriesPath, 'r') as file:
        data = json.load(file)
        NameOfSeries = data['variable']
        Series = RemoveSpaceFromName(NameOfSeries)
        THeSHowNAme = replacespace(NameOfSeries)

def saveLanguage():
    global Language
    LanguagePath = rf'{script_dir}\Language.json'
    with open (LanguagePath, 'w') as file:
        json.dump({"variable": Language}, file)

def loadLanguage():
    global Language
    LanguagePath = rf'{script_dir}\Language.json'
    with open (LanguagePath, 'r') as file:
        data = json.load(file)
        Language = data['variable']

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
    saveLanguage()

def loadVariables():
    global Episodeentry
    global Seasonentry
    global Serieentry
    global Episode
    global Season
    global NameOfSeries
    global Language
    global langentry
    loadEpisode()
    loadSeason()
    loadSeries()
    loadLanguage()
    Episodeentry.delete(0, tk.END)
    Episodeentry.insert(0, Episode)
    Seasonentry.delete(0, tk.END)
    Seasonentry.insert(0, Season)
    Serieentry.delete(0, tk.END)
    Serieentry.insert(0, NameOfSeries)
    langentry.delete(0, tk.END)
    langentry.insert(0, Language)



Load_OS_Login_data()
LoadVLCData()


def redownload():
    global current_index
    global vlc
    global SubPath
    global host
    global port
    global password
    if current_index < len(slug_file_id_list):
        element = slug_file_id_list[current_index]
        CurrentSubName.config(text=f"Current Sub: {element['slug']}")
        Id.FileID = element['file_id']
    else:
        messagebox.showinfo("Info", "End of list reached")
    DownloadSub()
    EncodeSRT(encoding='utf-8')

def change_to_next_subtitle_vlc_http(host, port, password):
    global current_subtitle_index
    url = f'http://{host}:{port}/requests/status.xml'
    headers = {'User-Agent': 'Mozilla/5.0'}
    auth = requests.auth.HTTPBasicAuth('', password)  
    current_subtitle_index += 1 #Delete this if your video has only one subtitle track
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
    
    #DownloadSelection = ttk.Button(winmdow,text="Download selection")
    #DownloadSelection.place(x=260, y=360)

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

    entry6 = ttk.Entry(window, width=20, font=("Arial, 12"), show="*")
    entry6.place(x=580, y=60)
    entry6.delete(0, tk.END)
    entry6.insert(0, password)

    label6 = ttk.Label(window, text="Vlc http port:", font=("Arial, 10"))
    label6.place(x=450, y=110)

    entry7 = ttk.Entry(window, width=20, font=("Arial, 12"))
    entry7.place(x=580, y=110)
    entry7.delete(0, tk.END)
    entry7.insert(0, port)

    label7 = ttk.Label(window, text="Vlc http host:", font=("Arial, 10"))
    label7.place(x=450, y=160)

    entry8 = ttk.Entry(window, width=20, font=("Arial, 12"))
    entry8.place(x=580, y=160)
    entry8.delete(0, tk.END)
    entry8.insert(0, host)

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
        host = entry8.get()
        port = entry7.get()
        password = entry6.get()
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


def downloadSub():
    global Series
    global Season
    global Episode
    login()
    SearchForSub(Series, Season, Episode)
    DownloadSub()
    EncodeSRT(encoding='utf-8')


os.environ["PATH"] += os.pathsep + Vlcpath


subprocess.run([
    'setx', 'PATH', os.environ["PATH"]
], shell=True)


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

action_button = ttk.Button(root, text="Download sub", command=downloadSub)
action_button.place(x=280, y=90)

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


Serieentry = ttk.Entry(root, width=20, font=("Arial", 9))
Serieentry.place(x=100, y=40)
Serieentry.insert(0, NameOfSeries)


label = ttk.Label(root, text="Series Name:", foreground="Black", font=("Arial", 9))
label.place(x=20, y=40)


Seasonentry = ttk.Entry(root, width=20, font=("Arial", 9))
Seasonentry.place(x=100, y=80)
Seasonentry.insert(0, Season)

label = ttk.Label(root, text="Season N::", foreground="Black", font=("Arial", 9))
label.place(x=20, y=80)


Episodeentry = ttk.Entry(root, width=20, font=("Arial", 9))
Episodeentry.place(x=100, y=120)
Episodeentry.insert(0, Episode)

label = ttk.Label(root, text="Episode N:", foreground="Black", font=("Arial", 9))
label.place(x=20, y=120)

timeentry = ttk.Entry(root, width=7, font=("Arial", 9))
timeentry.place(x=100, y=160)
timeentry.insert(0, Delay)

label = ttk.Label(root, text="Time shift:", foreground="Black", font=("Arial", 9))
label.place(x=20, y=160)

langentry = ttk.Entry(root, width=6, font=("Arial", 9))
langentry.place(x=200, y=160)
langentry.insert(0, Language)

lang = ttk.Label(root, text="lang:", foreground="Black", font=("Arial", 9))
lang.place(x=160, y=160)

CurentLabel = ttk.Label(root, text=f'Current video: {Series} S{Season} E{Episode}', foreground="Black", font=("Arial", 9))
CurentLabel.place(x=280, y=160)

PrevLabel = ttk.Label(root, text=f'Previous video: {prevSeries} S{prevSeason} E{prevEpisode}', foreground="Black", font=("Arial", 9))
PrevLabel.place(x=280, y=140)


## Load Variables
LoadPrevVariables()
loadVariables()

CurentLabel.config(text=f'Current video: {Series} S{Season} E{Episode}')
PrevLabel.config(text=f'Previous video: {prevSeries} S{prevSeason} E{prevEpisode}')

Label = ttk.Label(root, text=f'Made with ❤️ by Majd', foreground="Black", font=("Arial", 7))
Label.place(x=10, y=230)


root.mainloop()



## Made with ❤️ by Majd
