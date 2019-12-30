import os
from docx import Document
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml


def _get_config():
    return yaml.load(os.path.join('..', '..', 'config.yml'))


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
            row[1].text = f"\nIf you have any questions, please email me at {get_config.get('email')}"

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
