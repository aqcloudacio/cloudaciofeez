import scrapy
import re
import fitz
import requests

from distutils.util import strtobool
from requests.exceptions import MissingSchema, SSLError
from urllib.parse import urlparse, urljoin

from furl import furl
from scrapy.utils.response import open_in_browser
from scrapes.models import AplScrapeSettings
from scrapy.utils.log import configure_logging

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

    Allows for one command line mod
    -a single_scrape_platform_id=123 (only the group of scrapes with this settings id)
    '''

    if getattr(instance, 'single_scrape_platform_id',''):
        #if you want to scape a single platform
        scrape_data = AplScrapeSettings.objects.filter(id=instance.single_scrape_platform_id)
    else:
        scrape_data = AplScrapeSettings.objects.all()

    return scrape_data


def get_url(scrape, name):
    '''
    Gets the url for each scrape, based off the root scrape in the settings
    '''
    root = str(getattr(scrape, "root"))

    if root:
        return root
    else:
        return None

def get_xpath_data(scrape, spider_name):
    '''
    Collects xpath expressions from the model.
    '''

    return {
        'url': scrape.xpath_url,
    }


def get_meta(scrape, spider_name, instance):
    '''
    Builds a packet of metadata for each scrape, so it can be used throughout
    the scrape rather than calling from the DB every time is needs to be used.
    '''
    meta = {}

    # meta['settings'] = scrape.settings
    meta['name'] = spider_name
    meta['url'] = get_url(scrape, spider_name)

    meta['debug'] = strtobool(getattr(instance, "debug", 'false'))

    meta['platformname'] = scrape.platform
    meta['platformid'] = scrape.platform.id

    if getattr(scrape, "prerender_js"):
        meta['splash'] = {
            'endpoint': 'render.html',
            'args': {
                'wait': 10,
                'timeout': 90
            }
        }

    meta['xpath_data'] = get_xpath_data(scrape, spider_name=spider_name)

    meta['pdf'] = getattr(scrape, "pdf","")

    if meta['pdf']:
        meta['pdf_manual'] = getattr(scrape, "pdf_manual","")
        meta['pdf_mod_date'] = getattr(scrape, "pdf_mod_date","")

    meta['next_check'] = getattr(scrape, "next_check","")

    meta['keep_url_args'] = getattr(scrape, "keep_url_args","")
    meta['direct_link'] = getattr(scrape, "direct_link","")
    meta['excise_string'] = getattr(scrape, "excise_string","")



    return meta


def get_item(meta, type):
    '''
    Sets some base key/val pairs for the scrapy item before parsing.
    '''

    ret = {
        'type': type,
        # 'settings': meta['settings'],
    }

    if 'platformid' in meta:
        ret['platformid'] = meta['platformid']

    if 'platformname' in meta:
        ret['platformname'] = meta['platformname']

    return ret


def excise_string(url, meta):

    excise_list = meta['excise_string'].split(',')
    start = excise_list[0]
    end = excise_list[1]
    regex = re.compile('{}(.+?){}'.format(re.escape(start), re.escape(end)))

    try:
        url = regex.findall(url)[0]
        # print("Excised href: "+url)
        return url

    except AttributeError:
        # AAA, ZZZ not found in the original string
        print("Unable to excise href from xpath data")

    except Exception as e:
        print(e)
        print(meta['platformname'])


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
    Only manual processing here - checks the date against the recorded date in
    the DB and logs message accordingly.
    '''
    if not meta['keep_url_args']:
        url = furl(url).remove(args=True, fragment=True).url

    if meta['excise_string']:
        url = excise_string(url, meta)

    parsed = urlparse(url)

    if not parsed.scheme:
        # Sets the scheme if the link is relative
        parsed = urlparse(meta['url'])
        # Removed quote(url) code as it was adding unreadable characters.
        #Unsure of consequences.
        url = urljoin(parsed.scheme+"://"+parsed.netloc, url)
        print(url)

    if meta['pdf_manual']:
        # If the PDF can not be scraped, just log an alert if the modification
        # date has changed so it can be updated manually.
        message = check_pdf_date(url, meta)
        return (url, message)

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
        return ("error", f"{meta['platformname']}: Missing Schema")
    except SSLError:
        pdf = get_pdf(url, headers, verify=False)

    try:
        doc = fitz.open(stream=pdf.content, filetype="pdf")
    except Exception:
        return ("error", f"{meta['platformname']}: Can not open PDF")


    if not meta['pdf_mod_date']:
        # For debugging/setup
        print(doc.metadata['modDate'])

    if doc.metadata['modDate'] == meta['pdf_mod_date']:
        return("info", f"{meta['platformname']}: No change to mod date")
    else:
        return ("warning", f"{meta['platformname']}: Revision required. New date: {doc.metadata['modDate']}")

    return None

#
# def yield_item(item, instance):
#     '''
#     Allows debug mode via -a debug=T in command line
#     '''
#     if strtobool(getattr(instance, "debug", 'false')):
#         print("DEBUG:")
#         print(item)
#     else:
#         print("Scraped:")
#         return item


class AplSpider(scrapy.Spider):
    name = "apl"
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }
    configure_logging()


    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        scrape_data = get_data(self)

        for scrape in scrape_data:
            meta = get_meta(scrape, self.name, self)
            # self.logger.info(f"Starting scrape for {meta['platformname']}")

            url = get_url(scrape, self.name)

            if url:
                try:
                    yield scrapy.Request(url, self.parse, meta=meta)
                except Exception as e:
                    print(e)
            else:
                if meta['next_check']:
                    self.logger.info(f"{meta['platformname']}: Next manual check on {meta['next_check']}")
                else:
                    self.logger.error(f"{meta['platformname']}: could not retrieve URL")


    def parse(self, response):

        item = get_item(response.meta, "platform")

        xpath_data = response.meta['xpath_data']

        if response.meta["pdf"]:
            # print(xpath_data['url'])
            try:
                if not response.meta['direct_link']:
                    # open_in_browser(response)
                    url_data = response.xpath(xpath_data['url']).getall()
                    url_data = " ".join(url_data)
                else:
                    url_data = response.url
            except Exception as e:
                print(e)
                print(response.meta['platformname'])
            # print(url_data)
            url, log_data = parse_pdf(url_data, item, response.meta)
            level, message = log_data
            # Sets the item url to the direct link url for pipeline
            item['url'] = url
            # Logs the outcome of the scrape.

            if level == "warning":
                self.logger.warning(message)
            elif level == "info":
                self.logger.info(message)
            elif level == "error":
                self.logger.error(message)
            else:
                pass

        yield item
