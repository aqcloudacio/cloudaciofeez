import scrapy
import re
import camelot
import logging
import fitz
import requests
import os

from distutils.util import strtobool
from requests.exceptions import MissingSchema, SSLError
from urllib.parse import urlparse, urljoin, quote
from pathlib import Path
from django.utils.text import slugify

from furl import furl
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
from scrapes.models import InvestmentScrape

excluded_keys = [
    'platformname',
    'inv_id',
    'invname',
    'type',
    '',
    'settings',
]

def get_data(instance):
    '''
    Gets the scrape data from the models.

    Allows for two command line mods
    -a single_scrape_id=123 (only the the investment scrape with this id)
    -a single_scrape_group_id=123 (only the group of scrapes with this settings id)
    '''

    if getattr(instance, 'single_scrape_id',''):
        #if you want to scape a single record
        scrape_data = InvestmentScrape.objects.filter(id=instance.single_scrape_id)
    elif getattr(instance, 'single_scrape_group_id',''):
        #if you want to scape a single record
        scrape_data = InvestmentScrape.objects.filter(settings__id=instance.single_scrape_group_id)
    else:
        scrape_data = InvestmentScrape.objects.all()

    return scrape_data


def get_url(scrape, name):
    '''
    Gets the url for each scrape, based off the root scrape in the settings
    '''
    root = str(getattr(scrape.settings, name+"_root"))
    path = ''

    if getattr(scrape, name+"_path"):
        # If there is a path hard coded for the investment scrape instance.
        path = getattr(scrape, name+"_path")

    elif getattr(scrape.settings, name+"_slugify_path",''):
        # If there is no path hard coded, infer the path based on the name.
        path = "/"+slugify(str(scrape.name.name))
        if getattr(scrape.settings, name+"_slugify_path_no_hyphens"):
            path = path.replace("-","")
    else:
        # If no joining required and data comes from the root url
        pass

    url = root+path

    return url


def get_xpath_data(scrape, spider_name):
    '''
    Collects xpath expressions from the model.
    Could be dynamically built when refactored.
    '''

    if spider_name == 'aa':
        return {
            'url': scrape.settings.xpath_aa_url,
            'root': scrape.settings.xpath_aa_root,
            'node': scrape.settings.xpath_aa_node,
            'inv_name_path': scrape.settings.xpath_aa_inv_name_path,
            'name_path': scrape.settings.xpath_aa_name_path,
            'data_path': scrape.settings.xpath_aa_allocation_path,
        }
    elif spider_name == 'fee':
        return {
            'url': scrape.settings.xpath_fee_url,
            'root': scrape.settings.xpath_fee_root,
            'inv_name_path': '',
            'node': scrape.settings.xpath_fee_node,
            'name_path': scrape.settings.xpath_fee_name_path,
            'data_path': scrape.settings.xpath_fee_path,
        }

    elif spider_name == 'bs':
        return {
            'url': scrape.settings.xpath_bs_url,
            'root': scrape.settings.xpath_bs_root,
            'node': scrape.settings.xpath_bs_node,
            'name_path': scrape.settings.xpath_bs_name_path,
            'buy_spread_data_path': scrape.settings.xpath_bs_buy_spread_path,
            'sell_spread_data_path': scrape.settings.xpath_bs_sell_spread_path,

        }

