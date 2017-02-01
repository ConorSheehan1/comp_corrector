import glob
import os
import shutil
import zipfile


def rename(path, rm_dirs=True, rm_zips=True):
    '''

    :param path:    path to directory containing folders which contain either files or zips
    :param rm_dirs: boolean to remove empty directories
    :param rm_zips: boolean to remove zips after extraction
    :return:        files renamed dirname_filename in path specified
    '''

    print("renaming files in path:", path)

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
        # double check path is a directory and is empty
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
    :return:        extract any files in zipfile that start with name specified
    '''

    archive = zipfile.ZipFile(zip_path)

    for file in archive.namelist():
        if any(file.startswith(name) for name in names):
            print("extracting file", file)
            # extract file to folder the zipfile is currently in
            archive.extract(file, os.path.dirname(zip_path))


def missing_names(path, names):
    '''
    :param path:  path to files
    :param names: list of names
    :return:      string of list of any names without a corresponding file in the path
    '''

    for file in glob.glob(path + "*"):
        for name in names:
            if os.path.basename(file).startswith(name):
                try:
                    names.remove(name)
                # if name has already been removed from list, continue with loop
                except:
                    continue

    return names


def compile_c(path, compiler):
    try:
        errors = 0
        # iterate over sub directories of path
        for dir in glob.glob(path + "*/"):

            # change directory so gcc can compile files from that directory
            os.chdir(dir)

            # iterate of files in each directory
            for file in glob.glob(dir + "*"):

                # option to choose file ending?
                if file.lower().endswith(".c"):
                    file_name = os.path.basename(file)
                    print("compiling", file_name, "at", os.getcwd())
                    command = compiler + " -o " + file_name.split(".")[0] + " " + file_name
                    print(command)

                    # if there's an error running the command, return false
                    if os.system(command) == 1:
                        errors += 1
        return errors
    except:
        return -1

if __name__ == "__main__":
    compile_c("C:/Users/conor/Documents/work/ucd_work/test/", "gcc")
