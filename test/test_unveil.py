"""Tests for unveil.

Cover the parts that don't need the ~20 external analysis tools: MIME-based
file-type detection (via libmagic), tool presence checks, the encoder registry,
report generation, and the graceful "tool not installed" path.

Run with `pytest` from the repo root. libmagic + python-magic are required
(the module is skipped otherwise); the external analysis tools are not.
"""
import os
import sys

import pytest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))

pytest.importorskip("magic")  # unveil cannot run at all without libmagic
import commands as c  # noqa: E402
import unveil  # noqa: E402

TESTFILES = os.path.join(HERE, "..", "test_files")


# ─── file-type detection ───────────────────────────────────────────────────--

DETECTION_CASES = {
    "image.png": "image",
    "image.jpeg": "image",
    "image.gif": "image",
    "image.bmp": "image",
    "pdf.pdf": "pdf",
    "audio.flac": "audio",
    "audio.wav": "audio",
    "audio.mp3": "audio",
    "challenge.mkv": "video",
    "archive.zip": "archive",
    "archive.tar": "archive",
    "archive.7z": "archive",
    "archive.rar": "archive",       # regression: x-rar must map to archive
    "database.db": "database",
    "exe": "executable",
    "doc.docx": "document",
    "doc.odt": "document",
}


@pytest.mark.parametrize("fname,expected", sorted(DETECTION_CASES.items()))
def test_file_type_detection(fname, expected):
    path = os.path.join(TESTFILES, fname)
    if not os.path.isfile(path):
        pytest.skip(f"sample {fname} missing")
    assert c.file_type_identifier(path) == expected


def test_rar_subtypes_registered():
    assert "x-rar" in c.SUPPORTED_TYPES["archive"]
    assert "vnd.rar" in c.SUPPORTED_TYPES["archive"]


def test_valid_types_match_supported():
    assert c.VALID_TYPES == list(c.SUPPORTED_TYPES.keys())
    for expected in ("image", "pdf", "audio", "video", "archive",
                     "document", "image_disk", "executable", "database"):
        assert expected in c.VALID_TYPES


# ─── tool presence ─────────────────────────────────────────────────────────--

def test_check_tool_present_and_absent():
    assert c.check_tool("sh") is True            # always on PATH
    assert c.check_tool("definitely_not_a_tool_xyz") is False


# ─── report generation ─────────────────────────────────────────────────────--

def test_report_generation(tmp_path, monkeypatch):
    report = tmp_path / "report.txt"
    monkeypatch.setattr(c, "report_file", str(report))
    c.init_report(str(tmp_path / "sample.bin"), "image", forced=False)
    c.write_section_header("General analysis")
    c.write_in_report(str(report), "some command", "some output")
    text = report.read_text()
    assert "UNVEIL" in text
    assert "GENERAL ANALYSIS" in text
    assert "some output" in text


def test_missing_tool_writes_not_installed(tmp_path, monkeypatch):
    report = tmp_path / "report.txt"
    monkeypatch.setattr(c, "report_file", str(report))
    c.init_report(str(tmp_path / "sample.bin"), "image", forced=False)
    # a tool that does not exist must be reported, not crash
    c._run_cmd(["definitely_not_a_tool_xyz", "x"], "definitely_not_a_tool_xyz x")
    assert "Not installed" in report.read_text()


# ─── dispatch ──────────────────────────────────────────────────────────────--

def test_run_type_specific_unknown_returns_false():
    assert unveil.run_type_specific("bogus_type", "whatever") is False
