import glob
import os
import shutil
import zipfile


def rename(path, rm_dirs=False, rm_zips=False):
    '''

    :param path:    path to directory containing folders which contain either files or zips
    :param rm_dirs: boolean to remove empty directories
    :param rm_zips: boolean to remove zips after extraction
    :return:        files renamed dirname_filename in path specified
    '''

    print(path)

    # replace backslash with forward slash so all paths are the same for windows, osx, linux
    # path = path.replace("\\", "/")

    # iterate over sub directories
    for dir in glob.glob(path + "*/"):

        # unzip all files in subdirectories
        unzip(dir, rm_zips)

        # get name of directory
        # replace backslash with forward slash so all paths are the same for windows, osx, linux
        dir_name = dir.replace("\\", "/").split("/")[-2]

        # iterate over every file in sub directory
        for file in glob.glob(dir + "*"):
            # get name of file
            file_name = os.path.basename(file)

            # move file to outer path and rename file with prefix (dir_name_file_name)
            print("moving", path + dir_name + "_" + file_name)
            shutil.move(file, path + dir_name + "_" + file_name)

    if rm_dirs:
        remove_empty_folders(path)


def remove_empty_folders(path):
    # iterate over sub directories
    for dir in glob.glob(path + "*"):
        # double check path is subdirectory and empty
        if os.path.isdir(dir) and not os.listdir(dir):
            print("removing empty directory", dir)
            os.rmdir(dir)


def unzip(path, rm=False):
    '''
    :param path: path to zipfile
    :param rm:   boolean to remove zip after extraction
    :return:    unzipped files
    '''

    for file in glob.glob(path + "*.zip"):
        # extract zip to path
        zipfile.ZipFile(file).extractall(path)

        if rm:
            # remove zip after extraction
            os.remove(file)


def unzip_outer(zip_path, names):
    '''
    :param zip_path: path to zip file
    :param names:   list of strings
    :return:        extract any files in zipfile that start with name in names
    '''

    archive = zipfile.ZipFile(zip_path)

    for file in archive.namelist():
        if any(file.startswith(name)for name in names):
            print("extracting file", file)
            # extract file to folder the zipfile is currently in
            archive.extract(file, os.path.dirname(zip_path))


def missing_names(path, names):
    '''
    :param path:  path to files
    :param names: list of names
    :return:      string of list of any names without a corresponding file in the path
    '''
    print("path", path)
    print("files in path", [os.path.basename(file) for file in glob.glob(path + "*")])
    # for name in names:
    #     if any(os.path.basename(file).startswith(name) for file in glob.glob(path + "*")):
    #         names.remove(name)

    for file in glob.glob(path + "*"):
        for name in names:
            if os.path.basename(file).startswith(name):
                try:
                    names.remove(name)
                except:
                    continue

    for file in glob.glob(path + "*"):
        for name in names:
            if os.path.basename(file).startswith(name):
                print("whyy??", file)

    return names

if __name__ == "__main__":
    bools = {"True": True, "False": False}

    unzip_outer("C:/Users/conor/Documents/work/test/test/COMP 10280-Practical 2, Thursday, 22 September 2016--35506.zip", input())

    # rm_dirs = input("Remove empty directories after moving files? True/False")
    # while rm_dirs not in bools:
    #     rm_dirs = input("Please choose 'True' or 'False'. Remove empty directories after moving files?")
    #
    # rm_zips = input("Remove zips after extraction? True/False")
    # while rm_zips not in bools:
    #     rm_dirs = input("Please choose 'True' or 'False'. zips after extraction?")
    #
    # user_dir = input("Choose a directory")
    # while not os.path.isdir(user_dir):
    #     user_dir = input("Chosen path must be a directory, try again")
    #
    #
    # # if rm_dirs are not empty they evaluate to true
    # print(user_dir, bools[rm_dirs], bools[rm_zips])

    # rename("C:/Users/conor/Documents/GitHub/CompCorrector/outer/test/", bools[rm_dirs], bools[rm_zips])