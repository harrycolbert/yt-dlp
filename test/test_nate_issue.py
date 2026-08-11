#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import unittest
from urllib.parse import urlparse, parse_qs
from yt_dlp.extractor.youtube._video import YoutubeIE
import subprocess
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import yt_dlp.YoutubeDL
import time
from yt_dlp.utils._utils import ReExtractInfo
from test.helper import (
    is_download_test,
)
 
class YoutubeDL(yt_dlp.YoutubeDL, unittest.TestCase):
    def __init__(self, *args, **kwargs):
        _ = args # Args must exist for reasons outside of this test,
        _ = kwargs # But PEP8 requires args exist.
        self.to_stderr = self.to_screen
        self.processed_info_dicts = []
        # Note: since this is 5 seconds before the timestamp, which we've set to 10 seconds,
        # it should throw the ReExtractInfo exception 5 seconds after the test starts
        self.params = {
            'filesize': 1,  # See note above
            'logtostderror': False,
        }

        super().__init__(self.params)
        self._testMethodName = 'test_nate_issue'
        self.test_nate_issue = self.test_1
        self._cleanups = []
        self._testMethodDoc = (
            'A test of the comments feature with the --write-comment option'
        )

def test_save_comments_immediately(tmp_path):
    TEST_URL = "https://www.youtube.com/watch?v=X3oDvz4YauE"

    video_id = parse_qs(urlparse(TEST_URL).query)["v"][0]
    filename = tmp_path / f"{video_id}.comments.jsonl"
    repo_root = Path(__file__).resolve().parents[1]
    print(repo_root)


    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "yt_dlp",
            "--write-comments",

            TEST_URL,
        ],
        cwd=tmp_path,
        env=env,
    )

    time.sleep(5)
    process.terminate()

    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()

    assert filename.exists()
    assert filename.stat().st_size > 0

if __name__ == '__main__':
    unittest.main()
