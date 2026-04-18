#!/usr/bin/env python3

import os
import sys
import argparse
import commands

# ─── CLI ──────────────────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(
    description="Analyse a file using standard Linux tools and generate a structured report.",
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    "-f", "--file",
    type=str,
    metavar="FILE",
    required=True,
    help="Path to the file to analyse",
)
parser.add_argument(
    "-o", "--output",
    type=str,
    metavar="REPORT",
    default=None,
    help="Output report filename (default: unveil.txt)",
)
parser.add_argument(
    "-t", "--type",
    type=str,
    metavar="TYPE",
    default=None,
    choices=commands.VALID_TYPES,
    help=(
        "Force a specific file type instead of auto-detection.\n"
        "Supported values: " + ", ".join(commands.VALID_TYPES)
    ),
)

# Show help + art when called with no arguments
if len(sys.argv) == 1:
    commands.ascii_art()
    parser.print_help()
    sys.exit(0)

args = parser.parse_args()
filename = args.file

# ─── Output file ──────────────────────────────────────────────────────────────

if args.output is not None:
    commands.report_file = args.output

# ─── Input validation ─────────────────────────────────────────────────────────

if not os.path.isfile(filename):
    commands.cprint("ERROR: file does not exist", commands.Color.RED, bold=True)
    sys.exit(1)
if not os.access(filename, os.R_OK):
    commands.cprint("ERROR: file is not readable", commands.Color.RED, bold=True)
    sys.exit(1)

# ─── File-type detection ──────────────────────────────────────────────────────

if args.type:
    filetype = args.type
    commands.cprint(
        f"\n  File type  : {filetype}  (forced by user)\n",
        commands.Color.MAGENTA,
        bold=True,
    )
else:
    filetype = commands.file_type_identifier(filename)
    commands.cprint(
        f"\n  File type  : {filetype}  (auto-detected)\n",
        commands.Color.CYAN,
        bold=True,
    )

# Initialise the report with a proper header
commands.init_report(filename, filetype, forced=bool(args.type))

# ─── Universal commands ───────────────────────────────────────────────────────

commands.write_section_header("General analysis")
commands.file_command(filename)
commands.exiftool_command(filename)
commands.binwalk_command(filename)
commands.xxd_command(filename)

# ─── Type-specific commands ───────────────────────────────────────────────────

commands.write_section_header(f"Type-specific analysis — {filetype}")

if filetype == "image":
    commands.pngcheck_command(filename)
    commands.zsteg_command(filename)
    commands.steghide_command(filename)

elif filetype == "pdf":
    commands.pdfinfo_command(filename)
    commands.pdfimages_command(filename)
    commands.pdftotext_command(filename)

elif filetype == "audio":
    commands.soxi_command(filename)
    commands.steghide_command(filename)

elif filetype == "video":
    commands.ffprobe_command(filename)

elif filetype == "archive":
    commands.seven_zip_command(filename)

elif filetype == "document":
    commands.unzip_command(filename)
    commands.olevba_command(filename)
    commands.docx2txt_command(filename)
    commands.odt2txt_command(filename)

elif filetype == "image_disk":
    commands.fdisk_command(filename)
    commands.mmls_command(filename)

elif filetype == "executable":
    commands.checksec_command(filename)
    commands.nm_command(filename)
    commands.objdump_command(filename)

elif filetype == "database":
    commands.sqlite3_command(filename)

else:
    commands.cprint(
        f'\n  File type "{filetype}" is not supported.',
        commands.Color.YELLOW,
        bold=True,
    )
    commands.cprint(
        f'  Partial results saved in: {commands.report_file}\n',
        commands.Color.DIM,
    )
    sys.exit(0)

# ─── Done ─────────────────────────────────────────────────────────────────────

commands.cprint(
    f"\n✅  Analysis complete — report saved to: {commands.report_file}\n",
    commands.Color.GREEN,
    bold=True,
)
sys.exit(0)
