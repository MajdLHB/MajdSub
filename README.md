# Subtitle Automation Script

## Overview

This Python script automates the process of downloading and encoding subtitles for TV series. It leverages the OpenSubtitles API for subtitles and the Maze-TV API to track and manage episodes. The script is currently in beta mode and works with your local VLC media player to play episodes with the downloaded subtitles.

## Features

- **Subtitle Download and Encoding**: Automatically downloads Arabic subtitles for your episodes and encodes them to UTF-8.
- **Episode Tracking**: Uses the Maze-TV API to track the number of episodes in the series you are watching and saves the last episode you watched.
- **Automated Playback**: Searches for the episode in your local files and opens it directly in VLC media player with the encoded subtitles.
- **Next Episode Handling**: By pressing the 'Next' button, the script fetches the next available subtitle from OpenSubtitles and adds it to VLC.
- **GUI**: Utilizes Tkinter for a user-friendly graphical interface.

## Future Plans

- **Support for Movies**: The script will be updated to handle movies, making it versatile for both TV series and films.
- **Multi-language Support**: Plans to expand subtitle download options to include all languages supported by OpenSubtitles.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/subtitle-automation-script.git
   cd subtitle-automation-script
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Up VLC HTTP Interface:

Open VLC media player.
Go to Tools > Preferences.
Under Show settings, select All.
Navigate to Interface > Main interfaces > Lua.
Set the password and ensure the HTTP interface is enabled.
Update the port and password in the script accordingly.
Update Configuration:

Replace placeholder paths, API keys, and other configurations in the script with your own.
Directory Structure
The series must be organized as follows:
A folder with the series name without spaces.
Inside this folder, a subfolder for each season (e.g., s1 or S01).
Each episode file must have the letter 'e' followed by the episode number in its name (e.g., e01).
Usage
Run the Script:

bash
Copy code
python main.py
Graphical User Interface:

Use the GUI to select the series and episode you want to watch.
The script will handle downloading and encoding the subtitle, then open the episode in VLC.
Contributing
Feel free to contribute to the project by:

Forking the repository.
Creating a new branch (git checkout -b feature-branch).
Making your changes.
Submitting a pull request.
License
This project is open-source and available under the MIT License. See the LICENSE file for more information.

Support
For any issues or feature requests, please open an issue on the GitHub repository.

Acknowledgments
OpenSubtitles API for providing subtitle data.
Maze-TV API for episode tracking.
VLC Media Player for media playback.
Note: This script is still in beta mode. Please ensure you update the file paths, API keys, and other configurations to match your setup.

Feel free to adjust the content as per your specific requirements or preferences.
