from documents.builder.utils import is_fee_table, split_platforms


def get_display_list(content, platforms):

    if content.type == 'Ongoing Fees Content':
        return platforms[0].ongoing_display_list
    elif content.type == 'Adviser Fee':
        return platforms[0].adviser_fee_list


def get_column_headers(table_type, structure):
    '''
    Returns the column header descriptions for different table types
    '''
    if is_fee_table(table_type):
        column_headers = ["Current", "Recommended", "Alternative"]
        if structure.display_alternate_platform:
            return column_headers
        else:
            column_headers.pop()
            return column_headers


def add_content(cell, i, description, text_list, element, **kwargs):
    '''
    Adds text to the given cell.
    '''
    content = kwargs.get("content")
    # print('Adding content...')
    try:
        # If it is the first column (Row header)
        if i == 0:
            # print("Adding header..")
            # Adds bullets to header rows if selected
            if element.bullet_items:
                row_header = add_bullets(str(description))
            else:
            # Adds row header text
                row_header = description
            # print(row_header)
            cell.text = str(row_header)
            # print(f'{cell.text} Header added')
        # If it is not the first column (content)
        else:
            if text_list:
                text = format_text(text_list[i-1], description, content=content)
                cell.text = str(text)
    except Exception as e:
        print("Could not add content")
        print(e)


def format_text(text, description, **kwargs):
    '''
    Attempts to convert the text to an integer to check if it a number.
    If that fails, just returns the raw text.

    If it is a number, checks if it belongs to the ongoing_fees or adviser_fees
    lists and if it does not, outputs a special format only for the balance.

    If does belong to one of those lists, outputs to 2DP.
    '''
    content = kwargs.get("content")
    try:
        val = int(text)
        if content:
            if content.table_type == "Product":
                if text < 0:
                    return '-${:,.0f}'.format(abs(text))
                else:
                    return '${:,.0f}'.format(text)
        else:
            if hasattr(description, 'type'):
                if description.type == 'Balance':
                    return '${:,.0f}'.format(text)
                else:
                    return '${:,.2f}'.format(text)
            else:
                if text < 0:
                    return '-${:,.2f}'.format(abs(text))
                else:
                    return '${:,.2f}'.format(text)
    except Exception:
        return text

def add_percentage(text, platform, description, structure, content):
    '''
    Adds a percentage to percentage fees.
    '''
    if not is_consolidated(content):
        percentage = str(round((text / platform.platform_total * 100), 2))
    else:
        print(platform.consolidated_balance)
        percentage = str(round((text / platform.consolidated_balance * 100), 2))


    if structure.percentage_position == "Right":
        percentage_str = "(" + percentage + '%)'
        text = format_text(text, description)
        text += " " + percentage_str

    elif structure.percentage_position == "Bottom":
        percentage_str = "(" + percentage + '%)'
        text = format_text(text, description)
        text += "\n" + percentage_str

    elif structure.percentage_position == "Left":
        percentage_str = percentage + '%'
        text = format_text(text, description)
        text = percentage_str + ' ' + text

    return text


def add_NA(text, description, structure):
    '''
    Adds the text "N/A" to flat fees if that toggle is True.
    '''
    if structure.percentage_position == "Right":
        text = format_text(text, description)
        text += "\t(N/A)"

    elif structure.percentage_position == "Bottom":
        text = format_text(text, description)
        text += "\n(N/A)"

    elif structure.percentage_position == "Left":
        text = format_text(text, description)
        text = 'N/A \t' + text

    return text

def is_floating_fee(property):

    return (("_calculated" in property) or
                (property == "platform_sliding_admin_fee") or
                (property == "buy_sell_spread_total") or
                (property == "platform_total_fees_ex_adviser") or
                (property == "platform_total_fees") or
                (property == "platform_investment_fee")
            )

