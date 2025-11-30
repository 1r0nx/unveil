#!/usr/bin/bash

commands=("binutils" "poppler-utils" "sleuthkit" "7zip" "binwalk" "checksec" "steghide" "docx2txt" "libimage-exiftool-perl" "fdisk" "ffmpeg" "file" "pngcheck" "sqlite3" "unzip" "xxd" "ruby-rubygems" "odt2txt")

for tool in "${commands[@]}"
do
	echo "-----------> INSTALLING/CHECKING $tool"
	sudo apt-get install $tool -y
	echo -e ""
done

echo "-----------> INSTALLING/CHECKING zsteg"
sudo gem install zsteg

## Uncomment the following lines to set a python3-venv in ~/Documents/Python
#if [ -n "$VIRTUAL_ENV" ]; then
#    echo "A python-venv is already set as: $VIRTUAL_ENV"
#else
#    sudo apt-get install python3 python3-venv
#    python3 -m venv ~/Documents/Python
#    pip3 install oletools
#fi