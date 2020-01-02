import glob
import os
import yaml
import subprocess
from subprocess import PIPE


# TODO: refactor to stop passing compiler and capture_output around. Use class?
# TODO: add java supprt?
def _compile_cfile(
    file_path: str, cwd: str, compiler: str, capture_output: bool
) -> int:
    """
    This function runs commands on the OS.
    It tries to compile the file within cwd to handle relative imports.
    It returns the status code of the compile command.
    :param file_path:
    :param cwd: current working directory
    :compiler: name of compiler executable
    :capture_output: flag to capture output if True 
    :return: status code
    """
    # if file doesn't end with .c, don't bother compiling, don't increment error count
    if not file_path.lower().endswith(".c"):
        return 0

    file_name = os.path.basename(file_path)
    # os.system needs space between -o and filename, subprocess.run must not
    # otherwise adds space to start of file name. e.g. 'a.c' -> ' a'
    command = [compiler, f"-o{os.path.splitext(file_name)[0]}", file_name]

    # TODO: when python 3.7 works with lxml, use capture_output=True here instead of stderr=PIPE
    kwargs = {"cwd": cwd}
    if capture_output:
        kwargs["stdout"] = PIPE
        kwargs["stderr"] = PIPE

    # will return 0 if successfully compiled, 1 if not
    return subprocess.run(command, **kwargs).returncode


def _compile_all_cfiles(folder: str, compiler: str, capture_output: bool) -> int:
    """
    Compiles all .c files in folder.
    """
    errors = 0
    for c_file in glob.glob(f"{folder}/*.c"):
        # compile files in subfolder
        if _compile_cfile(c_file, folder, compiler, capture_output) != 0:
            errors += 1
    return errors


# TODO: return dict of students and files which failed to compile.
# Then add to feedback.docx.
def compile_c(path: str, compiler="gcc", capture_output=False) -> int:
    """
    For each student submission, compile their c files and count the compiler errors.
    :param path:      path to files
    :param compiler:  name of compiler to use
    :return:          number of files which fail to compile (-1 if exception occurs)
    """
    errors = 0
    for folder in glob.glob(f"{path}/*/"):
        for sub_folder in glob.glob(f"{folder}/*"):
            # if folder contains subfolder, and it doesn't start with an underscore e.g. __MACOSX
            underscore_dir = os.path.basename(sub_folder).startswith("_")
            if os.path.isdir(sub_folder) and not underscore_dir:
                errors += _compile_all_cfiles(sub_folder, compiler, capture_output)

        # compile files in main folder. some students zips do not contain a folder, just files.
        errors += _compile_all_cfiles(folder, compiler, capture_output)

    return errors
