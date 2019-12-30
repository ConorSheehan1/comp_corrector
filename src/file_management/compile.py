import glob
import os
import yaml

def get_config():
    return yaml.load(os.path.join('..', '..', 'config.yml'))


def missing_names(path, names):
    '''
    :param path:  path to files
    :param names: list of names
    :return:      list of any names without a corresponding file in the path
    '''

    missing_list = []
    for name in names:
        # if no files in the directory start with the students name, add it to list of missing names
        if not any(os.path.basename(file).startswith(name) for file in glob.glob(path + "*")):
            missing_list.append(name)

    return missing_list


def compile_c(path, compiler="gcc"):
    '''
    :param path:      path to files
    :param compiler:  name of compiler to use
    :return:          number of files which fail to compile (-1 if exception occurs)
    '''

    # function that runs commands on os!
    def helper(helper_file):
        if helper_file.lower().endswith(".c"):
            helper_file_name = os.path.basename(helper_file)
            command = compiler + " -o " + helper_file_name.split(".")[0] + " " + helper_file_name
            print("running in dir", os.getcwd())

            # will return 0 if successfully compiled, 1 if not
            return os.system(command)
        # if file doesn't end with .c, don't bother compiling, don't increment error count
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

