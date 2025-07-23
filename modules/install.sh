# FOLLOW THE INSTRUCTIONS FROM THE README.md

# termux-setup-storage
# pkg install git
# git clone https://github.com/Bejmo/MusicBox.git
# sh ./MusicBox/modules/install.sh

mv ./MusicBox/modules ./storage/downloads/MusicBox
cd
pkg update
pkg install python libjpeg-turbo libpng zlib clang make ffmpeg
pip install yt-dlp mutagen requests Pillow

echo "cd storage/downloads/MusicBox" > musicbox.sh
echo "python3 main.py" >> musicbox.sh

echo "alias yt=\"sh musicbox.sh\"" >> ~/.bashrc

rm -rf ./MusicBox