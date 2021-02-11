# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from django.shortcuts import get_list_or_404, get_object_or_404
from itemadapter import ItemAdapter
from decimal import Decimal

from investments.models import (AssetAllocationName, AssetAllocation,
                                InvestmentName, Investment)
from scrapes.models import InvestmentScrape
from platforms.models import PlatformNames

excluded_keys = [
    'platformname',
    'inv_id',
    'invname',
    'type',
    '',
    'settings',
]

class CleanDataPipeline(object):
    '''
    Cleans the data collected so it can be saved into the DB.
    '''
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if "\\n" in adapter.get('invname',""):
            # Replaces newlines with spaces
            invname = adapter['invname'].replace("\\n"," ")
            adapter['invname'] = invname

        # Removes extra spaces inside string when collecting new investments
        if adapter.get('invname',''):
            invname = " ".join(adapter['invname'].split())
            adapter['invname'] = invname

        # Removes keys with NoneType vals. Could be changed to a dict comprehension
        del_items = []
        for key, val in adapter.items():
            if key not in excluded_keys:
                if not val:
                    del_items.append(key)
        for k in del_items:
            del adapter[k]

        for key, val in adapter.items():
            if key not in excluded_keys:
                # Removes percentage sign + any text after and divides by 100
                if "%" in val:
                    adapter[key] = val.split("%")[0]

                #Nil items that are not numbers ("Zero", "Nil", etc)
                try:
                    adapter[key] = Decimal(adapter[key])
                except Exception:
                    adapter[key] = 0

                # Converts integer/float to correct percentage decimal.
                adapter[key] = Decimal(adapter[key])/100

        return item


class CheckAANamesPipeline(object):
    '''
    Checks if the asset allocation names collected exist in the database.
    If they don't, create a new one.
    '''
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        existing_aa_names = get_list_or_404(AssetAllocationName)

        for key in adapter.keys():
            if key not in excluded_keys:
                if key.casefold() not in (i.name.casefold() for i in existing_aa_names):
                    aa_name = AssetAllocationName(name=key.title())
                    aa_name.save()
        return item


class UpdateAANamesPipelines(object):

        def process_item(self, item, spider):

            adapter = ItemAdapter(item)

            # Converts keys to lowercase so they can be matched to
            # case-insensitive models
            lowercase_adapter = {k.lower(): v for k, v in adapter.items()}

            # Gets AA Names again (new ones added)
            existing_aa_names = get_list_or_404(AssetAllocationName)

            try:
                existing_aa = get_list_or_404(AssetAllocation,
                                              investment=adapter['inv_id'])
            except Exception:
                existing_aa = []

            #delete old allocationss (if they have changed)
            unused_names = [aa for aa in existing_aa if str(aa.name).lower() not in lowercase_adapter.keys()]
            for name in unused_names:
                name.delete()

            #Update existing ones
            for aa in existing_aa:
                # Matches the lowercase existing aa name to the lowercase
                # dict value and saves the updated allocation.
                try:
                    aa.percentage = lowercase_adapter[str(aa.name).lower()]
                except KeyError as e:
                    print(f"LOG: Asset class {e} no longer exists in scraped data")
                aa.save()

                lowercase_adapter.pop(str(aa.name).lower())

            #Create new ones
            for k,v in lowercase_adapter.items():

                aa_name = next((i for i in existing_aa_names if i.name.lower() == k), None)
                #Get the AA NAME ID
                if k not in excluded_keys:
                    allocation = AssetAllocation(name=aa_name,
                                                 percentage=v,
                                                 investment_id=adapter['inv_id'])
                    allocation.save()


            return item


class AssignInvId(object):
    '''
    Assigns an inv_id to an item without one. The adapter must have invname.
    '''
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('invname', ""):
            investment = get_object_or_404(InvestmentName,
                                            name=adapter['invname'],
                                            platform=adapter['platformname'])
            adapter['inv_id'] = investment.linked_inv

        return item




class CheckInvExistsPipeline(object):
    '''
    Currently only for single-page fees (all fees in one dict)

    Searches for the investment
    '''
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'inv_id' in adapter.keys():
            # Nothing here, as it is assumed an inv_id means the investment
            # already exists. Might change in future.
            # For now, will just pass on this pipeline.
            pass

        elif 'invname' in adapter.keys():
            # If the invname has been passsed and there is no inv_id, that
            # means the investment must not exist (it couldn't be found in
            # the AssignInvId pipeline)
            platform = adapter['platformname']
            investments = InvestmentName.objects.filter(platform_id=platform)
            if str(adapter['invname']).casefold() not in [str(i.name).casefold() for i in investments]:
                # If the invname does not exist in the investments for this
                # platform, create a new investment and matching scrape.
                new_inv = InvestmentName(name=adapter['invname'].title(),
                                         platform=adapter['platformname'])
                new_inv.save()
                new_inv_scrape = InvestmentScrape(name=new_inv,
                                                  settings=adapter['settings'])
                new_inv_scrape.save()

                # Should be a log
                print('NEW INV CREATED:', new_inv.name)

        else:
            # If all fees/buy spreads/sell spreads are in the same response.
            platform = adapter['platformname']
            investmentnames = InvestmentName.objects.filter(platform_id=platform)
            for key in [k for k in adapter.keys() if k not in excluded_keys]:
                # Iterate investments in the item
                if str(key).casefold() not in [str(i.name).casefold() for i in investmentnames]:
                    # If they don't exist (as above), create new investment
                    # and matching scrape.
                    new_inv = InvestmentName(name=key.title(),
                                             platform=adapter['platformname'])
                    new_inv.save()
                    new_inv_scrape = InvestmentScrape(name=new_inv,
                                                      settings=adapter['settings'])
                    new_inv_scrape.save()

                    # Should be a log
                    print('NEW INV CREATED:', new_inv.name)

        return item


class UpdateInvPipeline(object):
    '''
    Updates the given investment item's _investment_fee, buy_spread or
    sell_spread.

    By the time the item reaches this function, it will either be assigned an
    inv_id, or can be looked up via its platformname.
    '''
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if 'inv_id' in adapter.keys():
            # If inv_id is passed in item, look up the investment instance and
            # save the data directly.
            inv = get_object_or_404(Investment,
                                    id=adapter['inv_id'],
                                    template=True)
            setattr(inv, adapter['type'], adapter['data'])
            inv.save()
        else:
            lowercase_adapter = {k.lower(): v for k, v in adapter.items()}
            # If all investments are in the same item, get all investments for
            # the platform and iterate through them.
            platform = adapter['platformname']
            investments = Investment.objects.filter(name__platform=platform,
                                                    template=True)

            for inv in investments:
                # For each investment, assign the data from the item to the
                # relevant field - the adapter['type'])
                setattr(inv, adapter['type'], lowercase_adapter[str(inv.name.name).casefold()])
                inv.save()

        return item

class SaveLinkPipeline(object):
    '''
    For PDS scrapes only - saves the direct link (link to doc) in the
    platformname model.
    '''
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        print(item['platformid'])

        if 'url' in adapter.keys():

            platformname = (PlatformNames.objects.filter(id=item['platformid']))[0]

            platformname.direct_pds_link = adapter['url']
            platformname.save()
