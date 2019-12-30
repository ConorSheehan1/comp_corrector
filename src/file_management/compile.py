import glob
import os
import yaml


def _compile_helper(helper_file, compiler="gcc"):
    """
    this function runs compile commands on os!
    """
    if helper_file.lower().endswith(".c"):
        helper_file_name = os.path.basename(helper_file)
        # command = compiler + " -o " + helper_file_name.split(".")[0] + " " + helper_file_name
        command = (
            f"{compiler} -o {os.path.splitext(helper_file_name)[0]} {helper_file_name}"
        )
        print("running in dir", os.getcwd())

        # will return 0 if successfully compiled, 1 if not
        return os.system(command)
    # if file doesn't end with .c, don't bother compiling, don't increment error count
    return 0


def compile_c(path, compiler="gcc"):
    """
    :param path:      path to files
    :param compiler:  name of compiler to use
    :return:          number of files which fail to compile (-1 if exception occurs)
    """

    try:
        errors = 0

        # iterate over sub directories of path
        for folder in glob.glob(path + "*/"):

            # change directory so gcc can compile files from that directory
            # handles relative imports
            os.chdir(folder)

            # iterate of files in each directory
            for sub_folder in glob.glob(folder + "/*"):

                # if folder contains subfolder, and it isn't __MACOSX
                if not os.path.basename(sub_folder).startswith("_") and os.path.isdir(
                    sub_folder
                ):
                    # change directory so gcc can compile files from that directory
                    os.chdir(sub_folder)

                    for subfile in glob.glob(sub_folder + "/*"):
                        # compile files in subfolder
                        if _compile_helper(subfile) != 0:
                            errors += 1

                    # move out of subdirectory
                    os.system("cd ..")

                # compile files in main folder
                if _compile_helper(sub_folder) != 0:
                    errors += 1

        return errors
    # TODO: add logging, log exception here and in ui.py when extracting files.
    # Hides exception compiling.
    except:
        return -1