def get_directions(scrape, spider_name):
    '''
    Gets the "directions" for each scrape. This is how the scrape will be
    treated once data is collected.
    '''
    strings_to_remove = scrape.settings.strings_to_remove
    if strings_to_remove:
        strings_to_remove = strings_to_remove.split(',')
    else:
        strings_to_remove = []

    directions = {
        'strings_to_remove': strings_to_remove,
        'capitalise_names': scrape.settings.capitalise_names
    }

    if spider_name == 'aa':
        subdict = {
            'split_inv_name_string': scrape.settings.aa_split_inv_name_string,
            'split_name_string': scrape.settings.aa_split_name_string,
            'excise_name_string': scrape.settings.aa_excise_name_string,
            'excise_inv_name_string': scrape.settings.aa_excise_inv_name_string,
            'use_percentage_regex': scrape.settings.aa_use_percentage_regex,
        }

    elif spider_name == 'fee':
        subdict = {
            'split_inv_name_string': '',
            'split_name_string': scrape.settings.fee_split_name_string,
            'excise_name_string': scrape.settings.fee_excise_name_string,
            'excise_inv_name_string': '',
            'use_percentage_regex': scrape.settings.fee_use_percentage_regex,
        }

    elif spider_name == 'bs':
        subdict = {
            'split_inv_name_string': '',
            'split_name_string': scrape.settings.bs_split_name_string,
            'excise_name_string': scrape.settings.bs_excise_name_string,
            'excise_inv_name_string': '',
            'use_percentage_regex': scrape.settings.bs_use_regex_percentage,
        }

    directions = {**directions, **subdict}

    return directions


def get_meta(scrape, spider_name, instance):
    '''
    Builds a packet of metadata for each scrape, so it can be used throughout
    the scrape rather than calling from the DB every time is needs to be used.
    '''
    meta = {}

    meta['settings'] = scrape.settings
    meta['name'] = spider_name
    meta['url'] = get_url(scrape, spider_name)

    meta['debug'] = strtobool(getattr(instance, "debug", 'false'))

    if getattr(scrape, spider_name+"_path",'') or getattr(scrape.settings, spider_name+"_slugify_path",""):
        # Only add inv_id if there is a fee_path.
        # If there no fee_path, all fees for that platform will be in the
        # same response.
        meta['inv_id'] = scrape.name.linked_inv
    else:
        #If not fee path, attach the platform for lookup later
        meta['platformname'] = scrape.name.platform

    if getattr(scrape.settings, spider_name+"_prerender_js"):
        meta['splash'] = {
            'endpoint': 'render.html',
            'args': {
                'wait': 10,
                'timeout': 90
            }
        }

    meta['xpath_data'] = get_xpath_data(scrape, spider_name=spider_name)

    meta['directions'] = get_directions(scrape, spider_name=spider_name)

    meta['pdf'] = getattr(scrape.settings, spider_name+"_pdf","")

    meta['grid_style'] = getattr(scrape.settings, spider_name+"_pdf_grid_style","")

    if meta['pdf']:
        meta['pdf_tables'] = getattr(scrape.settings, spider_name+"_pdf_tables","")
        meta['pdf_manual'] = getattr(scrape.settings, spider_name+"_pdf_manual","")
        meta['pdf_mod_date'] = getattr(scrape.settings, spider_name+"_pdf_mod_date","")

    return meta

def get_camelot_params(meta, url):
    '''
    Collects the parameters for camelot from the model so they can be
    dynamically passed to camelot for table reading.
    '''
    ret = {}

    camelot_params = getattr(meta['settings'], meta['name']+"_camelot","")

    ret['filepath'] = url
    settings = ["pages", "flavor", "table_areas", "row_tol", "strip_text",
        "process_background", "line_scale"]

    for i in settings:
        if getattr(camelot_params,i):
            if i == "table_areas":
                ret[i] = [getattr(camelot_params,i)]
            else:
                ret[i] = getattr(camelot_params,i)

    # ret['column_tol'] = 50
    # ret['flavor'] = camelot_settings.flavor
    # ret['table_areas'] = list(camelot_settings.table_areas)
    # ret['column_tol'] = 0
    # ret['strip_text'] = camelot_settings.strip_text
    # table_areas=["69.07805964800265,129.7869813190117,299.301762984054,24.28337559085968"],
    return ret

def get_item(meta, type):
    '''
    Sets some base key/val pairs for the scrapy item before parsing.
    '''

    ret = {
        'type': type,
        'settings': meta['settings'],
    }

    if 'inv_id' in meta:
        ret['inv_id'] = meta['inv_id']

    if 'platformname' in meta:
        ret['platformname'] = meta['platformname']

    return ret

