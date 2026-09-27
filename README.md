# Unveil

## 🛠️ Overview

**Unveil** is a flexible command-line tool designed to analyse a file by executing specific commands based on their detected file type. It's a "cold" analysis; that means it's not going to try to extract something (apart from text or macros).

Its main goal is to automate file analysis and processing by applying predefined actions depending on the file format (PDF, ZIP, image, binary, etc.).

This tool is especially useful for:

* File analysis and forensics
* Pentesting and CTF challenges
* Automation of repetitive file inspection tasks

---

## 🧩 How It Works

1. Matches file type with a predefined rule
2. Force a filetype with option if not detected by rule
3. Executes associated command
4. Stores output in report file

---

## 🧱 Requirements

The only Python dependency is **python-magic** (which needs the system `libmagic`):
```
pip3 install -r requirements.txt      # installs python-magic
sudo apt-get install libmagic1        # system library used by python-magic
```
Optionally, **pyinstaller** to compile the source into a binary:
```
pip3 install pyinstaller
```

And all commands to be run (you need to have them on you machine):
```
7z
binwalk
checksec
docx2txt
odt2txt
exiftool
fdisk 
ffmpeg 
ffprobe
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

The script install_commands.sh from this repository will install the commands automatically. But for olevba you need to have a python-venv set. How to to do it:
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
chmod +x install_commands.sh;
pip3 install -r requirements.txt;
./install_commands.sh;
pyinstaller --onefile --name unveil src/unveil.py;
sudo cp dist/unveil /usr/bin/;
```
You can now use it as standard linux command!


Or you can run the script normally (from the `src/` directory, as `unveil.py`
imports its sibling `commands.py`):
```
cd src
python3 unveil.py -f <file>
```
---

## ⚙️ Usage

```bash
unveil -f <file> -o <report_file> -t <filetype>
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
- Video
- Archive
- Document
- Image disk
- Executable
- Database

---

## 🛡️ Security Considerations

* External tools are invoked directly via `subprocess` with an argument list and **no shell**, so filenames are not subject to shell injection.
* Each tool runs with a timeout and missing tools are skipped, so a hostile or malformed file cannot hang or crash the analysis.

---

## 🧪 Tests

The test suite in `test/` covers file-type detection (against the samples in
`test_files/`), tool-presence checks, report generation, and the graceful
"tool not installed" path. It needs `python-magic` (+ `libmagic`) but not the
external analysis tools.

```bash
pip install -r requirements.txt pytest
pytest
```

Tests also run on every push and pull request via GitHub Actions
(`.github/workflows/tests.yml`), across Python 3.8, 3.11 and 3.12.

---

## 📜 License

MIT License

---

## 🙋 Contributing

Pull Requests and suggestions are welcome. Please follow standard coding practices and document your changes.


