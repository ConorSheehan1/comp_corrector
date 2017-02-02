import glob
import os
import zipfile


def unzip(path, rm_zips=True):
    # iterate over sub directories of path
    for dir in glob.glob(path + "*/"):

        # unzip all files in subdirectories
        for file in glob.glob(dir + "*.zip"):
            # extract zip to path
            zipfile.ZipFile(file).extractall(dir)

            # remove zip after extraction
            if rm_zips:
                os.remove(file)


def remove_empty_folders(path):
    # iterate over sub directories
    for dir in glob.glob(path + "*"):
        # double check path is a directory and is empty
        if os.path.isdir(dir) and not os.listdir(dir):
            print("removing empty directory", dir)
            os.rmdir(dir)


def unzip_outer(zip_path, names):
    '''
    :param zip_path: path to zip file
    :param names:   list of strings
    :return:        extract any files in zipfile that start with name specified
    '''

    archive = zipfile.ZipFile(zip_path)

    for file in archive.namelist():
        # if the current file starts with any of the names in the list of names passed, extract it
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


def compile_c(path, compiler="gcc"):

    # function that actually runs commands
    def helper(helper_file):
        if helper_file.lower().endswith(".c"):
            helper_file_name = os.path.basename(helper_file)
            command = compiler + " -o " + helper_file_name.split(".")[0] + " " + helper_file_name
            print(command, "running in dir", os.getcwd())

            # will return 0 if successfully compiled, 1 if not
            return os.system(command)
        return 0

    try:
        errors = 0

        # iterate over sub directories of path
        for dir in glob.glob(path + "*/"):

            # change directory so gcc can compile files from that directory
            os.chdir(dir)

            # iterate of files in each directory
            for file in glob.glob(dir + "/*"):

                # if folder contains subfolder, and it isn't __MACOSX
                if not os.path.basename(file).startswith("_") and os.path.isdir(file):
                    # change directory so gcc can compile files from that directory
                    os.chdir(file)

                    for subfile in glob.glob(file + "/*"):
                        # compile files in subfolder
                        errors += helper(subfile)

                    # move out of subdirectory
                    os.system("cd ..")

                # compile files in main folder
                errors += helper(file)

        return errors
    except:
        return -1

if __name__ == "__main__":
    compile_c("C:/Users/conor/Documents/work/ucd_work/test/", "gcc")
