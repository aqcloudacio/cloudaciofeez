from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.table import _Cell, Table

def is_fee_item(content):
    '''
    Returns whether the content item is the large "ongoing fee" section or not
    '''
    return content.type == 'Ongoing Fees Content' or content.type == "Adviser Fee"

def is_content_item(content):
    '''
    Returns whether the content item is an AA content item
    '''
    result = "Content" in content.type
    return result

def is_fee_table(table_type):
    '''
    Whether the table is a fee table or an AA table
    '''
    return (table_type == "Actual") or (table_type == "Consolidated")


def split_platforms(platforms):
    cur = [platform for platform in platforms if platform.status == "Current"]
    rec = [platform for platform in platforms if platform.status == "Recommended"]
    alt = [platform for platform in platforms if platform.status == "Alternative"]

    return cur,rec,alt

def sort_platforms(platforms):
    '''
    Sorts the platforms in the order current/rec/alt
    '''
    current = []
    recommended = []
    alternative = []

    current, recommended, alternative = split_platforms(platforms)

    return current + recommended + alternative

def get_platforms(platforms, structure):
    '''
    Returns the platforms to be used, depending in whether alts are to be
    included.

    Also removes platforms with no balance (platform_total).
    '''
    platforms = [p for p in platforms if p.platform_total > 0]

    if structure.display_alternative_platform:
        return sort_platforms(platforms)

    else:
        platforms = [x for x in platforms if x.status != 'Alternative']
        return sort_platforms(platforms)


def get_num_cols(platforms, structure, table_type, num_table_splits):
    '''
    Returns the number of columns. Add 1 for row header.
    '''
    if is_fee_table(table_type):
        return len(platforms) + 1



def set_cell_margins(cell: _Cell, **kwargs):
    """
    cell:  actual cell instance you want to modify

    usage:

        set_cell_margins(cell, top=50, start=50, bottom=50, end=50)

    provided values are in twentieths of a point (1/1440 of an inch).
    read more here: http://officeopenxml.com/WPtableCellMargins.php
    """
    # accesses the actual element
    tc = cell._tc
    # access the table cell properties (tcPr)
    tcPr = tc.get_or_add_tcPr()
    # print(dir(tc))
    # access the table cell margin element
    tcMar = OxmlElement('w:tcMar')

    for m in [
        "top",
        "start",
        "bottom",
        "end",
    ]:
        if m in kwargs:
            node = OxmlElement("w:{}".format(m))
            # w:top
            node.set(qn('w:w'), str(kwargs.get(m)))
            # w:w set kwargs[0]
            node.set(qn('w:type'), 'dxa')
            # w:type set 'dxa'
            tcMar.append(node)

    tcPr.append(tcMar)

############################################


def add_table_cell_margins(table: Table, **kwargs):
    """
    table:  actual table instance you want to modify

    usage:

        set_table_cell_margins(table, top=50, bottom=50, start=50, end=50)

    provided values are in twentieths of a point (1/1440 of an inch).
    """
    tblPr = table._tblPr
    tblCellMar = OxmlElement('w:tblCellMar')

    for m in [
        "top",
        "bottom",
        "start",
        "end",
    ]:
        if m in kwargs:
            node = OxmlElement("w:{}".format(m))
            # w:top
            node.set(qn('w:w'), str(kwargs.get(m)))
            # w:w set kwargs[0]
            node.set(qn('w:type'), 'dxa')
            # w:type set 'dxa'
            tblCellMar.append(node)

    tblPr.append(tblCellMar)
