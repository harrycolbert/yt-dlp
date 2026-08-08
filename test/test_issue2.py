#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import yt_dlp.YoutubeDL
import time
from yt_dlp.utils._utils import ReExtractInfo

from test.helper import (
    is_download_test,
)

def test_playlist_uses_short_metadata_output(capsys):
    ydl = yt_dlp.YoutubeDL({
        "quiet": False,
    })


    current_video = 1
    total_videos = 10

    ydl.to_stderr(
        f"[metadata] Extracting video "
        f"{current_video}/{total_videos}"
    )

    captured = capsys.readouterr()

    assert "[metadata] Extracting video 1/10" in captured.err
