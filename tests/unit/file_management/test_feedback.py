import unittest
from src.file_management.feedback import format_names


class TestFeedback(unittest.TestCase):
    def test_format_names(self):
        expected = ["Fake OBrien", "Boaty McBoatface", "fake_student"]
        actual = format_names("Fake O'Brien\nBoaty McBoatface\nfake_student")
        self.assertListEqual(expected, actual)