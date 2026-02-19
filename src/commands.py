import os
import shutil
import subprocess
from types import SimpleNamespace

import magic

report_file = "unveil.txt"


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
    print(art)


def beatiful_display(command):
    width = len(command) + 4

    # Border
    top = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"
    middle = f"║  {command}  ║"

    # Display
    return f"{top}\n{middle}\n{bottom}"


# Check if the commands is installed
def check_tool(tool):
    if shutil.which(tool) is None:
        cmd = ["type", tool]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
        result = result.stderr + result.stdout
        if "not found" in result:
            return False
        else:
            return True
    return True


# Run the command as safe as possible
def safe_run(cmd):
    try:
        return subprocess.run(
            cmd, capture_output=True, text=True, check=False, timeout=25
        )
    except FileNotFoundError:
        return SimpleNamespace(stdout="", stderr=f"ERROR: command not found: {cmd[0]}")
    except Exception as e:
        return SimpleNamespace(stdout="", stderr=f"ERROR while running {cmd}: {e}")


# The function to write in the report file
def write_in_report(report, command, res):
    with open(report_file, "a") as r:
        r.write(f"\n{command}\n\n")
        r.write(res + "\n")


# The function to retrive the filetype
def file_type_identifier(path):
    mime = magic.from_file(path, mime=True)
    file_type = mime.split("/", 1)[1]

    if file_type in ["bmp", "gif", "jpeg", "png"]:
        return "image"
    elif file_type in ["pdf"]:
        return "pdf"
    elif file_type in ["flac", "mpeg", "x-wav"]:
        return "audio"
    elif file_type in ["x-tar", "x-7z-compressed", "vnd.rar", "zip"]:
        return "archive"
    elif file_type in [
        "msword",
        "vnd.openxmlformats-officedocument.wordprocessingml.document",
        "vnd.oasis.opendocument.text",
        "vnd.ms-powerpoint",
        "vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]:
        return "document"
    elif file_type in ["x-raw-disk-image", "x-iso9660-image"]:
        return "image_disk"
    elif file_type in ["x-pie-executable"]:
        return "executable"
    elif file_type in ["vnd.sqlite3"]:
        return "database"
    else:
        return file_type


def file_command(filename):
    cmd = ["file", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def exiftool_command(filename):
    cmd = ["exiftool", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def binwalk_command(filename):
    cmd = ["binwalk", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed}\n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def xxd_command(filename):
    cmd = ["xxd", "-g", "1", "-l", "208", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {cmd[1]} {cmd[2]} {cmd[3]} {cmd[4]} {os.path.basename(cmd[5])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed}\n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)
    with open(report_file, "a") as r:
        r.write("First 208 bytes\n")

    cmd = ["xxd", "-g", "1", "-s", "-208", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {cmd[1]} {cmd[2]} {cmd[3]} {cmd[4]} {os.path.basename(cmd[5])}"
    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)
    with open(report_file, "a") as r:
        r.write("Last 208 bytes\n")


def pngcheck_command(filename):
    cmd = ["pngcheck", "-v", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def zsteg_command(filename):
    cmd = ["zsteg", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def steghide_command(filename):
    cmd = ["steghide", "info", filename, "-p", ""]
    cmd_displayed = f"{os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])} {cmd[3]} '{cmd[4]}'"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed}\n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def pdfinfo_command(filename):
    cmd = ["pdfinfo", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def unzip_command(filename):
    cmd = ["unzip", "-l", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def pdfimages_command(filename):
    cmd = ["pdfimages", "-list", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def pdftotext_command(filename):
    cmd = ["pdftotext", filename, "-"]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])} {cmd[2]}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed}\n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def soxi_command(filename):
    cmd = ["soxi", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def seven_zip_command(filename):
    cmd = ["7z", "l", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def olevba_command(filename):
    cmd = ["olevba", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed}\n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def docx2txt_command(filename):
    cmd = ["docx2txt", filename, "-"]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])} {cmd[2]}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def odt2txt_command(filename):
    cmd = ["odt2txt", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def fdisk_command(filename):
    cmd = ["fdisk", "-l", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed}\n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def mmls_command(filename):
    cmd = ["mmls", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def checksec_command(filename):
    cmd = ["checksec", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed}\n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def nm_command(filename):
    cmd = ["nm", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])}"
    print(f"\nRunning: {cmd_displayed} \n")

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def objdump_command(filename):
    cmd = ["objdump", "-d", filename]
    cmd_displayed = f"{os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}"
    print(f"\nRunning: {cmd_displayed} \n")

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)


def sqlite3_command(filename):
    cmd = ["sqlite3", filename, ".tables"]
    cmd_displayed = f"{os.path.basename(cmd[0])} {os.path.basename(cmd[1])} {cmd[2]}"

    if not check_tool(cmd[0]):
        write_in_report(report_file, beatiful_display(cmd[0]), "Not installed")
        return

    print(f"\nRunning: {cmd_displayed} \n")
    result = safe_run(cmd)
    res = result.stdout + result.stderr
    write_in_report(report_file, beatiful_display(cmd_displayed), res)
