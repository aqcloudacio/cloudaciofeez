from django.db import models

from investments.models import InvestmentName
from platforms.models import PlatformNames

class CamelotSettings(models.Model):

    # Pages to scrape for readable tables.
    # Formats = "1" "1,2" "1-2"
    settings = models.ForeignKey('scrapes.InvestmentScrapeSettings',
                                 on_delete=models.CASCADE,
                                 related_name="settings",
                                 blank=True, null=True)
    TYPE_CHOICES = [
        ("aa", "aa"),
        ("fee", "fee"),
        ("bs", "bs"),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES,
                              blank=True, null=True)
    pages = models.CharField(max_length=50, default="1")
    flavor = models.CharField(max_length=10, default="lattice")
    table_areas = models.CharField(max_length=200, null=True)
    row_tol = models.IntegerField(blank=True, null=True)
    strip_text = models.CharField(max_length=20, blank=True, default='')
    process_background = models.BooleanField(default=False)
    line_scale = models.IntegerField(blank=True, null=True)


    def __str__(self):
        if self.aa_settings.exists() or self.fee_settings.exists() or self.bs_settings.exists():
            return str(self.settings)+" - "+self.type
        else:
            return str(self.settings)+" - unassigned"



class InvestmentScrapeSettings(models.Model):
    '''
    Scrape settings for investments owned by a particular platform
    '''
    platform = models.ForeignKey(PlatformNames,
                                 on_delete=models.SET_NULL,
                                 related_name="scrape_settings",
                                 blank=True, null=True)
    notes = models.CharField(max_length=300, blank=True, null=True)
    ######
    #AA
    #####
    # Link to the AA root for a platform. For web-based AA only (not PDF)
    # Must be the full link, not ending with /
    aa_root = models.URLField(max_length=300, blank=True, null=True)
    # If no aa_path is given, will convert scrape.name to a slug
    # and attempt to use that as a path.
    aa_slugify_path = models.BooleanField(default=False)
    aa_slugify_path_no_hyphens = models.BooleanField(default=False)
    # If the required data is from dynamic JS that needs to be pre-rendered
    # using Splash
    aa_prerender_js = models.BooleanField(default=False)
    # If the data is in a PDF
    aa_pdf = models.BooleanField(default=False)
    aa_camelot = models.ForeignKey(CamelotSettings,
                                    on_delete=models.SET_NULL,
                                    related_name="aa_settings",
                                    blank=True, null=True)
    # Collected tables to scrape. This is for the entire set of tables across
    # All scraped pages. Format = "0,1,2,3,4".
    aa_pdf_tables = models.CharField(max_length=100, blank=True, null=True)
    aa_pdf_manual = models.BooleanField(default=False)
    aa_pdf_mod_date = models.CharField(max_length=100, default='')
    aa_pdf_grid_style = models.BooleanField(default=False)


    ######
    #FEES
    #####
    # Link to the AA root for a platform. For web-based AA only (not PDF)
    # Must be the full link, not ending with /
    fee_root = models.URLField(max_length=300, blank=True, null=True)
    # If no fee_path is given, will convert scrape.name to a slug
    # and attempt to use that as a path.
    fee_slugify_path = models.BooleanField(default=False)
    fee_slugify_path_no_hyphens = models.BooleanField(default=False)
    # If the required data is from dynamic JS that needs to be pre-rendered
    # using Splash
    fee_prerender_js = models.BooleanField(default=False)
    # If the data is in a PDF
    fee_pdf = models.BooleanField(default=False)
    fee_camelot = models.ForeignKey(CamelotSettings,
                                    on_delete=models.SET_NULL,
                                    related_name="fee_settings",
                                    blank=True, null=True)
    # Collected tables to scrape. This is for the entire set of tables across
    # All scraped pages. Format = "0,1,2,3,4".
    fee_pdf_tables = models.CharField(max_length=100, blank=True, null=True)
    #If the PDF is manual collection
    fee_pdf_manual = models.BooleanField(default=False)
    #Mod date on the PDF itself.
    fee_pdf_mod_date = models.CharField(max_length=100, default='')

    ######
    #BUY SELL
    #####
    # Link to the AA root for a platform. For web-based AA only (not PDF)
    # Must be the full link, not ending with /
    bs_root = models.URLField(max_length=300, blank=True, null=True)
    # If the required data is from dynamic JS that needs to be pre-rendered
    # using Splash
    bs_prerender_js = models.BooleanField(default=False)
    # If the data is in a PDF
    bs_pdf = models.BooleanField(default=False)
    bs_camelot = models.ForeignKey(CamelotSettings,
                                    on_delete=models.SET_NULL,
                                    related_name="bs_settings",
                                    blank=True, null=True)
    # Collected tables to scrape. This is for the entire set of tables across
    # All scraped pages. Format = "0,1,2,3,4".
    bs_pdf_tables = models.CharField(max_length=100, blank=True, null=True)
    #If the PDF is manual collection
    bs_pdf_manual = models.BooleanField(default=False)
    #Mod date on the PDF itself.
    bs_pdf_mod_date = models.CharField(max_length=100, default='')

    ##General formatting
    #strings to remove from name fields, should be separated by commas
    strings_to_remove = models.CharField(max_length=300, blank=True, null=True)
    capitalise_names = models.BooleanField(default=True)

    #AA
    #Xpath aa url path - for PDF URLs
    xpath_aa_url = models.CharField(max_length=300, blank=True, null=True)
    #Xpath aa query root
    xpath_aa_root = models.CharField(max_length=1000, blank=True, null=True)
    xpath_aa_node = models.CharField(max_length=300, blank=True, null=True)
    #Optional - only when all aas are in one request. gets the investment name
    xpath_aa_inv_name_path = models.CharField(max_length=300, blank=True, null=True)
    #Xpath paths
    xpath_aa_name_path = models.CharField(max_length=300, blank=True, null=True)
    xpath_aa_allocation_path = models.CharField(max_length=300, blank=True, null=True)
    #String for splitting the aa_inv_name on
    aa_split_inv_name_string = models.CharField(max_length=100, blank=True, null=True)
    #String for splitting the aa_name on
    aa_split_name_string = models.CharField(max_length=100, blank=True, null=True)
    aa_use_percentage_regex = models.BooleanField(default=False)
    # If the aa name string needs to be split from a long string
    # This field needs to be passed two string separated by a comma. It will
    # find the text between the two strings.
    aa_excise_name_string = models.CharField(max_length=100, blank=True, null=True)
    aa_excise_inv_name_string = models.CharField(max_length=100, blank=True, null=True)

    #FEES
    #Xpath fee url path - for PDF URLs
    xpath_fee_url = models.CharField(max_length=300, blank=True, null=True)
    #Xpath fee query root
    xpath_fee_root = models.CharField(max_length=1000, blank=True, null=True)
    xpath_fee_node = models.CharField(max_length=300, blank=True, null=True)
    #Xpath Paths
    xpath_fee_name_path = models.CharField(max_length=300, blank=True, null=True)
    xpath_fee_path = models.CharField(max_length=300, blank=True, null=True)
    #String for splitting the fee_name on
    fee_split_name_string = models.CharField(max_length=100, blank=True, null=True)
    #Use REGEX to get the percentage from a string
    fee_use_percentage_regex = models.BooleanField(default=False)
    # If the fee name string needs to be split from a long string
    # This field needs to be passed two string separated by a comma. It will
    # find the text between the two strings.
    fee_excise_name_string = models.CharField(max_length=100, blank=True, null=True)
    #PDF paths
    # pdf_fee_name_index = models.SmallIntegerField(blank=True, null=True)
    # pdf_fee_index = models.SmallIntegerField(blank=True, null=True)

    #BUY sell
    #Xpath bs url path - for PDF URLs
    xpath_bs_url = models.CharField(max_length=300, blank=True, null=True)
    #Xpath queires
    xpath_bs_root = models.CharField(max_length=300, blank=True, null=True)
    xpath_bs_node = models.CharField(max_length=300, blank=True, null=True)
    #Xpath Paths
    xpath_bs_name_path = models.CharField(max_length=300, blank=True, null=True)
    xpath_bs_buy_spread_path = models.CharField(max_length=300, blank=True, null=True)
    xpath_bs_sell_spread_path = models.CharField(max_length=300, blank=True, null=True)
    #String for splitting the fee_name on
    # Can be multiple strings split with a comma
    bs_split_name_string = models.CharField(max_length=100, blank=True, null=True)
    #Use REGEX to get the percentage from a string
    bs_use_regex_percentage = models.BooleanField(default=False)
    # If the bs name string needs to be split from a long string
    # This field needs to be passed two string separated by a comma. It will
    # find the text between the two strings.
    bs_excise_name_string = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.platform.name


