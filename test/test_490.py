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

    def test_determine_bitrate(self):
        # Ensure declared tbr value is respected
        self.assertEqual(125000, YoutubeDL()._determine_bitrate({'tbr': 1000}))
        # Ensure tbr is correctly calculated from constituent bitrates
        self.assertEqual(141000, YoutubeDL()._determine_bitrate({'vbr': 1000, 'abr': 128}))
        # Ensure requested_formats structure is recognized
        info_dict = {
            'requested_formats': [
                {'tbr': 1000},
                {'tbr': 128},
            ]
        }
        self.assertEqual(141000, YoutubeDL()._determine_bitrate(info_dict))
        # Ensure unrecognized data falls back to default behavior
        self.assertIsNone(
            YoutubeDL()._determine_bitrate({
                'format_id': '1',
            }),
        )

    def test_rate_limit_option_parsing(self):
        (parser, opts, urls, ydl_opts) = parse_options(['--limit-rate', 'bitrate', 'https://example.com/video'])
        self.assertEqual('bitrate', opts.ratelimit)
        self.assertEqual('bitrate', ydl_opts['ratelimit'])
