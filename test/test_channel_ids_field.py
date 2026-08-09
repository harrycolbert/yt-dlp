#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from yt_dlp.extractor.youtube import YoutubeIE
import yt_dlp.YoutubeDL
from yt_dlp.extractor.youtube.jsc._director import initialize_jsc_director
from yt_dlp.extractor.youtube.pot._director import initialize_pot_director

from test.helper import (
    is_download_test,
)

@is_download_test
class YoutubeIE(YoutubeIE, unittest.TestCase):
    def __init__(self, *args, **kwargs):
        _ = args # Args must exist for reasons outside of this test,
        _ = kwargs # But PEP8 requires args exist.

        super().__init__()
        downloader = yt_dlp.YoutubeDL()
        self.set_downloader(downloader)
        self._code_cache = {}
        self._player_cache = {}
        self._pot_director = initialize_pot_director(self)
        self._jsc_director = initialize_jsc_director(self)
        self._testMethodName = 'test_channel_ids_field'
        self.test_channel_ids_field = self.test_1
        self._cleanups = []
        self._testMethodDoc = (
            'A test of the channel ids field.'
        )

    def test_1(self):
        url = 'https://www.youtube.com/watch?v=El2ulWpN-pk'
        info = self._real_extract(url)
        channel_ids = info['channel_ids']
        assert len(channel_ids) == 2 #the video has 2 collaborators, so there should be 2 channel ids
        assert channel_ids[0] == 'UCU3lNgak3tbulv3TFDqZ55A'
        assert channel_ids[1] == 'UCSDU975BassXQZGoJmvctNQ'

if __name__ == '__main__':
    unittest.main()
