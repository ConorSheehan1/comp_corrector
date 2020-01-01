# TODO: rename to test_ui and setup mocking with tkinter
# for now, run all the steps that ui.py would run in main, but without errors and warnings for the user
import unittest

# TODO: stub file system?
import os
import shutil
import re

# functions under test
from src.file_management.zip_archives import unzip, unzip_outer, setup_safe_mode
from src.file_management.feedback import get_missing_names
from src.file_management.compile import compile_c


class TestMainSafeMode(unittest.TestCase):
    cwd = os.path.join("tests", "fixtures")
    safe_cwd = os.path.join(cwd, "example")

    def __init__(self, methodName="runTest"):
        unittest.TestCase.__init__(self, methodName)
        self.safe_cwd = self.__class__.safe_cwd
        self.zip_path = os.path.join(self.cwd, "example.zip")
        self.safe_zip_path = os.path.join(self.safe_cwd, "example.zip")
        self.example_student_dir = os.path.join(
            self.safe_cwd, "final_fake_student_2012347"
        )
        self.example_student_code = os.path.join(
            self.example_student_dir, "assignment1", "assignment1.c"
        )
        self.all_names = ["fake_student", "other_fake_student", "final_fake_student"]

    @classmethod
    def tearDownClass(cls):
        # delete non-empty example dir
        shutil.rmtree(cls.safe_cwd, ignore_errors=True)

    # https://stackoverflow.com/a/18627017/6305204
    # nosetests runs tests in order by name
    # not ideal, but need to enforce order until testing tkinter directly, or using different UI framework.
    def test_01_safe_mode(self):
        # example dir should not exist yet
        assert not os.path.exists(self.safe_cwd)
        assert not os.path.exists(self.safe_zip_path)
        setup_safe_mode(self.cwd, self.zip_path)
        assert os.path.exists(self.safe_cwd)
        assert os.path.exists(self.zip_path)

    def test_02_unzip(self):
        assert not os.path.exists(self.example_student_dir)
        # when names is [""], everything is extracted
        unzip_outer(self.safe_zip_path, [""])
        assert os.path.exists(self.example_student_dir)

    def test_03_unzip_inner(self):
        assert not os.path.exists(self.example_student_code)
        unzip(self.safe_cwd)
        assert os.path.exists(self.example_student_code)

    def test_04_missing_names(self):
        missing_names = get_missing_names(
            self.safe_cwd, self.all_names + ["missing_student"]
        )
        self.assertListEqual(["missing_student"], missing_names)

    def test_05_compile(self):
        """
        compile_c should compile assignment1.c to assignment1 executable.
        it should also return the error found compiling other_fake_student_2012346/assignment1.c
        """
        # compiled_file = self.example_student_code.replace(".c", "")
        compiled_file = re.sub(r"\.c$", "", self.example_student_code)
        assert not os.path.exists(compiled_file)
        # hide output for tests
        errors = compile_c(self.safe_cwd, capture_output=True)
        assert os.path.exists(compiled_file)


if __name__ == "__main__":
    unittest.main()
