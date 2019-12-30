import os
import yaml
import glob
import platform
from docx import Document
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml


def _get_config():
    # return yaml.dump(yaml.load(os.path.join("..", "..", "config.yml")))
    with open("config.yml") as config:
        return yaml.load(config, Loader=yaml.FullLoader)


def _open_file(filename):
    # open file with default app
    platform_name = platform.system()
    if platform_name == "Linux":
        os.system(f"xdg-open {filename}")
    elif platform_name == "Windows":
        os.system(f"start {filename}")
    # OSX
    elif platform_name == "Darwin":
        os.system(f"open {filename}")
    else:
        print(f"Unrecognised platform {platform_name}")


contact_string = (
    f"\nIf you have any questions, please email me at {_get_config().get('email')}"
)


def format_names(names):
    names = names.split("\n")
    # remove single quotes in all names
    return list(map(lambda n: n.replace("'", ""), names))


def get_missing_names(path, names):
    """
    :param path:  path to files
    :param names: list of names
    :return:      list of any names without a corresponding file in the path
    """

    missing_list = []
    for name in names:
        # if no files in the directory start with the students name, add it to list of missing names
        if not any(
            os.path.basename(file).startswith(name) for file in glob.glob(path + "*")
        ):
            missing_list.append(name)

    return missing_list


def create_docx_feedback(path, names, missing):
    """
    :param path:    path to files
    :param names:   list of names
    :return:        None
    """

    # change to path where file should be saved
    os.chdir(path)
    filename = "feedback.docx"
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
            shading_elm = parse_xml(r'<w:shd {} w:fill="F20C0C"/>'.format(nsdecls("w")))
            row[1]._tc.get_or_add_tcPr().append(shading_elm)
        else:
            row[1].text = contact_string

    # account for file already existing
    if os.path.exists(filename):
        os.remove(filename)

    d.save(filename)
    _open_file(filename)
