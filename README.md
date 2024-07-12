# MajdSub
Certainly! Here's a brief README draft for your GitHub repository:

---

# Series Subtitle Installer (Pre-Alpha)

This Python script, currently in pre-alpha development, integrates multiple APIs and local file management to enhance your series watching experience. It utilizes the OpenSubtitle API to fetch and install Arabic subtitles encoded in UTF-8, ensuring seamless viewing. The Maze-TV API integration retrieves the number of episodes in a series, facilitating automatic episode management and continuity between sessions. 

## Features:
- **Subtitle Management:** Automatically installs Arabic subtitles for series episodes.
- **Episode Count:** Fetches and displays the total number of episodes in a series from Maze-TV API.
- **Local File Handling:** Searches and plays episodes from local directories organized by series and season folders (e.g., 'SeriesName/S01/e01.mp4').
- **VLC Integration:** Controls VLC media player via its HTTP interface for fullscreen playback with added subtitles. Ensure VLC is configured (Preferences > Main Interface > Lua HTTP interface).

## Requirements:
- Python 3.x
- Tkinter (usually included with Python)
- VLC media player with Lua HTTP interface enabled

## Usage:
1. Clone the repository.
2. Set up API keys and file paths in the script.
3. Organize series episodes in the specified folder structure.
4. Run the script and use the GUI to search, select, and play episodes with subtitles.

## Configuration:
- Replace placeholders (`YOUR_API_KEY`, `PATH_TO_FILES`) with your specific credentials and paths.(For now the script uses my API key and my file paths intil the release)
- Ensure VLC HTTP interface settings match those in the script (Tools > Preferences > Main Interface > Lua HTTP).

## Notes:
This project is in pre-alpha stage, under active development. Feedback and contributions are welcome to improve functionality and usability.



Feel free to adjust and expand upon this template according to your project's specifics and ongoing developments!
