# filter investment list to exclude mstar or custom items
# check if inv has url for aa
# if it does, visit site
# check meta? to see if changed
# if it has, search for data
# if data different, update record
# mark record as checked on curentDate

from scrapes.models import InvestmentScrape

def scrape_investments():
    inv_scrapes = InvestmentScrape.objects.all()
    for inv in inv_scrapes:
        pass
        # FOR AA ROOT
        #     CHECK AA items
