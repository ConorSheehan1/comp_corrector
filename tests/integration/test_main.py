# TODO: rename to test_ui and setup mocking with tkinter
# for now, run all the steps that ui.py would run in main, but without errors and warnings for the user
import unittest
# TODO: stub file system?
import os
import shutil

# functions under test
from src.file_management.zip_archives import unzip, unzip_outer


class TestMain(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        unittest.TestCase.__init__(self, methodName)
        self.fixture_path = os.path.join("tests", "fixtures")
        self.example_dir = os.path.join(self.fixture_path, "example")
        self.example_zip = f"{self.example_dir}.zip"

    def tearDown(self):
        # delete non-empty example dir
        shutil.rmtree(self.example_dir, ignore_errors=True)

    def test_unzip(self):
        # example dir should not exist yet
        assert not os.path.exists(self.example_dir)
        # when names is [""], everything is extracted
        unzip_outer(self.example_zip, [""])
        assert os.path.exists(self.example_dir)

if __name__ == "__main__":
    unittest.main()