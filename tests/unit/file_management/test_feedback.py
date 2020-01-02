import unittest
from src.file_management.feedback import format_names


class TestFeedback(unittest.TestCase):
    def test_format_names(self):
        """
        format_names should split on \n and remove ' 
        """
        expected = ["Fake Name OBrien", "Boaty McBoatface", "fake_student"]
        actual = format_names("Fake Name O'Brien\n'Boaty' McBoatface\nfake_student")
        self.assertListEqual(expected, actual)
