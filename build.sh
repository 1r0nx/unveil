#!/usr/bin/bash
pyinstaller --onefile --add-binary "src/bin/*:bin" --name unveil src/unveil.py