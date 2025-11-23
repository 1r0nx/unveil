#!/usr/bin/zsh
pyinstaller --onefile --add-binary "src/bin/*:bin" --name unveil src/unveil.py