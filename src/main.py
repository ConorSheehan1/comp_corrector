import glob
import os
import shutil
import zipfile


def rename(path, rm_dirs=False, rm_zips=False):
    if os.path.isdir(path):
        print(path)

        # replace backslash with forward slash so all paths are the same for windows, osx, linux
        path = path.replace("\\", "/")

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

    else:
        raise ValueError("The path specified was empty or not a directory")


def remove_empty_folders(path):
    # iterate over sub directories
    for dir in glob.glob(path + "*"):
        # double check path is subdirectory and empty
        if os.path.isdir(dir) and not os.listdir(dir):
            print("removing empty directory", dir)
            os.rmdir(dir)


def unzip(path, rm=False):
    '''
    Input: path where dir with zips, rm=True to delete zips after extraction
    Output: contents of zip file in path specified
    '''

    for file in glob.glob(path + "*.zip"):
        # extract zip to path
        zipfile.ZipFile(file).extractall(path)

        if rm:
            # remove zip after extraction
            os.remove(file)


if __name__ == "__main__":
    bools = {"True":True, "False":False}
    rm_dirs = input("Remove empty directories after moving files? True/False")
    while rm_dirs not in bools:
        rm_dirs = input("Please choose 'True' or 'False'. Remove empty directories after moving files?")

    rm_zips = input("Remove zips after extraction? True/False")
    while rm_zips not in bools:
        rm_dirs = input("Please choose 'True' or 'False'. zips after extraction?")

    user_dir = input("Choose a directory")
    while not os.path.isdir(user_dir):
        user_dir = input("Chosen path must be a directory, try again")

    print(user_dir, rm_dirs, rm_zips)

    # rename("C:/Users/conor/Documents/GitHub/CompCorrector/outer/test/", bools[rm_dirs], bools[rm_zips])