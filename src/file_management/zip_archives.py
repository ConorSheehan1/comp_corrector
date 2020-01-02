import os
import glob
import zipfile
import shutil
from typing import List, Tuple


def unzip(path: str, rm_zips=True) -> List[str]:
    """
    unzips all zip files submitted by students.
    :param path: path to zip file
    :param rm_zips: bool to remove zip archives once extracted
    :return errors: list of zip file names that failed to extrac 
    """
    errors = []
    for folder in glob.glob(f"{path}/*/"):
        for file_path in glob.glob(f"{folder}*.zip"):
            try:
                zipfile.ZipFile(file_path).extractall(folder)
            except:
                errors.append(os.path.basename(file_path))

            if rm_zips:
                os.remove(file_path)
    return errors


def unzip_outer(zip_path: str, names: List[str]):
    """
    unzips the main submission zip, extracting only files which start with student names passed in.
    :param zip_path: path to zip file
    :param names:    list of student names
    """

    archive = zipfile.ZipFile(zip_path)

    for file_name in archive.namelist():
        # if the current file starts with any of the names in the list of names passed, extract it
        # if names is [""], everything is extracted, because any_string.startswith("") == True
        if any(file_name.startswith(name) for name in names):
            print("extracting file", file_name)
            # extract to the folder the zipfile is in
            archive.extract(file_name, os.path.dirname(zip_path))

    archive.close()


def setup_safe_mode(cwd: str, zip_path: str) -> Tuple[str, str]:
    """
    mimics extract to folder functionality of winrar.
    creates dir with same name as zip, then moves zip to that dir before extracting contents.
    :return: tuple of new safe dir and zip path
    """
    # make dir same name as zip (remove file extension, add slash)
    safe_dirname = os.path.basename(zip_path).split(".")[0]
    safe_cwd = os.path.join(cwd, safe_dirname)
    # create safe dir if it doesn't exist
    if not os.path.exists(safe_cwd):
        os.mkdir(safe_cwd)

    safe_zip_path = os.path.join(safe_cwd, os.path.basename(zip_path))

    # copy zip into safe directory before extracting.
    shutil.copy2(zip_path, safe_zip_path)
    print("safe mode enabled", zip_path)
    return safe_cwd, safe_zip_path


# TODO: add option in UI to enable this
def remove_empty_folders(path: str):
    """
    removes empty directories left by extraction process.
    """
    for folder in glob.glob(f"{path}/*/"):
        # double check path is a directory and is empty
        if os.path.isdir(folder) and not os.listdir(folder):
            print("removing empty directory", folder)
            os.rmdir(folder)  # will fail if the dir is not empty