class InvestmentScrape(models.Model):

    '''
    Details for each investment's scrape. One per investment.
    Platform-level settings are located in the InvestmentScrapeSettings model.
    '''
    name = models.ForeignKey(InvestmentName,
                             on_delete=models.CASCADE,
                             related_name="scrapes",
                             blank=True, null=True)
    settings = models.ForeignKey(InvestmentScrapeSettings,
                                 on_delete=models.CASCADE,
                                 related_name="scrapes",
                                 blank=True, null=True)
    last_checked = models.DateTimeField(auto_now=True)
    last_changed = models.DateTimeField(auto_now_add=True)

    ######
    #AA
    #####
    # Path from the AA root to get the AA for this record. Partial route
    # must start with a /
    # If there is no path, but you want to treat the investment as a single
    # (not platform-level scrape), you can pass '/'
    aa_path = models.CharField(max_length=100, blank=True)

    ######
    #FEES
    #####
    # Path from the fee root to get the fee for this record. Partial route
    # must start with a /
    fee_path = models.CharField(max_length=100, blank=True)

    ######
    #BUY SELL
    #####
    # Path from the fee root to get the fee for this record. Partial route
    # must start with a /
    bs_path = models.CharField(max_length=100, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'settings'],
                                    name='unique_investment_scrape')
        ]

    def __str__(self):
        return str(self.name)


