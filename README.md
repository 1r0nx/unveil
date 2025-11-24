# Unveil

## 🛠️ Overview

**Unveil** is a flexible command-line tool designed to analyse a file by executing specific commands based on their detected file type. It's a "cold" analysis; that means it's not going to try to extract something.

Its main goal is to automate file analysis and processing by applying predefined actions depending on the file format (PDF, ZIP, image, binary, etc.).

In the repository are saved the commands to run on the file provided, so no need to have them installed on your machine.

```
The commands: 

src/bin
├── 7z
├── binwalk
├── checksec
├── docx2txt
├── exiftool
├── fdisk
├── ffmpeg
├── file
├── mmls
├── nm
├── objdump
├── olevba
├── pdfimages
├── pdfinfo
├── pdftotext
├── pngcheck
├── soxi
├── sqlite3
├── steghide
├── unzip
├── xxd
└── zsteg

```

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

## 📦 Installation

```

Clone directly:

```bash
git clone https://github.com/1r0nx/unveil.git
cd unveil
./build.sh
```

```
The executable will be is in dist/
You can save it where ever you want to use it at standard linux command!
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

## 📂 Supported File Types (example)

- Image
- Pdf
- Audio
- Archive
- Document
- Image disk
- Executable
- Database

## 🧩 How It Works

1. Detects file type using magic bytes or file signature
2. Matches file type with a predefined rule
3. Executes associated command
4. Stores output in report file

---

## 🛡️ Security Considerations

* Avoid running on untrusted files without sandboxing
* Commands are executed in a system shell

---

## 📜 License

MIT License

---

## 🙋 Contributing

Pull Requests and suggestions are welcome. Please follow standard coding practices and document your changes.

---

## 📫 Contact

Author: ir0nx
Project: unveil
