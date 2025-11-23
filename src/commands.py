import subprocess
import os
import sys

report_file = "report.txt"


def resource_path(relative_path):
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative_path)


def write_in_report(report, command, res):
    with open(report_file, "a") as r:
        r.write(f"\n-------------{command}-----------------\n\n")
        r.write(res + "\n")


def file_type_identifier(filename):
    cmd = ["file", "-b", filename]
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "file", res)
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
    exiftool_path = resource_path("bin/exiftool")
    cmd = [exiftool_path, filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "exiftool", res)


def binwalk_command(filename):
    binwalk_path = resource_path("bin/binwalk")
    cmd = [binwalk_path, filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "binwalk", res)


def xxd_command(filename):
    xxd_path = resource_path("bin/xxd")
    cmd = [xxd_path, "-g", "1", "-l", "208", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {cmd[2]} {cmd[3]} {cmd[4]} {os.path.basename(cmd[5])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "hexdump", res)
    with open(report_file, "a") as r:
        r.write(f"First 208 bytes\n")

    cmd = [xxd_path, "-g", "1", "-s", "-208", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {cmd[2]} {cmd[3]} {cmd[4]} {os.path.basename(cmd[5])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "hexdump", res)
    with open(report_file, "a") as r:
        r.write(f"Last 208 bytes\n")


def pngcheck_command(filename):
    pngcheck_path = resource_path("bin/pngcheck")
    cmd = [pngcheck_path, "-v", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "pngcheck", res)


def zsteg_command(filename):
    zsteg_path = resource_path("bin/zsteg")
    cmd = [zsteg_path, filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "zsteg", res)


def steghide_command(filename):
    steghide_path = resource_path("bin/steghide")
    cmd = [steghide_path, "info", filename, "-p", ""]
    cmd_displayed = [steghide_path, "info", filename, "-p", '""']
    print(
        f"\nRunning: {os.path.basename(cmd_displayed[0])} {cmd_displayed[1]} {os.path.basename(cmd_displayed[2])} {cmd_displayed[3]} {cmd_displayed[4]}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout + result.stderr
    write_in_report(report_file, "steghide", res)


def pdfinfo_command(filename):
    pdfinfo_path = resource_path("bin/pdfinfo")
    cmd = [pdfinfo_path, filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "pdfinfo", res)


def unzip_command(filename):
    unzip_path = resource_path("bin/unzip")
    cmd = [unzip_path, "-l", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "unzip", res)


def pdfimages_command(filename):
    pdfimages_path = resource_path("bin/pdfimages")
    cmd = [pdfimages_path, "-list", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "pdfimages", res)


def pdftotext_command(filename):
    pdftotext_path = resource_path("bin/pdftotext")
    cmd = [pdftotext_path, filename, "-"]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])} {cmd[2]}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "pdftotext", res)


def soxi_command(filename):
    soxi_path = resource_path("bin/soxi")
    cmd = [soxi_path, filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "soxi", res)


def seven_zip_command(filename):
    seven_zip_path = resource_path("bin/7z")
    cmd = [seven_zip_path, "l", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "7z", res)


def olevba_command(filename):
    olevba_path = resource_path("bin/olevba")
    cmd = [olevba_path, filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "olevba", res)


def docx2txt_command(filename):
    docx2txt_path = resource_path("bin/docx2txt")
    cmd = [docx2txt_path, filename, "-"]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])} {cmd[2]}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "docx2txt", res)


def fdisk_command(filename):
    fdisk_path = resource_path("bin/fdisk")
    cmd = [fdisk_path, "-l", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "fdisk", res)


def mmls_command(filename):
    mmls_path = resource_path("bin/mmls")
    cmd = [mmls_path, filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "mmls", res)


def checksec_command(filename):
    checksec_path = resource_path("bin/checksec")
    cmd = [checksec_path, filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stderr
    write_in_report(report_file, "checksec", res)


def nm_command(filename):
    nm_path = resource_path("bin/nm")
    cmd = [nm_path, filename]
    print(f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "nm", res)


def objdump_command(filename):
    objdump_path = resource_path("bin/objdump")
    cmd = [objdump_path, "-d", filename]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {cmd[1]} {os.path.basename(cmd[2])}\n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "objdump", res)


def sqlite3_command(filename):
    sqlite3_path = resource_path("bin/sqlite3")
    cmd = [sqlite3_path, filename, ".tables"]
    print(
        f"\nRunning: {os.path.basename(cmd[0])} {os.path.basename(cmd[1])} {cmd[2]} \n"
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    res = result.stdout
    write_in_report(report_file, "sqlite3", res)
