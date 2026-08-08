import unittest
from collections import namedtuple
from yt_dlp import YoutubeDL, parse_options


class Test_490(unittest.TestCase):
    def test_merge_specification(self):
        """Ensure --no-merge flag prevents merging, but merging functions properly otherwise."""
        # Setup mock data
        MergerMock = namedtuple("MergerMock", "available")
        merger_mock = MergerMock(True)
        downloaded = ['file_name_example']
        files_to_move = {'file_name_example': True}
        # Test Merging
        info_dict = {"__postprocessors": []}
        parsed_options = parse_options([])
        self.assertFalse(parsed_options.ydl_opts.get('no_merge'))
        YoutubeDL.setup_merge(True, info_dict, files_to_move, downloaded, merger_mock, False)
        assert(merger_mock in info_dict.get("__postprocessors"))
        assert(info_dict.get("__files_to_merge") == downloaded)
        assert(True == info_dict.get("__real_download"))
        assert(files_to_move.get('file_name_example') == True)
        # Test No Merging
        info_dict = {"__postprocessors": []}
        parsed_options = parse_options(['--no-merge'])
        self.assertTrue(parsed_options.ydl_opts.get('no_merge'))
        YoutubeDL.setup_merge(False, info_dict, files_to_move, downloaded, merger_mock, False)
        assert(merger_mock not in info_dict.get("__postprocessors"))
        assert(info_dict.get("__files_to_merge", None) is None)
        assert(info_dict.get("__real_download", None) is None)
        assert(files_to_move.get('file_name_example', True) is None)
