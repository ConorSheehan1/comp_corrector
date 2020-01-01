import os
import glob
import zipfile
import shutil


def unzip(path, rm_zips=True):
    """
    :param path: path to zip file
    :param rm_zips: bool to remove zip archives once extracted
    """
    errors = []
    # iterate over sub directories of path
    for folder in glob.glob(f"{path}/*/"):
        # unzip all files in subdirectories
        for file_path in glob.glob(f"{folder}*.zip"):
            # extract zip to path
            try:
                zipfile.ZipFile(file_path).extractall(folder)
            except:
                errors.append(os.path.basename(file_path))

            # remove zip after extraction
            if rm_zips:
                os.remove(file_path)
    return errors


def unzip_outer(zip_path, names):
    """
    :param zip_path: path to zip file
    :param names:   list of strings
    :return:        extract any files in zipfile that start with name specified
    """

    archive = zipfile.ZipFile(zip_path)

    for file_name in archive.namelist():
        # if the current file starts with any of the names in the list of names passed, extract it
        # if names is [""], everything is extracted, because any_string.startswith("") == True
        if any(file_name.startswith(name) for name in names):
            print("extracting file", file_name)
            # extract file to folder the zipfile is currently in
            archive.extract(file_name, os.path.dirname(zip_path))

    archive.close()


def setup_safe_mode(cwd, zip_path):
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


def remove_empty_folders(path):
    # iterate over sub directories
    for folder in glob.glob(f"{path}/*/"):
        # double check path is a directory and is empty
        if os.path.isdir(folder) and not os.listdir(folder):
            print("removing empty directory", folder)
            os.rmdir(folder)  # will fail if the dir is not empty
