#!/usr/bin/bash

commands=("binutils" "poppler-utils" "sleuthkit" "7zip" "binwalk" "checksec" "steghide" "docx2txt" "exiftool" "fdisk" "ffmpeg" "file" "pngcheck" "sqlite3" "unzip" "xxd" "ruby-rubygems")

for tool in "${commands[@]}"
do
	echo "-----------> INSTALLING/CHECKING $tool"
	sudo apt-get install $tool -y
	echo -e ""
done

echo "-----------> INSTALLING/CHECKING zsteg"
sudo gem install zsteg