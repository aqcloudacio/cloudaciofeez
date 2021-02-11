import traceback
import os
from pathlib import Path
from django.conf import settings

from docx import Document
from django.shortcuts import get_object_or_404, get_list_or_404

from documents.models import Structure, Content, Style
from platforms.models import Platform
from scenarios.models import Report

from investments.models import Investment
from docx.enum.section import WD_SECTION

from documents.builder.styling import (build_element_style_set,
                                       build_table_style_set)

from documents.builder.utils import get_platforms
from documents.builder.structure import (get_num_table_splits,
                                         get_orientation,
                                         set_orientation,
                                         split_platform_types)

from documents.builder.consolidated import (get_consolidated_balance,
                                            get_consolidated_data)

from documents.builder.fees import build_fee_tables
from documents.builder.aa import get_aa, build_aa_tables
from documents.builder.product import build_product_tables
########################################


def build_document(scenario):
    '''
    id = scenario id
    '''
    try:
        theme = scenario.theme
        structure = get_object_or_404(Structure, theme=theme)
        style = get_object_or_404(Style, theme=theme)
        # all_platforms = full list of platforms. excludes alternative if selected
        all_platforms = get_platforms(get_list_or_404(Platform, scenario=scenario), structure)
        all_platforms = get_consolidated_balance(all_platforms)
        asset_allocation = get_aa(all_platforms, scenario)
        investments = get_list_or_404(Investment, platform__scenario=scenario)

        # platform_slice = reduced list after splitting
        platform_slices = [all_platforms]

        document = Document()

        # tables = ["aa", "actual", "consolidated"] IMPROT THIS FROM MODEL
        table_types = Content.TABLE_TYPE_CHOICES
        # If there are no recommended platforms, remove consolidated table.
        if not next((p for p in all_platforms if p.status == "Recommended"), False):
            table_types = [t for t in table_types if t[0] != "Consolidated"]

        # Build style sets
        build_element_style_set(document, style)
        table_style = build_table_style_set(document, style)

        #Set sections for first page
        section = document.sections[0]
        prev_section = 0

        if structure.split_platform_types:
            platform_slices = split_platform_types(platform_slices)


        for table_type in [i[0] for i in table_types]:
            content = theme.content.filter(table_type=table_type, visible=True)

            if (table_type == "AA"):

                orientation = get_orientation(0, structure)
                set_orientation(section, prev_section, orientation)

                build_aa_tables(document, style, table_style, structure, content, asset_allocation)

                prev_section = section
                section = document.add_section(WD_SECTION.NEW_PAGE)

            elif (table_type == "Consolidated") or (table_type == "Actual") or (table_type == "Product"):

                if table_type == "Consolidated":
                    all_platforms = get_consolidated_data(all_platforms)

                for platform_slice in platform_slices:
                # Want to split super/inv here and iterate on platform groupings
                    num_table_splits = get_num_table_splits(all_platforms, structure)


                    if (table_type == "Consolidated") or (table_type == "Actual"):
                        orientation = get_orientation(num_table_splits, structure)
                        set_orientation(section, prev_section, orientation)
                        build_fee_tables(all_platforms, structure, table_type, document, style,
                                     table_style, content, platform_slice, num_table_splits, orientation)

                    elif table_type == "Product":
                        orientation = get_orientation(0, structure)
                        set_orientation(section, prev_section, orientation)
                        build_product_tables(document, style, table_style, structure, content, platform_slice, investments)

                    prev_section = section
                    section = document.add_section(WD_SECTION.NEW_PAGE)

        return save_document(document, scenario)

    except Exception as e:
        print(e)
        print (traceback.format_exc())

def save_document(document, scenario):
    '''
    Builds and saves the document then returns the filepath so it can be linked
    to the report instance that called it via the pre-save signal.
    '''
    report_path = os.path.join(settings.REPORTS_PATH, str(scenario.id))

    file_path = os.path.join(settings.MEDIA_ROOT, settings.REPORTS_PATH, str(scenario.id))

    if not os.path.exists(file_path):

        Path(file_path).mkdir(parents=True, exist_ok=True)

    date = scenario.updated_at.strftime('%d-%m-%y %H.%M')
    file_name = f"ProductRex for {scenario.client} ({date}).docx"

    document.save(os.path.join(file_path, file_name))

    file = os.path.join(report_path, file_name)
    return file
