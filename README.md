# MusicBox  
**(Android app experiment to download music using yt-dlp and Python)**

This project is a simple attempt to create an Android app that downloads music via YouTube playlists. It uses Python and yt-dlp. Due to permission restrictions in the Play Store version of Termux, I didn’t finish the full app with a proper interface. However, you *can* run the Python script in Termux to download music.

## How does it work?  
- All the core Python files are located in the `/modules` folder (other files can be ignored). Run the script by executing `main.py`.
- Music is downloaded into a folder named `/AIMP` located at the same directory level as `/modules`.  
  - If you download a playlist, it creates a folder with the playlist’s name inside `/AIMP`.
  - If the playlist was downloaded before, it will try to find and download only new songs, updating the playlist folder.
  - **Note:** The folder is named **AIMP** because that's the music player I use, but you can rename it to whatever you prefer.
- When you run the script, simply provide the URL of the YouTube playlist, and it will download or update the music accordingly.
  - Update the playlist means:
    - It deletes all the local songs that are no longer in the playlist
    - It downloads the songs that are not in local but in the playlist.
- Example folder structure (if you put the project inside your `Downloads` folder):
downloads/
├── AIMP    # All downloaded music
└── modules # Python source files
- Note: The name of the files has the video id. That's because, if two songs have the same name, the program may fail updating the playlist.

---

## Requirements  
- The YouTube playlist **must be at least Unlisted** (Private playlists will cause the program to fail).  
- It's recommended to manually remove unavailable videos from the playlist to avoid delays during downloading.

---

## How to use it on your mobile device (with Termux)

1. Install **Termux** from the Play Store.

2. Open Termux and paste the next 4 commands
```bash
termux-setup-storage
```
```bash
pkg install git
```
```bash
git clone https://github.com/Bejmo/MusicBox.git
```
```bash
sh ./MusicBox/modules/install.sh
```

3. Reboot **Termux** and you will be able to execute the scrit by just typing `yt` on **Termux**.

---

## Known issues & future improvements

- **Unavailable videos in playlists:** These need to be removed manually for smoother operation. You can find a list of problematic videos in `error_logs_not_saved.txt` (after you execute the script).
- **Album art may be missing:** Sometimes the metadata (including cover art) isn’t properly saved on some files (if the portrait is not downlaoded, you can see the missing song in `error_logs_not_saved.txt`).
- **Update functionality:** Currently, the script only adds new songs from the playlist but does not remove files that no longer exist in the playlist. I'd like to add this feature in the future.

---

## 🚨 **Legal Warning** 🚨

This script uses **yt-dlp**, a tool for downloading content from various websites, including videos and audio. 

**Usage of this script to download copyrighted content without proper authorization may violate terms of service of platforms and copyright laws in many jurisdictions.**

### Responsible Use:
- Use this script only to download content that is legally available or has a license allowing download.
- **Do not use this script to download copyrighted content without explicit permission from the copyright holder.**
- The repository maintainer is not responsible for any illegal or improper use of this script.

By using this script, you agree that you are fully responsible for your actions and must comply with all local laws and platform terms of service.




## COMMANDS FOR DEVELOPERS
- Install dependencies
  - pip install -r dependencies.txt
- Put on the server:
  - uvicorn main_fastAPI:app --reload
- Server dependencies:
  - pip install python-multipart fastapi uvicorn gtts