import os
import shutil
import subprocess
from datetime import datetime
from types import SimpleNamespace

import magic

report_file = "unveil.txt"

# ANSI color codes
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    DIM     = "\033[2m"

def cprint(msg, color=Color.RESET, bold=False):
    prefix = Color.BOLD if bold else ""
    print(f"{prefix}{color}{msg}{Color.RESET}")

def ascii_art():
    art = r"""
$$\   $$\                               $$\ $$\
$$ |  $$ |                              \__|$$ |
$$ |  $$ |$$$$$$$\ $$\    $$\  $$$$$$\  $$\ $$ |
$$ |  $$ |$$  __$$\\$$\  $$  |$$  __$$\ $$ |$$ |
$$ |  $$ |$$ |  $$ |\$$\$$  / $$$$$$$$ |$$ |$$ |
$$ |  $$ |$$ |  $$ | \$$$  /  $$   ____|$$ |$$ |
\$$$$$$  |$$ |  $$ |  \$  /   \$$$$$$$\ $$ |$$ |
 \______/ \__|  \__|   \_/     \_______|\__|\__|
"""
    cprint(art, Color.CYAN, bold=True)


def beautiful_display(command):
    width = len(command) + 4
    top    = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"
    middle = f"║  {command}  ║"
    return f"{top}\n{middle}\n{bottom}"


def print_section(title):
    """Print a styled section header in the terminal."""
    width = 60
    bar = "─" * width
    cprint(f"\n┌{bar}┐", Color.BLUE)
    cprint(f"│  🔍 {title:<{width - 4}}│", Color.BLUE, bold=True)
    cprint(f"└{bar}┘", Color.BLUE)


def print_running(cmd_displayed):
    cprint(f"  ▶  {cmd_displayed}", Color.YELLOW)


def print_ok():
    cprint("  ✔  Done", Color.GREEN)


def print_skip(tool):
    cprint(f"  ✘  {tool} — not installed", Color.RED)


def print_result_preview(res, max_lines=5):
    """Print a short preview of a command result."""
    if not res.strip():
        cprint("  (no output)", Color.DIM)
        return
    lines = res.strip().splitlines()
    for line in lines[:max_lines]:
        cprint(f"     {line}", Color.DIM)
    if len(lines) > max_lines:
        cprint(f"     … ({len(lines) - max_lines} more lines in report)", Color.DIM)


# ─── Report helpers ───────────────────────────────────────────────────────────

