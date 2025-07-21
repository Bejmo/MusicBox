# MusicBox  
**(Android app experiment to download music using yt-dlp and Python)**

This project is a simple attempt to create an Android app that downloads music via YouTube playlists. It uses Python and yt-dlp. Due to permission restrictions in the Play Store version of Termux, I didn’t finish the full app with a proper interface. However, you *can* run the Python script in Termux to download music—though the interface is quite basic.

## How does it work?  
- All the core Python files are located in the `/modules` folder (other files can be ignored). Run the script by executing `main.py`.
- Music is downloaded into a folder named `/AIMP` located at the same directory level as `/modules`.  
  - If you download a playlist, it creates a folder with the playlist’s name inside `/AIMP`.
  - If the playlist was downloaded before, it will try to find and download only new songs, updating the playlist folder.
  - **Note:** The folder is named **AIMP** because that's the music player I use, but you can rename it to whatever you prefer.
- When you run the script, simply provide the URL of the YouTube playlist, and it will download or update the music accordingly.
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

1. Choose a folder on your device to place the `/modules` folder from this repository. You can rename it—I'll use **MusicBox** as an example.  
   Recommended location: `/storage/downloads/MusicBox`

   *Tip:* Use the **Files** app on Android for easy folder creation.

2. Install **Termux** from the Play Store.

3. Open Termux and give it permission to access your storage by running:
```bash
termux-setup-storage
```

4. Then, you need to install Python and all the packages needed. Just paste all these commands:
```bash
  pkg update
  pkg install python libjpeg-turbo libpng zlib clang make ffmpeg
  pip install yt-dlp mutagen requests Pillow
```

1. Create a simple shell script to run the downloader:
```bash
  nano download_yt.sh
```
Paste the following:
```
  cd storage/downloads/MusicBox
  python3 main.py
```
Save the file (`Ctrl + S`) and exit (`Ctrl + X`).


6. Run the script by typing:
```bash
  sh download_yt.sh
```
But if you want it to be shorter, go to pass number 7.

7. *(Optional but recommended)* Create a shortcut command to run the script easily:
```bash
  nano ~/.bashrc
```
Add this line at the end (you can change `yt` to any command you prefer):
```bash
  alias yt="sh download_yt.sh"
```
Save the file (`Ctrl + S`) and exit (`Ctrl + X`).

8. Reboot **Termux** and you will be able to execute the scrit by just typing `yt` on **Termux**.


## Known issues & future improvements

- **Unavailable videos in playlists:** These need to be removed manually for smoother operation. You can find a list of problematic videos in `error_logs_not_saved.txt` (after you execute the script).
- **Album art may be missing:** Sometimes the metadata (including cover art) isn’t properly saved on some files (if the portrait is not downlaoded, you can see the missing song in `error_logs_not_saved.txt`).
- **Update functionality:** Currently, the script only adds new songs from the playlist but does not remove files that no longer exist in the playlist. I'd like to add this feature in the future.