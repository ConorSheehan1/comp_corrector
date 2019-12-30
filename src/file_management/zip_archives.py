import glob
import zipfile


def unzip(path, rm_zips=True):
    """
    :param path: path to zip file
    :param rm_zips: bool to remove zip archives once extracted
    """
    errors = []
    # iterate over sub directories of path
    for dir in glob.glob(path + "*/"):

        # unzip all files in subdirectories
        for file in glob.glob(dir + "*.zip"):
            # extract zip to path
            try:
                zipfile.ZipFile(file).extractall(dir)
            except:
                errors.append(os.path.basename(file))

            # remove zip after extraction
            if rm_zips:
                os.remove(file)
    return errors


def unzip_outer(zip_path, names):
    """
    :param zip_path: path to zip file
    :param names:   list of strings
    :return:        extract any files in zipfile that start with name specified
    """

    archive = zipfile.ZipFile(zip_path)

    for file in archive.namelist():
        # if the current file starts with any of the names in the list of names passed, extract it
        if any(file.startswith(name) for name in names):
            print("extracting file", file)
            # extract file to folder the zipfile is currently in
            archive.extract(file, os.path.dirname(zip_path))

    archive.close()


def remove_empty_folders(path):
    # iterate over sub directories
    for dir in glob.glob(path + "*"):
        # double check path is a directory and is empty
        if os.path.isdir(dir) and not os.listdir(dir):
            print("removing empty directory", dir)
            os.rmdir(dir)