def get_pdf(url, headers, **kwargs):
    '''
    Gets the PDF using requests. Only for manual PDF checks
    '''

    if 'verify' in kwargs:
        return requests.get(url, headers=headers, verify=kwargs['verify'])
    else:
        return requests.get(url, headers=headers)

def parse_pdf(url, item, meta):
    '''
    Takes the PDF url and convert tables within it to an html file.

    This HTML is then converted to root_data with the xpath_root selector
    and the selector is passed to the parse_root function
    '''
    url = furl(url).remove(args=True, fragment=True).url
    parsed = urlparse(url)
    if not parsed.scheme:
        # Sets the scheme if the link is relative
        parsed = urlparse(meta['url'])
        url = urljoin(parsed.scheme+"://"+parsed.netloc, quote(url))

    if meta['pdf_manual']:
        # If the PDF can not be scraped, just log an alert if the modification
        # date has changed so it can be updated manually.
        return check_pdf_date(url, meta)

    else:
        camelot_params = get_camelot_params(meta, url)

        # So I don't get spammed with PDFMiner logs.
        logging.getLogger("pdfminer").setLevel(logging.WARNING)
        try:
            # Attempts to read the PDF with camelot
            tables = camelot.read_pdf(**camelot_params)
        except NotImplementedError:
            # If it camelot can't read the PDF due to encryption, unencrypt and
            # retry.
            url = downgrade_pdf(url)
            camelot_params = get_camelot_params(meta, url)
            tables = camelot.read_pdf(**camelot_params)

        if not meta['pdf_tables']:
            print("TABLES:")
            for t in tables:
                # For debugging/setup of scrapes
                print(t.df.to_html())
        else:
            if meta['pdf_tables'] == "all":
                table_nums = range(tables.n)
            else:
                table_nums = [int(n.strip()) for n in meta['pdf_tables'].split(",")]

            for n in table_nums:
                body = tables[n].df.to_html()
                # print(body)
                # Converts entire df stream to a scrapy selector.
                root_data = Selector(text=body).xpath(meta['xpath_data']['root'])
                print(root_data)
                # Passes the new selector to the regular parse_root function.
                item = parse_root(root_data, item, meta)

            return item

def check_pdf_date(url, meta):
    '''
    Opens the PDF and checks the date. If there is no date in the mode, print
    the date for storage.

    If the date has changed, log a message to prompt manual data check.
    '''

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'upgrade-insecure-requests' : '1',
            'connection': 'keep-alive',
            'cookie':'_ga=GA1.3.1178790649.1596189148; _gid=GA1.3.112459409.1596776805; PHPSESSID=88cee6c31c764e1e86adc809ed1eb4ff'
            }
    try:
        pdf = get_pdf(url, headers)
    except MissingSchema:
        print("Missing Schema")
    except SSLError:
        pdf = get_pdf(url, headers, verify=False)

    doc = fitz.open(stream=pdf.content, filetype="pdf")

    if not meta['pdf_mod_date']:
        # For debugging/setup
        print(doc.metadata['modDate'])

    if doc.metadata['modDate'] == meta['pdf_mod_date']:
        print("NO CHANGE TO MODIFICATION DATE")
    else:
        print("DATA REQUIRES REVISION")
        print("MOD DATE   "+doc.metadata['modDate'])

    return None


def downgrade_pdf(url):
    '''
    Uses GhostScript to downgrade the PDF version so it can be unencrypted.
    '''
    filename = Path('temp-input.pdf')
    response = requests.get(url)
    filename.write_bytes(response.content)
    output = os.system('gswin64c -sDEVICE=pdfwrite -dCompatabilityLevel=1.4 -dSAFER -dNOPAUSE -dBATCH -o temp-output.pdf temp-input.pdf ')

    return os.path.join(os.getcwd(),"temp-output.pdf")