def check_for_percentage(platforms, property, description, structure, content):
    '''
    Checks if the given data is a percentage, or the "display NA" field is
    True. If it is, passes that data for formatting.

    Returns data_list as well, which is an unformatted list of the original
    data to be used to skip rows.
    '''
    text_list = []
    data_list = []
    try:
        # Iterate each platform in the scenario
        for platform in platforms:
            # If it's a regular fee table, get the prop value so it can be
            # added to the text_list
            if not is_consolidated(content):
                text = getattr(platform, property)
            # If it's a consolidated fee table, perform some modifications to
            # the prop values.
            else:
                # Multiply the fee by the platform factor (the % of the
                # scenario value of the platform value)
                if is_floating_fee(property):
                    text = getattr(platform, property) * platform.factor
                elif property == "platform_sliding_admin_fee":
                    text = platform.platform_sliding_admin_fee_consolidated
                else:
                    text = getattr(platform, property)
            data = text

            if is_floating_fee(property):
                text = add_percentage(text, platform, description, structure, content)

            elif structure.display_NA_flat_fees:
                text = add_NA(text, description, structure)

            text_list.append(text)
            data_list.append(data)

        return text_list, data_list
    except Exception as e:
        print(e)


def get_status_fees(current, recommended, alternative):

    cur_val = sum([x.platform_total_fees for x in current])
    rec_val = sum([x.platform_total_fees for x in recommended])
    alt_val = sum([x.platform_total_fees for x in alternative])
    return [cur_val, rec_val, alt_val]


def get_agg_totals(platforms):
    '''
    Returns the total fees for each type of platform.
    '''
    current, recommended, alternative = split_platforms(platforms)
    fee_totals = get_status_fees(current, recommended, alternative)

    return fee_totals

def is_consolidated(content):
    '''
    Tests if the table is a consolidated fee table
    '''
    return content.table_type == "Consolidated"


def get_text(platforms, description, is_fee_item, content, structure, all_platforms):
    '''
    Returns a text_list to be inserted into each cell in the row.

    Also Returns data_list, a list of the unformatted original data.
    '''
    data_list = []
    text_list = []
    # If the item is a fee_item, use the check_for_percentage fn to get the
    # text list
    print(description)
    if is_fee_item:
        property = 'platform_' + description
        text_list, data_list = check_for_percentage(platforms, property, description, structure, content)

    else:
        if description == 'Status':
            text_list = [platform.status for platform in platforms]
        if description == 'Product':
            text_list = [platform for platform in platforms]

        if description == 'Balance':

            if is_consolidated(content):
                text_list = [platform.consolidated_balance for platform in platforms]
            else:
                text_list = [platform.platform_total for platform in platforms]

        if description == 'Investments':
            text_list = [platform.platform_investments_string for platform in platforms]

        if description == 'Switch Fees':
            property = "switch_fees_total"
            text_list, data_list = check_for_percentage(platforms, property, description, structure, content)

        if description == 'Buy/Sell Fees':
            property = "buy_sell_spread_total"
            text_list, data_list = check_for_percentage(platforms, property, description, structure, content)
            print(text_list)
            print(data_list)

        if description == 'One-off Subtotal':
            text_list = get_one_off_subtotal(content, platforms)

        if description == 'Subtotal':
            if structure.display_percentage_subtotal:
                property = "platform_total_fees_ex_adviser"
                text_list, data_list = check_for_percentage(platforms, property, description, structure, content)
            else:
                text_list = [(platform.platform_total_fees_ex_adviser) for platform in platforms]

        if description == 'Total':
            if structure.display_percentage_total:
                property = "platform_total_fees"
                text_list, data_list = check_for_percentage(platforms, property, description, structure, content)
            else:
                text_list = [platform.platform_total_fees for platform in platforms]

        if description == 'Aggregated Total':
            text_list = get_agg_totals(platforms)

    if not data_list:
        data_list = text_list

    return text_list, data_list

def get_one_off_subtotal(content, platforms):
    '''
    Finds whether the style has buy/sell or switch fees visible.
    Then gets one or both of them from platforms, sums them, and returns the
    total
    '''
    theme = content.theme
    all_content = theme.content.all()
    visible_content = [c for c in all_content if c.visible is True]

    subtotal_items = []
    result = []
    for content in visible_content:
        if content.type == "Switch Fees":
            subtotal_items.append("switch_fees_total")
        elif content.type == "Buy/Sell Fees":
            subtotal_items.append("buy_sell_spread_total")

    for platform in platforms:
        subtotal = 0
        for item in subtotal_items:
            subtotal += getattr(platform, item)
        result.append(subtotal)

    return result


def add_bullets(content):
    '''
    Adds a hyphen as bullet to the text string for the given row header.
    '''
    return " - "+content