class PlatformScrapeSettings(models.Model):
    '''
    Scrape settings for platforms themselves (fee/data scrapes).
    '''
    platform = models.ForeignKey(PlatformNames,
                                 on_delete=models.SET_NULL,
                                 related_name="fee_scrape_settings",
                                 blank=True, null=True)
    notes = models.CharField(max_length=300, blank=True, null=True)
    last_checked = models.DateTimeField(auto_now=True)
    last_changed = models.DateTimeField(auto_now_add=True)

    # For manual checks - when the next check is needed
    next_check = models.DateTimeField(blank=True, null=True)
    # Link to the url root for a platform.
    # Must be the full link, not ending with /
    root = models.URLField(max_length=300, blank=True, null=True)
    # If the required data is from dynamic S that needs to be pre-rendered
    # using Splash
    prerender_js = models.BooleanField(default=False)
    # If the data is in a PDF (assume all are, just in case we change later.)
    pdf = models.BooleanField(default=True)
    # All platform fee PDF scraping will be manual to start with.
    pdf_manual = models.BooleanField(default=True)
    # Last modified date of PDF.
    pdf_mod_date = models.CharField(max_length=100, default='')

    #Xpath aa url path - for PDF URLs
    xpath_url = models.CharField(max_length=300, blank=True, null=True)
    #Keeps args from the xpath url
    keep_url_args = models.BooleanField(default=False)

    #If the root is a direct link to the file - only to be used if the file
    # appears to not be static
    direct_link = models.BooleanField(default=False)

    # If the href needs to be split from a long string (for example a JS func)
    # This field needs to be passed two strings separated by a comma. It will
    # find the text between the two strings.
    excise_string = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.platform.name

class AplScrapeSettings(models.Model):
    '''
    Scrape settings for apls for platforms (scrapes for the investment
    limitations of fee groups).
    '''
    platform = models.ForeignKey(PlatformNames,
                                 on_delete=models.SET_NULL,
                                 related_name="apl_scrape_settings",
                                 blank=True, null=True)
    notes = models.CharField(max_length=300, blank=True, null=True)
    last_checked = models.DateTimeField(auto_now=True)
    last_changed = models.DateTimeField(auto_now_add=True)

    # For manual checks - when the next check is needed
    next_check = models.DateTimeField(blank=True, null=True)
    # Link to the url root for a platform.
    # Must be the full link, not ending with /
    root = models.URLField(max_length=300, blank=True, null=True)
    # If the required data is from dynamic S that needs to be pre-rendered
    # using Splash
    prerender_js = models.BooleanField(default=False)
    # If the data is in a PDF (assume all are, just in case we change later.)
    pdf = models.BooleanField(default=True)
    # All platform fee PDF scraping will be manual to start with.
    pdf_manual = models.BooleanField(default=True)
    # Last modified date of PDF.
    pdf_mod_date = models.CharField(max_length=100, default='')

    #Xpath aa url path - for PDF URLs
    xpath_url = models.CharField(max_length=300, blank=True, null=True)
    #Keeps args from the xpath url
    keep_url_args = models.BooleanField(default=False)

    #If the root is a direct link to the file - only to be used if the file
    # appears to not be static
    direct_link = models.BooleanField(default=False)

    # If the href needs to be split from a long string (for example a JS func)
    # This field needs to be passed two strings separated by a comma. It will
    # find the text between the two strings.
    excise_string = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.platform.name
