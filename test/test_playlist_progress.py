#!/usr/bin/env python3

# Allow direct execution
import io
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import yt_dlp.YoutubeDL
from contextlib import redirect_stdout

from test.helper import (
    is_download_test,
)


@is_download_test
class YoutubeDL(yt_dlp.YoutubeDL, unittest.TestCase):
    def __init__(self, *args, **kwargs):
        _ = args # Args must exist for reasons outside of this test,
        _ = kwargs # But PEP8 requires args exist.
        self.to_stdout = print
        self.processed_info_dicts = []
        self.params = {
            'logtostderror': True,
        }

        super().__init__(self.params)
        self._testMethodName = 'test_playlist_progress'
        self.test_playlist_progress = self.test_1
        self._cleanups = []
        self._testMethodDoc = (
            'A test of the console output for playlist download progress'
        )

    def test_1(self):

        with open('file', 'w') as f:
            with redirect_stdout(f):
                url = 'https://www.youtube.com/playlist?list=OLAK5uy_nVcB-bX_kuL90n0CBMlMkZf1CsTDqP_PU'

                ie = self.extract_info(url,False)

                self.process_ie_result(ie,False)

        with open("file", "r", encoding="utf-8") as f:
            output = f.read()
            pat = '\[metadata\] Extracting video [0-9]+\/[0-9]+'
            res = re.search(pat,output)
            assert res is not None

        os.remove('file')

if __name__ == '__main__':
    unittest.main()
