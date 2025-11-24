#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import commands


parser = argparse.ArgumentParser(
    description="get info from a file by running standard linux commands on the file and generate a report.txt"
)
parser.add_argument("-f", "--file", type=str, metavar="filename", required=True)
parser.add_argument("-o", "--output", type=str, metavar="report")

if len(sys.argv) == 1:
    commands.ascii_art()
    parser.print_help()
    sys.exit(0)

args = parser.parse_args()
filename = args.file

if args.output != None:
    commands.report_file = args.output

if os.path.exists(filename):
    pass
else:
    print(f'The file "{filename}" doesnt exist!')
    exit(0)

# Start of commands to run for any files
res = commands.file_type_identifier(filename)
commands.exiftool_command(filename)
commands.binwalk_command(filename)
commands.xxd_command(filename)
# End of commands to run for any files

if res == "image":
    commands.pngcheck_command(filename)
    commands.zsteg_command(filename)
    commands.steghide_command(filename)

elif res == "pdf":
    commands.pdfinfo_command(filename)
    commands.pdfimages_command(filename)
    commands.pdftotext_command(filename)

elif res == "audio":
    commands.soxi_command(filename)
    commands.steghide_command(filename)

elif res == "archive":
    commands.seven_zip_command(filename)

elif res == "document":
    commands.unzip_command(filename)
    commands.olevba_command(filename)
    commands.docx2txt_command(filename)

elif res == "image_disk":
    commands.fdisk_command(filename)
    commands.mmls_command(filename)

elif res == "executable":
    commands.checksec_command(filename)
    commands.nm_command(filename)
    commands.objdump_command(filename)

elif res == "database":
    commands.sqlite3_command(filename)

else:
    print("\nThis file type is not supported :(")
    print(f'GO CHECK THE FILE: "{commands.report_file}"\n')
    exit(0)

print(f'\nGO CHECK THE FILE: "{commands.report_file}"\n')
