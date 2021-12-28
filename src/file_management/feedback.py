# Standard Library
import glob
import os
import platform
from typing import Dict, List

# Third party
import yaml
from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def _get_config() -> Dict:
    with open("config.yml") as config:
        return yaml.load(config, Loader=yaml.FullLoader)


contact_string = f"\nIf you have any questions, please email me at {_get_config().get('email')}"


def format_names(names: str) -> List[str]:
    # remove single quotes in all names
    return [n.replace("'", "") for n in names.split("\n")]


def get_missing_names(path: str, names: str) -> List[str]:
    """
    :param path:  path to files
    :param names: list of names
    :return:      list of any names without a corresponding file in the path
    """

    file_names = [os.path.basename(file_path) for file_path in glob.glob(f"{path}/*")]
    return [
        name for name in names if not any((file_name.startswith(name) for file_name in file_names))
    ]


def create_feedback_file(
    path: str, names: List[str], missing: List[str], filename="feedback.docx"
) -> str:
    """
    :param path:        path to files
    :param names:       list of names
    :return file_path:  path to generated feedback file
    """

    # change to path where file should be saved
    file_path = os.path.join(path, filename)
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
    if os.path.exists(file_path):
        os.remove(file_path)

    d.save(file_path)
    return file_path


def open_feedback_file(filename: str):
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
