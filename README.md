

```markdown
# MajdSub
```

## Overview

A Python script in pre-alpha that integrates OpenSubtitle and Maze-TV APIs to fetch Arabic (and more languages) subtitles (and encode them in UTF-8) and episode counts, manages local series files, and controls VLC for seamless fullscreen playback with subtitles.

## Features

- **Subtitle Download and Encoding**: Automatically downloads subtitles for your episodes and encodes them to UTF-8.
- **Episode Tracking**: Uses the Maze-TV API to track the number of episodes in the series you are watching and saves the last episode you watched.
- **Automated Playback**: Searches for the episode in your local files and opens it directly in VLC media player with the encoded subtitles.
- **Next Episode Handling**: By pressing the 'Next' button, the script fetches the next available subtitle from OpenSubtitles and adds it to VLC.
- **GUI**: Utilizes Tkinter for a user-friendly graphical interface.
- **Future Support for Movies**: Planned updates to handle movies.
- **Multi-language Support**: Plans to expand subtitle download options to include all languages supported by OpenSubtitles.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MajdLHB/MajdSub.git
   cd MajdSub
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up VLC HTTP Interface**:
   - Open VLC media player.
   - Go to `Tools > Preferences`.
   - Under `Show settings`, select `All`.
   - Navigate to `Interface > Main interfaces > Lua`.
   - Set the password and ensure the HTTP interface is enabled.
   - Update the port and password in the script accordingly.

4. **Update Configuration**:
   - Replace placeholder paths, API keys, and other configurations in the script with your own.

## Directory Structure

- The series must be organized as follows:
  - A folder with the series name without spaces.
  - Inside this folder, a subfolder for each season (e.g., `s1` or `S01`).
  - Each episode file must have the letter 'e' followed by the episode number in its name (e.g., `e01`).

## Usage

1. **Run the Script**:
   ```bash
   python script.py
   ```

2. **Graphical User Interface**:
   - Use the GUI to select the series and episode you want to watch.
   - The script will handle downloading and encoding the subtitle, then open the episode in VLC.

## Configuration Files

- **APIKey.json**: Store your API key for OpenSubtitles.
- **Episode.json**: Configuration for the current episode.
- **OSPassword.json**: Store your OpenSubtitles password.
- **OSUsername.json**: Store your OpenSubtitles username.
- **PrevEpisode.json**: Store information about the previous episode watched.
- **PrevSeason.json**: Store information about the previous season watched.
- **PrevSeries.json**: Store information about the previous series watched.

## Contributing

Feel free to contribute to the project by:
- Forking the repository.
- Creating a new branch (`git checkout -b feature-branch`).
- Making your changes.
- Submitting a pull request.

## License

This project is open-source and available under the MIT License. 

## Support

For any issues or feature requests, please open an issue on the [GitHub repository](https://github.com/MajdLHB/MajdSub/issues).

## Acknowledgments

- [OpenSubtitles API](https://www.opensubtitles.com) for providing subtitle data.
- [Maze-TV API](https://www.maze.tv) for episode tracking.
- [VLC Media Player](https://www.videolan.org/vlc/index.html) for media playback.

---

**Note**: This script is still in pre-alpha mode. Please ensure you update the file paths, API keys, and other configurations to match your setup.

