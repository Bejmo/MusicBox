# MusicBox
Android App to download music (uses yt-dlp with Python).

## Requirements
- To use `terminal_mobile.py`, the folder AIMP must be next to this program's folder.
- The YouTube playlist that you use must:
  -  Be AT LEAST Unlisted (CAN'T BE PRIVATE, OR THE PROGRAM WILL FAIL).
  -  Sorted by "Date added (newest)" (if you want to use the "Update" function)
- It is recommended to delete all the unavaliable videos from the YouTube playlist. It may cause a delay on the download.

## Further work and some problems
- Delete the unavailable videos of the playlist sent. This has to be done manually, but I want to automate it.
  - You can see them in `error_logs_not_saved.txt`.
- Ensure all the dowloaded songs have portrait (in the portrait is not downlaoded, you can see the song in `error_logs_not_saved.txt`).
  - Some times (I don't really know why) it just doesn't put the metadata on the files.