def parse_root(root_data, item, meta):
    '''
    Iterates the data from the root xpath expression and sends it to different
    functions for parsing.
    '''
    xpath_data = meta['xpath_data']
    headers = []

    for i, node in enumerate(root_data):
        # Iterates root data. This is done for all requests.
        if meta['debug']:
            print(node)

        if xpath_data['node']:
            # For data where there is a sub-node
            # Also for "Grid style" AA disclosure in one table in a PDF
            item = iterate_node_data(node, i, item, xpath_data, meta, headers)

        else:
            if xpath_data['inv_name_path']:
                # If all data (AA only) is in a single request.
                inv = node.xpath(xpath_data['inv_name_path']).get()
                item[inv] = {}
                item[inv] = get_item_data(node, xpath_data, meta, item[inv])
            else:
                item = get_item_data(node, xpath_data, meta, item)


    return item

def iterate_node_data(node, i, item, xpath_data, meta, headers):
    '''
    Mostly for iterating grid-style tables for asset allocation.
    Note that for grid-style AA, the node xpath is usually just .//td or
    .//th | .//td and the inv_name, name and data paths should be null.
    '''
    node_data = node.xpath(xpath_data['node'])

    if meta['debug']:
        print(node_data)

    # For "Grid style" AA disclosure in one table
    if meta['grid_style']:
        #Remove empty cells from table parsing
        # Why? - removed for Mine Super.
        # node_data = [n for n in node_data if n.xpath('.//text()').get()]

        for x, node in enumerate(node_data):
            if i == 0:
                if x != 0:
                    # Header rows, exclude very first cell (top left)
                    if not xpath_data['inv_name_path']:
                        inv = node.xpath('.//text()').getall()
                    else:
                        inv = node.xpath(xpath_data['inv_name_path']).getall()

                    inv = " ".join(inv)
                    inv = clean_inv_name(inv, meta['directions'])
                    item[inv] = {}
                    headers.append(inv)
                    print(headers)
            else:
                if x != 0:
                    name = node_data[0].xpath('.//text()').get()
                    # print(name)
                    name = clean_name(name, meta['directions'])
                    if not xpath_data['data_path']:
                        data = node.xpath('.//text()').get()
                    else:
                        data = node.xpath(xpath_data['data_path']).get()
                    item[headers[x-1]][name] = data
                # Data rows

    elif xpath_data['inv_name_path']:
        inv = node.xpath(xpath_data['inv_name_path']).getall()

        if meta['debug']:
            print(inv)

        if inv:
            inv = " ".join(inv)
            inv = clean_inv_name(inv, meta['directions'])
            item[inv] = {}
            print(inv)

            for node in node_data:
                item[inv] = get_item_data(node, xpath_data, meta, item[inv])

    else:
        for node in node_data:
            item = get_item_data(node, xpath_data, meta, item)

    return item


def clean_name(name, directions):
    '''
    Cleans the aa allocation_name, bs investment name and fee investment name
    '''
    #Removes newlines
    name = name.replace("\\n", "")

    if directions['excise_name_string']:
        excise_list = directions['excise_name_string'].split(',')
        start = excise_list[0]
        end = excise_list[1]
        regex = re.compile('{}(.+?){}'.format(re.escape(start), re.escape(end)))
        print(regex)
        try:
            name = regex.findall(name)[0]
            print(name)
            print("Excised name: "+name)
        except AttributeError:
            # AAA, ZZZ not found in the original string
            print("Unable to excise name from xpath data")

    name = name.strip()

    if directions['strings_to_remove']:
        for string in directions['strings_to_remove']:
            name = name.replace(string, ' ')

    if "\xa0" in name:
        name = name.replace("\xa0","")


    if directions['split_name_string']:
        name = name.split(directions['split_name_string'])[0]
    name = name.strip()


    return name