def init_report(filename, filetype, forced=False):
    """Write a header block at the top of the report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    forced_note = f" (forced by user)" if forced else ""
    header = (
        "╔══════════════════════════════════════════════════════════════╗\n"
        "║                     UNVEIL — ANALYSIS REPORT                ║\n"
        "╚══════════════════════════════════════════════════════════════╝\n"
        f"\n  File     : {os.path.abspath(filename)}"
        f"\n  Date     : {now}"
        f"\n  Type     : {filetype}{forced_note}"
        f"\n  Report   : {os.path.abspath(report_file)}"
        "\n\n" + "═" * 64 + "\n"
    )
    with open(report_file, "w") as r:
        r.write(header)


def write_in_report(report, command, res):
    sep = "─" * 64
    with open(report, "a") as r:
        r.write(f"\n{command}\n\n")
        r.write(res.strip() + "\n")
        r.write(f"\n{sep}\n")


def write_section_header(title):
    """Write a section title in the report."""
    with open(report_file, "a") as r:
        r.write(f"\n\n{'═' * 64}\n")
        r.write(f"  {title.upper()}\n")
        r.write(f"{'═' * 64}\n")


# ─── Tool utilities ───────────────────────────────────────────────────────────

def check_tool(tool):
    if shutil.which(tool) is not None:
        return True
    shell = os.environ.get("SHELL", "/bin/sh")
    cmd = [shell, "-i", "-c", f"type {tool}"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
    return "not found" not in (result.stderr + result.stdout)


def safe_run(cmd):
    try:
        return subprocess.run(
            cmd, capture_output=True, text=True, check=False, timeout=25
        )
    except Exception as e:
        return SimpleNamespace(stdout="", stderr=f"ERROR while running {cmd}: {e}")


# ─── File-type identifier ─────────────────────────────────────────────────────

SUPPORTED_TYPES = {
    "image":      ["bmp", "gif", "jpeg", "png", "webp", "tiff", "x-portable-bitmap"],
    "pdf":        ["pdf"],
    "audio":      ["flac", "mpeg", "x-wav", "mp4", "ogg", "x-flac"],
    "archive":    ["x-tar", "x-7z-compressed", "vnd.rar", "zip", "gzip", "x-bzip2", "x-xz"],
    "video":      ["x-matroska", "mp4", "quicktime", "x-msvideo", "webm"],
    "document":   [
        "msword",
        "vnd.openxmlformats-officedocument.wordprocessingml.document",
        "vnd.oasis.opendocument.text",
        "vnd.ms-powerpoint",
        "vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ],
    "image_disk": ["x-raw-disk-image", "x-iso9660-image"],
    "executable": ["x-pie-executable", "x-executable", "x-sharedlib"],
    "database":   ["vnd.sqlite3", "x-sqlite3"],
}

VALID_TYPES = list(SUPPORTED_TYPES.keys())


def file_type_identifier(path):
    mime = magic.from_file(path, mime=True)
    file_subtype = mime.split("/", 1)[1]
    for category, subtypes in SUPPORTED_TYPES.items():
        if file_subtype in subtypes:
            return category
    return file_subtype


# ─── Generic command runner ───────────────────────────────────────────────────

def _run_cmd(cmd, cmd_displayed, section_title=None):
    tool = cmd[0]
    title = section_title or cmd_displayed

    print_section(title)

    if not check_tool(tool):
        print_skip(tool)
        write_in_report(report_file, beautiful_display(cmd_displayed), "Not installed")
        return

    print_running(cmd_displayed)
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    print_ok()
    print_result_preview(res)
    write_in_report(report_file, beautiful_display(cmd_displayed), res)


# ─── Individual command wrappers ──────────────────────────────────────────────

def file_command(filename):
    cmd = ["file", filename]
    _run_cmd(cmd, f"file {os.path.basename(filename)}", "File type detection")


def exiftool_command(filename):
    cmd = ["exiftool", filename]
    _run_cmd(cmd, f"exiftool {os.path.basename(filename)}", "Metadata (exiftool)")


def binwalk_command(filename):
    cmd = ["binwalk", filename]
    _run_cmd(cmd, f"binwalk {os.path.basename(filename)}", "Embedded files (binwalk)")


def xxd_command(filename):
    base = os.path.basename(filename)

    # First 208 bytes
    cmd = ["xxd", "-g", "1", "-l", "208", filename]
    cmd_displayed = f"xxd -g 1 -l 208 {base}"
    print_section("Hex dump — first 208 bytes")
    if not check_tool("xxd"):
        print_skip("xxd")
        write_in_report(report_file, beautiful_display(cmd_displayed), "Not installed")
    else:
        print_running(cmd_displayed)
        result = safe_run(cmd)
        res = result.stdout + result.stderr
        print_ok()
        print_result_preview(res)
        write_in_report(report_file, beautiful_display(cmd_displayed), res)
        with open(report_file, "a") as r:
            r.write("▲ First 208 bytes\n")

    # Last 208 bytes
    cmd2 = ["xxd", "-g", "1", "-s", "-208", filename]
    cmd_displayed2 = f"xxd -g 1 -s -208 {base}"
    print_section("Hex dump — last 208 bytes")
    if check_tool("xxd"):
        print_running(cmd_displayed2)
        result2 = safe_run(cmd2)
        res2 = result2.stdout + result2.stderr
        print_ok()
        print_result_preview(res2)
        write_in_report(report_file, beautiful_display(cmd_displayed2), res2)
        with open(report_file, "a") as r:
            r.write("▼ Last 208 bytes\n")


def pngcheck_command(filename):
    cmd = ["pngcheck", "-v", filename]
    _run_cmd(cmd, f"pngcheck -v {os.path.basename(filename)}", "PNG integrity (pngcheck)")


def zsteg_command(filename):
    cmd = ["zsteg","-a", filename]
    _run_cmd(cmd, f"zsteg -a {os.path.basename(filename)}", "LSB steganography (zsteg)")


def steghide_command(filename):
    cmd = ["steghide", "info", filename, "-p", ""]
    _run_cmd(cmd, f"steghide info {os.path.basename(filename)} -p ''", "Steganography (steghide)")


def pdfinfo_command(filename):
    cmd = ["pdfinfo", filename]
    _run_cmd(cmd, f"pdfinfo {os.path.basename(filename)}", "PDF metadata (pdfinfo)")


def pdfimages_command(filename):
    cmd = ["pdfimages", "-list", filename]
    _run_cmd(cmd, f"pdfimages -list {os.path.basename(filename)}", "PDF embedded images")


def pdftotext_command(filename):
    cmd = ["pdftotext", filename, "-"]
    _run_cmd(cmd, f"pdftotext {os.path.basename(filename)} -", "PDF text content")


def soxi_command(filename):
    cmd = ["soxi", filename]
    _run_cmd(cmd, f"soxi {os.path.basename(filename)}", "Audio info (soxi)")


def seven_zip_command(filename):
    cmd = ["7z", "l", filename]
    _run_cmd(cmd, f"7z l {os.path.basename(filename)}", "Archive listing (7z)")


def ffprobe_command(filename):
    cmd = ["ffprobe", "-hide_banner", "-show_format", filename]
    _run_cmd(cmd, f"ffprobe -hide_banner -show_format {os.path.basename(filename)}", "Video info (ffprobe)")


def olevba_command(filename):
    cmd = ["olevba", filename]
    _run_cmd(cmd, f"olevba {os.path.basename(filename)}", "Macro analysis (olevba)")


def docx2txt_command(filename):
    cmd = ["docx2txt", filename, "-"]
    _run_cmd(cmd, f"docx2txt {os.path.basename(filename)} -", "DOCX text extraction")


def odt2txt_command(filename):
    cmd = ["odt2txt", filename]
    _run_cmd(cmd, f"odt2txt {os.path.basename(filename)}", "ODT text extraction")


def unzip_command(filename):
    cmd = ["unzip", "-l", filename]
    _run_cmd(cmd, f"unzip -l {os.path.basename(filename)}", "ZIP listing (unzip)")


def fdisk_command(filename):
    cmd = ["fdisk", "-l", filename]
    _run_cmd(cmd, f"fdisk -l {os.path.basename(filename)}", "Disk partitions (fdisk)")


def mmls_command(filename):
    cmd = ["mmls", filename]
    _run_cmd(cmd, f"mmls {os.path.basename(filename)}", "Partition layout (mmls)")


def checksec_command(filename):
    cmd = ["checksec", filename]
    _run_cmd(cmd, f"checksec {os.path.basename(filename)}", "Security flags (checksec)")


def nm_command(filename):
    cmd = ["nm", filename]
    _run_cmd(cmd, f"nm {os.path.basename(filename)}", "Symbol table (nm)")


def objdump_command(filename):
    cmd = ["objdump", "-d", filename]
    _run_cmd(cmd, f"objdump -d {os.path.basename(filename)}", "Disassembly (objdump)")


def sqlite3_command(filename):
    cmd = ["sqlite3", filename, ".tables"]
    _run_cmd(cmd, f"sqlite3 {os.path.basename(filename)} .tables", "SQLite tables")
