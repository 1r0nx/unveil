#!/usr/bin/bash

pyinstaller --onefile --name unveil src/unveil.py
#sudo cp dist/unveil /usr/bin/unveil