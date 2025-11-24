# Unveil

## 🛠️ Overview

**Unveil** is a flexible command-line tool designed to analyse a file by executing specific commands based on their detected file type. It's a "cold" analysis; that means it's not going to try to extract something.

Its main goal is to automate file analysis and processing by applying predefined actions depending on the file format (PDF, ZIP, image, binary, etc.).

This tool is especially useful for:

* File analysis and forensics
* Pentesting and CTF challenges
* Automation of repetitive file inspection tasks

---

## 🚀 Features

* Automatic file type detection
* Rule-based command execution
* Support for multiple file formats

---

## 🧱 Requirements
You need to have pyinstaller to compile the source code into binary. You can install it with:
```
pip3 install pyinstaller
```

And all commands to be run (you need to have them on you machine):
```
7z
binwalk
checksec
docs2txt
exiftool
fdisk 
ffmpeg 
file 
mmls
nm 
objdump 
pdfimages 
pdfinfo 
pdftotext 
pngcheck 
soxi 
sqlite3 
unzip 
xxd 
zsteg 
olevba
```

The script install_commands.sh from the repository will install the commands automatically. But for olevba you need to have a python-venv set. How to to do it:
```bash
sudo apt-get install python3 python3-venv
python3 -m venv /path/to/venv
pip3 install oletools
```
Notes: In the ./intall_commands.sh you can uncomments the last lines to set the venv to ~/Documents/Python

---

## 📦 Installation
You can install it by cloning the repository and build the binary
```
git clone https://github.com/1r0nx/unveil.git;
cd unveil;
chmod +x *.sh;
./install_commands.sh;
./build.sh;
```

```
The executable will be in dist/
You can save it where ever you want and use it as a standard linux command!
```

Or you can run the script normally
```
chmod +x unveil.py
./unveil.py
```
---

## ⚙️ Usage

```bash
unveil -f <file> -o <report_file>
```

Example:

```bash
unveil -f suspicious_file.bin -o suspicisous_report.txt
```

---

## 📂 Supported File Types

- Image
- Pdf
- Audio
- Archive
- Document
- Image disk
- Executable
- Database

## 🧩 How It Works

1. Matches file type with a predefined rule
2. Executes associated command
3. Stores output in report file

---

## 🛡️ Security Considerations

* Commands are executed in a system shell

---

## 📜 License

MIT License

---

## 🙋 Contributing

Pull Requests and suggestions are welcome. Please follow standard coding practices and document your changes.