def clean_inv_name(name, directions):
    '''
    Cleans the AA investment name
    '''
    name = name.replace("\\n", "")

    if directions['excise_inv_name_string']:
        excise_list = directions['excise_inv_name_string'].split(',')
        start = excise_list[0]
        end = excise_list[1]
        regex = re.compile('{}(.+?){}'.format(re.escape(start), re.escape(end)))
        print(regex)
        try:
            name = regex.findall(name)[0]
            print(name)
            print("Excised name: "+name)
        except AttributeError:
            # AAA, ZZZ not found in the original string
            print("Unable to excise name from xpath data")

    if directions['split_inv_name_string']:
        name = name.split(directions['split_inv_name_string'])[0]

    if directions['strings_to_remove']:
        for string in directions['strings_to_remove']:
            name = name.replace(string, ' ')

    if directions['capitalise_names']:
        name = name.title()

    name = name.strip()

    return name

def get_item_data(node, xpath_data, meta, item):
    '''
    Gets the "name" of the item (key)
    '''
    xpath_data = meta['xpath_data']
    directions = meta['directions']

    if xpath_data['name_path']:
        # If the name can be grabbed using a selector
        name = node.xpath(xpath_data['name_path']).getall()
        name = " ".join(name)
        name = clean_name(name, directions)

    elif directions['split_name_string']:
        # If the name needs to be split from a string using a keyword
        name = node.getall()
        name = " ".join(name)
        name = clean_name(name, directions)
    elif meta['inv_id']:
        #If it is a fee scrape and we already know the name
        name = 'data'
    else:
        #If there is no name (i.e. it is the only investment in the platform)
        name = str(item['platformname'])

    if not name:
        print("ERROR: Name path incorrect")

    if name:
        if meta['debug']:
            print(name)
        val = get_val(item, node, xpath_data, directions)
        if val:
            if item.get(name, False):
                # If there are duplicate AA ames (for example "Defensive" and
                # "Growth" Property), convert the vals to floats, add them
                # together, then convert back to str for processing.
                item[name] = early_val_clean(item[name])
                val = early_val_clean(val)
                item[name] += val
                item[name] = str(item[name])
            else:
                item[name] = val

    if val:
        return item


def get_val(item, node, xpath_data, directions):
    '''
    Gets the value for each key
    '''
    if (item.get('type',"") == "buy_spread" or item.get('type',"") == "sell_spread"):
        data_path = item['type']+'_data_path'
    else:
        data_path = 'data_path'

    if xpath_data[data_path]:
        #If the val can be grabbed using a selector
        val = node.xpath(xpath_data[data_path]).getall()
        val = " ".join(val)
        if directions['use_percentage_regex']:
            val = apply_percentage_regex(val)
            if not val:
                return None

    elif directions['use_percentage_regex']:
        # If the val needs to be split from a string with the name
        val = node.getall()
        val = " ".join(val)
        val = apply_percentage_regex(val)
        if not val:
            return None

    else:
        pass
        #Do someting else

    if "\\n" in val:
        # Replaces newlines with spaces
        val = val.replace("\\n"," ")

    #removes extra whitespace
    val = " ".join(val.split())


    if not val:
        print("ERROR: No value for this name")

    return val

def apply_percentage_regex(val):
    '''
    REGEX finds percentages in string
    '''
    try:
        #REGEX finds percentages in string
        val = re.search("(\d+(\.\d+)?%)", val).group()
        return val
    except Exception:
        print("No regex match found")
        return None


def early_val_clean(val):
    '''
    For items that need to be roughly cleaned early due to duplicate keys
    '''
    if "%" in val:
        val = val.split("%")[0]

    val = val.strip()
    val = float(val)
    return val

def yield_item(item, instance):
    '''
    Allows debug mode via -a debug=T in command line
    '''
    if strtobool(getattr(instance, "debug", 'false')):
        print("DEBUG:")
        print(item)
    else:
        print("Scraped:")
        return item


