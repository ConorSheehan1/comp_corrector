import glob
import os
import zipfile
from docx import Document
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
import src.secret


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


def feedback(path, names, missing):
    '''
    :param path:    path to files
    :param names:   list of names
    :return:        None
    '''

    # change to path where file should be saved
    os.chdir(path)
    filename = 'feedback.docx'
    d = Document()

    # create table to store feedback
    table = d.add_table(rows=0, cols=2, style="Table Grid")
    for name in names:
        row = table.add_row().cells
        row[0].text = name

        if name in missing:
            row[1].text = "no file submitted"
            # https://groups.google.com/forum/#!topic/python-docx/-c3OrRHA3qo
            # no api for changing color of individual cell, modify underlying xml
            shading_elm = parse_xml(r'<w:shd {} w:fill="F20C0C"/>'.format(nsdecls('w')))
            row[1]._tc.get_or_add_tcPr().append(shading_elm)
        else:
            row[1].text = "\nIf you have any questions, please email me at " + src.secret.email

    # account for file already existing
    if os.path.exists(filename):
        os.remove(filename)

    d.save(filename)
    # open file with default app
    try:
        os.system("start " + filename)
    except:
        # for osx and linux
        os.system("open " + filename)


if __name__ == "__main__":
    compile_c("C:/Users/conor/Documents/work/ucd_work/test/", "gcc")
