from documents.builder.utils import split_platforms, is_fee_item
from documents.builder.content import add_content, get_text, get_agg_totals
from documents.builder.styling import add_styling
from math import ceil
from docx.enum.section import WD_ORIENT

def full_width_content(content,structure):
    element = content.element
    type = element.type

    if ((type == "rowSubheader1")
        and (structure.full_width_subheader1)):
        return True

    elif ((type == "rowSubheader2")
        and (structure.full_width_subheader2)):
        return True

    else:
        return False

def skip_row(data_list, structure):
    '''
    Checks if the unformatted data for each row equals 0 (that is, zero value)
    If it does, and display_null_rows is false, the row will be skipped.

    int(data_list[0]) checks if the data is an integer(not a total or text) and
    aborts the function using the try/except, as these rows are always included.
    '''
    if structure.display_null_rows:
        return False
    else:
        try:
            int(data_list[0])
            if sum(data_list) == 0:
                return True
            else:
                return False
        except Exception as e:
            return False

def get_status_lengths(*args):
    '''
    Returns the number of platforms of each status type
    '''
    lengths = []
    for type in args:
        length = len(type)
        if length > 0:
            lengths.append(length)

    return lengths

def build_agg_total(table, platforms, content):
    '''
    Merges cells together so that there is only one total cell for each type

    Is disabled if content has overflowed into more than one table (landscape
    is fine).
    '''

    current, recommended, alternative = split_platforms(platforms)

    status_lengths = get_status_lengths(current, recommended, alternative)

    content_indexes = [0,1]
    merge_start = content_indexes[-1]
    row_cells = table.add_row().cells

    for i, status_length in enumerate(status_lengths):
        if status_length > 0:
            merge_end = merge_start + status_length - 1
            row_cells[merge_start].merge(row_cells[merge_end])
            merge_start = merge_end + 1
            if i != len(status_lengths) - 1:
                content_indexes.append(merge_start)

    build_agg_total_cells(table, platforms, content, row_cells, content_indexes)


def build_agg_total_cells(table, platforms, content, row_cells, content_indexes):
    '''
    Adds content and styling to agg total cells. Main point of different is
    passing the start of each merged cell to the content filler, rather
    than iterating over every cell in the row.
    '''
    display_name = content
    element = content.element

    text_list = get_agg_totals(platforms)
    try:
        for (i, location) in enumerate(content_indexes):
            active_cell = row_cells[location]
            add_content(active_cell, i, display_name, text_list, element)
            add_styling(active_cell, i, element)

    except Exception as e:
        print(e)


def set_orientation(section, prev_section, orientation):
    section.orientation = orientation
    if is_orientation_changed(section, prev_section):

        new_width, new_height = section.page_height, section.page_width
        section.page_width = new_width
        section.page_height = new_height

def is_orientation_changed(section, prev_section):

    if hasattr(prev_section, 'orientation'):
        return section.orientation != prev_section.orientation
    else:
        if "LANDSCAPE" in str(section.orientation):
            return True
        else:
            return False


def get_num_table_splits(all_platforms, structure):

    num_table_splits = ceil(len(all_platforms)/structure.portrait_overflow_limit)

    if num_table_splits > 1:
        if structure.change_orientation_if_overflow:
            num_table_splits = ceil(len(all_platforms)/structure.landscape_overflow_limit)

    return num_table_splits


def get_orientation(num_table_splits, structure):

    if num_table_splits > 1:
        if structure.change_orientation_if_overflow:
            return WD_ORIENT.LANDSCAPE

        else:
            return WD_ORIENT.PORTRAIT

    else:
        return WD_ORIENT.PORTRAIT

def split_platform_types(platform_slices):
    [platform_slices] = platform_slices
    super = [p for p in platform_slices if ((p.platform_type == "Accumulation")
                                            or (p.platform_type == "SMSF - Accumulation")
                                            or (p.platform_type == "Defined Benefit"))]

    pension = [p for p in platform_slices if ((p.platform_type == "Pension")
                                            or (p.platform_type == "SMSF - Pension"))]

    inv = [p for p in platform_slices if (p.platform_type == "Investment")]

    result = []
    for i in [super, pension, inv]:
        if i:
            result.append(i)
    return result
