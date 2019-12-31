# TODO: rename to test_ui and setup mocking with tkinter
# for now, run all the steps that ui.py would run in main, but without errors and warnings for the user
import unittest

# TODO: stub file system?
import os
import shutil

# functions under test
from src.file_management.zip_archives import unzip, unzip_outer
from src.file_management.feedback import get_missing_names


class TestMain(unittest.TestCase):
    example_dir = os.path.join("tests", "fixtures", "example")

    def __init__(self, methodName="runTest"):
        unittest.TestCase.__init__(self, methodName)
        self.example_dir = self.__class__.example_dir
        self.example_zip = f"{self.example_dir}.zip"
        self.example_student_dir = os.path.join(
            self.example_dir, "final_fake_student_2012347", "assignment1"
        )
        self.all_names = ["fake_student", "other_fake_student", "final_fake_student"]

    @classmethod
    def tearDownClass(cls):
        # delete non-empty example dir
        shutil.rmtree(cls.example_dir, ignore_errors=True)

    # https://stackoverflow.com/a/18627017/6305204
    # nosetests runs tests in order by name
    # not ideal, but need to enforce order until testing tkinter directly, or using different UI framework.
    def test_01_unzip(self):
        # example dir should not exist yet
        assert not os.path.exists(self.example_dir)
        # when names is [""], everything is extracted
        unzip_outer(self.example_zip, [""])
        assert os.path.exists(self.example_dir)

    def test_02_unzip_inner(self):
        assert not os.path.exists(self.example_student_dir)
        unzip(self.example_dir)
        assert os.path.exists(self.example_student_dir)

    def test_03_missing_names(self):
        missing_names = get_missing_names(
            self.example_dir, self.all_names + ["missing_student"]
        )
        self.assertListEqual(["missing_student"], missing_names)


if __name__ == "__main__":
    unittest.main()