class AASpider(scrapy.Spider):
    name = "aa"
    custom_settings = {
        'ITEM_PIPELINES': {
           'scrape_module.pipelines.CleanDataPipeline': 301,
           'scrape_module.pipelines.CheckInvExistsPipeline': 302,
           'scrape_module.pipelines.AssignInvId': 303,
           'scrape_module.pipelines.CheckAANamesPipeline': 304,
           'scrape_module.pipelines.UpdateAANamesPipelines': 305,
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):

        scrape_data = get_data(self)

        for scrape in scrape_data:
            meta = get_meta(scrape, self.name, self)
            yield scrapy.Request(get_url(scrape, self.name), self.parse, meta=meta)


    def parse(self, response):

        item = get_item(response.meta, "aa")

        xpath_data = response.meta['xpath_data']

        if response.meta["pdf"]:
            open_in_browser(response)
            url_data = response.xpath(xpath_data['url']).getall()
            url_data = " ".join(url_data)
            item = parse_pdf(url_data, item, response.meta)


        else:
            root_data = response.xpath(xpath_data['root'])
            if not root_data:
                open_in_browser(response)
            # open_in_browser(response)

            item = parse_root(root_data, item, response.meta)
            # print(item)

        if response.meta.get("platformname"):
            # If all data is in a single request and needs to be split
            if item:
                for k,v in item.items():
                    if k not in excluded_keys and v:
                        single_item = v
                        single_item['invname'] = k
                        single_item['type'] = item['type']
                        single_item['settings'] = item['settings']
                        single_item['platformname'] = item['platformname']
                        # print(single_item)
                        yield yield_item(single_item, self)
        else:
            yield yield_item(item, self)

class FeeSpider(scrapy.Spider):
    name = "fee"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrape_module.pipelines.CleanDataPipeline': 300,
            'scrape_module.pipelines.CheckInvExistsPipeline': 301,
            'scrape_module.pipelines.UpdateInvPipeline': 302,
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


    def start_requests(self):
        scrape_data = get_data(self)

        for scrape in scrape_data:
            meta = get_meta(scrape, self.name, self)
            yield scrapy.Request(get_url(scrape, 'fee'), self.parse, meta=meta)

    def parse(self, response):

        item = get_item(response.meta, "_investment_fee")

        xpath_data = response.meta['xpath_data']

        if response.meta["pdf"]:
            url_data = response.xpath(xpath_data['url']).getall()
            url_data = " ".join(url_data)
            if not url_data:
                open_in_browser(response)
            item = parse_pdf(url_data, item, response.meta)
            yield yield_item(item, self)

        else:
            root_data = response.xpath(xpath_data['root'])
            # open_in_browser(response)

            if not root_data:
                open_in_browser(response)

            # print(root_data)

            item = parse_root(root_data, item, response.meta)
            # print(item)
            yield yield_item(item, self)


class BSSpider(scrapy.Spider):
    name = "bs"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrape_module.pipelines.CleanDataPipeline': 300,
            'scrape_module.pipelines.CheckInvExistsPipeline': 301,
            'scrape_module.pipelines.UpdateInvPipeline': 302,
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        scrape_data = get_data(self)

        for scrape in scrape_data:
            meta = get_meta(scrape, self.name, self)
            yield scrapy.Request(get_url(scrape, "bs"), self.parse, meta=meta)

    def parse(self, response):
        bs = {
            'Buy': {},
            'Sell': {},
        }
        for k in bs.keys():
            bs[k] = get_item(response.meta, k.lower()+'_spread')

        xpath_data = response.meta['xpath_data']

        if response.meta["pdf"]:
            url_data = response.xpath(xpath_data['url']).getall()
            url_data = " ".join(url_data)
            for k,v in bs.items():
                bs[k] = parse_pdf(url_data, v, response.meta)

            for k,v in bs.items():
                yield yield_item(v, self)

        else:
            root_data = response.xpath(xpath_data['root'])

            if not root_data:
                open_in_browser(response)
            headers = []
            for i, node in enumerate(root_data):

                if xpath_data['node']:

                    for k,v in bs.items():
                        bs[k] = iterate_node_data(node, i, v, xpath_data, response.meta, headers)

                elif xpath_data['name_path']:

                    for k,v in bs.items():
                        bs[k] = get_item_data(node, xpath_data, response.meta, v)

            for k,v in bs.items():

                yield yield_item(v, self)
