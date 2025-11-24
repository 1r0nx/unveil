import subprocess
import os
import sys

report_file = "report.txt"


def write_in_report(report, command, res):
    with open(report_file, "a") as r:
        r.write(f"\n-------------{command}-----------------\n\n")
        r.write(res + "\n")


def file_type_identifier(filename):
    cmd = ["file", "-b", filename]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    res = result.stdout
    with open(report_file, "a") as r:
        r.write(f"-------------file-----------------\n\n")
        r.write(res + "\n")
    if ("PC bitmap" in res) or ("GIF" in res) or ("JPEG" in res) or ("PNG" in res):
        return "image"
    if "PDF" in res:
        return "pdf"
    if (
        ("FLAC" in res)
        or ("Audio file with ID3" in res)
        or ("RIFF" in res)
        or ("WAVE" in res)
    ):
        return "audio"
    if "archive" in res:
        return "archive"
    if "Microsoft" in res:
        return "document"
    if "executable" in res:
        return "executable"
    if ("SQLite" in res) or ("database" in res):
        return "database"
    if ("ext4" in res) or ("FAT" in res) or ("DOS" in res) or ("MBR" in res):
        return "image_disk"


def exiftool_command(filename):
    cmd = ["exiftool", filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "exiftool", res)


def binwalk_command(filename):
    cmd = ["binwalk", filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "binwalk", res)


def xxd_command(filename):
    cmd = ["xxd", "-g", "1", "-l", "208", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {cmd[2]} {cmd[3]} {cmd[4]} {os.path.basename(cmd[5])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "hexdump", res)
    with open(report_file, "a") as r:
        r.write(f"First 208 bytes\n")

    cmd = ["xxd", "-g", "1", "-s", "-208", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {cmd[2]} {cmd[3]} {cmd[4]} {os.path.basename(cmd[5])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "hexdump", res)
    with open(report_file, "a") as r:
        r.write(f"Last 208 bytes\n")


def pngcheck_command(filename):
    cmd = ["pngcheck", "-v", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "pngcheck", res)


def zsteg_command(filename):
    cmd = ["zsteg", filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "zsteg", res)


def steghide_command(filename):
    cmd = ["steghide", "info", filename, "-p", ""]
    cmd_displayed = ["steghide", "info", filename, "-p", '""']
    print(
        f"\nRunning: {os.path.basename(cmd_displayed[0])} {cmd_displayed[1]} {os.path.basename(cmd_displayed[2])} {cmd_displayed[3]} {cmd_displayed[4]}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout + result.stderr
    write_in_report(report_file, "steghide", res)


def pdfinfo_command(filename):
    cmd = ["pdfinfo", filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "pdfinfo", res)


def unzip_command(filename):
    cmd = ["unzip", "-l", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "unzip", res)


def pdfimages_command(filename):
    cmd = ["pdfimages", "-list", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "pdfimages", res)


def pdftotext_command(filename):
    cmd = ["pdftotext", filename, "-"]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])} {cmd[2]}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "pdftotext", res)


def soxi_command(filename):
    cmd = ["soxi", filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "soxi", res)


def seven_zip_command(filename):
    cmd = ["7z", "l", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "7z", res)


def olevba_command(filename):
    cmd = ["olevba", filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "olevba", res)


def docx2txt_command(filename):
    cmd = ["docx2txt", filename, "-"]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])} {cmd[2]}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "docx2txt", res)


def fdisk_command(filename):
    cmd = ["fdisk", "-l", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "fdisk", res)


def mmls_command(filename):
    cmd = ["mmls", filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "mmls", res)


def checksec_command(filename):
    cmd = ["checksec", filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stderr
    write_in_report(report_file, "checksec", res)


def nm_command(filename):
    cmd = ["nm", filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "nm", res)


def objdump_command(filename):
    cmd = ["objdump", "-d", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "objdump", res)


def sqlite3_command(filename):
    cmd = ["sqlite3", filename, ".tables"]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])} {cmd[2]} \n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "sqlite3", res)
