from django.db import models

from platforms.models import PlatformNames
from investments.models import InvestmentName
from portfolios.models import Portfolio
# Create your models here.

class AdvertType(models.Model):

    type = models.CharField(max_length=50)

    # starred_super
    # starred_invwrap
    # starred_pension
    # starred_investment
    # starred_portfolio
    # popover
    # document_cta

    def __str__(self):
        return self.type


class Advertiser(models.Model):

    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Advert(models.Model):

    name = models.CharField(max_length=50)
    advertiser = models.ForeignKey(Advertiser,
                                   on_delete=models.SET_NULL,
                                   related_name="adverts",
                                   blank=True, null=True)
    fee = models.IntegerField(blank=True, null=True)
    type = models.ForeignKey(AdvertType,
                             on_delete=models.SET_NULL,
                             related_name="adverts",
                             blank=True, null=True)

    # For starred super/invewarp/pension
    platform_template = models.ForeignKey(PlatformNames,
                                          on_delete=models.SET_NULL,
                                          related_name="adverts",
                                          blank=True, null=True)
    # For starred investment
    investment_template = models.ForeignKey(InvestmentName,
                                            on_delete=models.SET_NULL,
                                            related_name="adverts",
                                            blank=True, null=True)
    # For starred portfolio
    portfolio_template = models.ForeignKey(Portfolio,
                                           on_delete=models.SET_NULL,
                                           related_name="adverts",
                                           blank=True, null=True)
    # Day the ad starts, start_date INCLUSIVE
    start_date = models.DateField()
    # Day the ad ends, end_date INCLUSIVE
    end_date = models.DateField()

    # Toggles whether the starred platform is shown in the "alternative" column
    show_in_alternative = models.BooleanField(default=True)

    # These items should be handled by google ad manager, but are here for dev
    # purposes.
    link = models.CharField(max_length=50)
    image = models.ImageField(blank=True)

    @property
    def platform_name(self):
        if self.platform_template:
            return self.platform_template.name
        else:
            return None

    @property
    def investment_name(self):
        if self.investment_template:
            return self.investment_template.name
        else:
            return None

    def __str__(self):
        return self.name
