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

@is_download_test
class YoutubeDL(yt_dlp.YoutubeDL,unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.to_stderr = self.to_screen
        self.processed_info_dicts = []
        self.params = {
            'offset': 5, #since this is 5 seconds before the timestamp, which we've set to 10 seconds, it should throw the ReExtractInfo exception 5 seconds after the test starts
            'wait_for_video': (1,100),
            'logtostderror': False,
        }

        super().__init__(self.params)
        self._testMethodName = 'test_wait_offset'
        self.test_wait_offset = self.test_1
        self._cleanups = []
        self._testMethodDoc = 'A test of the offset feature with the --wait-for-video option'

    def test_1(self):
        ie_result = _make_result()

        start_time = time.time()


        try:
            self._wait_for_video(ie_result)
        except ReExtractInfo:
            end_time = time.time()
            elapsed = end_time - start_time
            
            assert round(elapsed) == 5
            return

        assert False

def _make_result():
    res = {
        'id': 'testid',
        '_type': 'video',
        'live_status': 'is_upcoming',
        'title': 'testttitle',
        'extractor': 'testex',
        'extractor_key': 'TestEx',
        'release_timestamp': time.time() + 10,
    }
    return res

if __name__ == '__main__':
    unittest.main()