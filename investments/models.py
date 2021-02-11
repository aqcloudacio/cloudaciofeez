from django.db import models
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404

from riskprofiles.models import RiskProfileAAName


class InvestmentClass(models.Model):

    name = models.CharField(max_length=50)
    listed = models.BooleanField(default=False)  # Listed equities, that is.

    CATEGORY_CHOICES = [
        ("MF", "Managed Fund",),
        ("MA", "Managed Account",),
        ("LISTED", "Australian Listed Asset",),
        ("OTHER", "Other Asset"),
    ]
    category = models.CharField(max_length=100,
                                choices=CATEGORY_CHOICES,
                                blank=True, null=True)
    # INVESTMENT_CHOICES = [
    #     ("MF", "Managed Fund"),
    #     ("ASX", "Australian Listed Share"),
    #     ("ETF", "Australian Listed ETF"),
    #     ("SF", "Super Fund Investment"),
    #     ("MA", "Managed Account"),
    #     ("IS", "International Share"),
    #     ("LIC", "Listed Investment Company"),
    #     ("P", "Property"),
    #     ("ALT", "Alternative Investment"),
    #     ("CASH", "Cash")
    #     ("TD", "Term Deposit")
    #     ("OTHER", "Other Asset")
    # ]
    def __str__(self):
        if self.name:
            return self.name
        else:
            return ''


class InvestmentName(models.Model):
    """
    Stores the names of investments. Used to select investments for duplication
    and maintain a unique set of names.
    """
    name = models.CharField(max_length=300)
    # Platform field is only for investments that are EXCLUSIVE to a
    # platform, for example, industry funds.
    platform = models.ForeignKey("platforms.PlatformNames",
                                 on_delete=models.SET_NULL,
                                 related_name="investments",
                                 blank=True, null=True)
    # Only admin/template manager can edit these fields
    code = models.CharField(max_length=10, blank=True, null=True)

    @property
    def investment_class(self):
        try:
            investment_template = get_object_or_404(Investment,
                                                    name=self,
                                                    template=True)
            if investment_template.investment_class:
                return investment_template.investment_class.category
            elif self.platform:
                # Don't really want these two hard coded. Options?
                return "SF"
            else:
                return "OTHER"
        except Exception as e:
            print(self, " error: ", e, "in investment_class property")

    def __str__(self):
        if self.platform:
            return self.name+' - '+str(self.platform)
        else:
            return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'platform'],
                                    name='unique_investment_name')
        ]

    @property
    def linked_inv(self):
        '''
        Returns the investment template instance linked to this investment name
        '''
        try:
            template_inv = get_object_or_404(Investment,
                                             name=self,
                                             template=True)
            return template_inv.id
        except Exception as e:
            print(e)


    @property
    def extended_name(self):
        return str(self)


class Investment(models.Model):

    name = models.ForeignKey(InvestmentName,
                             on_delete=models.CASCADE,
                             related_name="investments",
                             blank=True, null=True)
    custom_name = models.CharField(max_length=200,
                                   blank=True, null=True)
    portfolio = models.ForeignKey("portfolios.Portfolio",
                                  on_delete=models.SET_NULL,
                                  related_name="investments",
                                  blank=True, null=True)
    platform = models.ForeignKey("platforms.Platform",
                                 on_delete=models.CASCADE,
                                 related_name="investments",
                                 blank=True, null=True)
    platform_fee_group = models.ForeignKey("platforms.PlatformFees",
                                           on_delete=models.CASCADE,
                                           related_name="investments",
                                           blank=True, null=True)
    investment_class = models.ForeignKey(InvestmentClass,
                                         on_delete=models.SET_NULL,
                                         related_name="investments",
                                         blank=True, null=True)
    amount = models.DecimalField(max_digits=9,
                                 decimal_places=2,
                                 default=0, blank=True)

    edited = models.BooleanField(default=False)
    template = models.BooleanField(default=False)

    _investment_fee = models.DecimalField(max_digits=7,
                                          decimal_places=6,
                                          default=0,
                                          blank=True)
    buy_spread = models.DecimalField(max_digits=7,
                                     decimal_places=6,
                                     default=0,
                                     blank=True)
    sell_spread = models.DecimalField(max_digits=7,
                                      default=0,
                                      decimal_places=6,
                                      blank=True)
    cash = models.BooleanField(default=False)
    TD = models.BooleanField(default=False)

    # Used to clear all existing asset allocations for this investment.
    clear_aa = models.BooleanField(default=False)

    # Used to override the fee group auto-allocation signal when the user
    # manually changes a fee group.

    override_fee_group = models.BooleanField(default=False)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'],
                                    condition=Q(template=True),
                                    name='unique_template_name')
        ]

    @property
    def status(self):
        '''
        Returns the status of the investment:
        buy = existing investment being increased
        sell = existing invesmment being decreased
        hold = existing investment being retained

        rebalanced = existing investment in current platform (ignored)
        new = new investment in rec platform
        old = old investment in current platform
        alt = any investment in alt platform
        '''
        if self.platform.get_source_platforms():
            for i in self.platform.investment_buys():
                if i[0].name == self.name:
                    return "buy"
            for i in self.platform.investment_sells():
                if i[0].name == self.name:
                    return "sell"
            for i in self.platform.investment_holds():
                if i[0].name == self.name:
                    return "hold"
        else:
            if self.platform.get_destination_platforms():
                return "rebalanced"
            else:
                if self.platform.status == "Recommended":
                    return "new"
                elif self.platform.status == "Current":
                    return "old"
                elif self.platform.status == "Alternative":
                    return "alt"

    @property
    def transaction(self):
        '''
        Returns the transaction (change in value) for the investment.
        '''
        if self.amount:
            if self.platform.get_source_platforms():
                for i in self.platform.investment_changes():
                    if i[0].name == self.name:
                        return i[1]
                else:
                    return 0
            else:
                if self.platform.get_destination_platforms():
                    return -self.amount
                else:
                    return self.amount
        else:
            return 0

    @property
    def cur_value(self):
        if self.status == "new":
            return 0
        elif self.status == "old":
            return self.amount
        elif self.status == "hold":
            return self.amount
        elif self.status == "buy":
            return self.amount - self.transaction
        elif self.status == "sell":
            return self.amount - self.transaction
        elif self.status == "rebalanced":
            return self.amount

    @property
    def rec_value(self):

        if self.status == "old":
            return 0
        elif self.status == "rebalanced":
            return 0
        else:
            return self.amount

    @property
    def allocation(self):
        if self.amount:
            return self.amount / self.platform.platform_total

    @property
    def investment_fee(self):
        '''
        If the investment is cash and no fee is present, return the cash fee
        from the assigned platform. Can be used in conjunction with generic
        "cash account" - i.e. unbranded/generic.
        '''
        if self._investment_fee > 0:
            return self._investment_fee
        else:
            if self.cash and self.platform:
                return self.platform.cash_fee
            else:
                return self._investment_fee

    @property
    def investment_fee_dollar(self):
        if self.amount and self.investment_fee:
            return self.amount*self.investment_fee
        else:
            return 0

    def __str__(self):
        if self.name:
            return self.name.name
        else:
            return self.custom_name


class AssetAllocationName(models.Model):

    '''
    These names are designed to be exact matches from product providers and
    other collection methods. This list will grow over time.

    Each item in this list MUST be linked to a field from the template list of
    "RiskProfileAAName"s. It can even be linked to more than one
    RiskProfileAAName, for example: "Fixed Interest" could be linked to both
    "Australian Fixed Interest" and "International Fixed Interest". If this
    occurs, then the actual % allocation will be split evenly between the
    linked RiskProfileAANames. In the example above, this means that 50% would
    go to each instance. If there were three links, it would be 33%, etc.

    '''

    name = models.CharField(max_length=50)
    rp_aaname_link = models.ManyToManyField(RiskProfileAAName,
                                            related_name="aa_links",
                                            blank=True)

    def __str__(self):
        return self.name

    # Australian Cash
    # International Cash
    # Australian Fixed Interest
    # International Fixed Interest
    # Australian Equities
    # International Equities
    # Australian Listed Property
    # International Listed Property
    # Direct Property
    # Infrastructure
    # Alternatives
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'],
                                    name='unique_aa_name')
        ]


class AssetAllocation(models.Model):
    '''
    Each asset allocation instance is linked to a single investment instance.
    '''

    name = models.ForeignKey(AssetAllocationName,
                             on_delete=models.CASCADE,
                             related_name="asset_allocations",
                             blank=True, null=True)
    percentage = models.DecimalField(max_digits=7,
                                     decimal_places=6,
                                     default=0)
    investment = models.ForeignKey(Investment,
                                   on_delete=models.CASCADE,
                                   related_name="asset_allocations")

    # This is only for the AA of user-made custom investments.
    rp_name_id = models.ForeignKey(RiskProfileAAName,
                                   on_delete=models.CASCADE,
                                   related_name="asset_allocations",
                                   blank=True, null=True)

    @property
    def aa_dollar(self):
        '''
        Returns the amount of $ allocated to this asset allocation, divided by
        the number of risk profile names it is linked to.

        So if an asset allocation is linked to 2 names, it will be divided in 2
        both names will be printed on the front end so will be correct.
        '''
        if self.investment.amount:
            num_links = self.name.rp_aaname_link.all().count()
            # In case the aaname is not yet assigned to an rpaaname
            if not num_links:
                num_links = 1
            return ((self.investment.amount*self.percentage) / num_links)
        else:
            return 0

    @property
    def platform_percentage(self):
        if self.investment.amount:
            platform_total = self.investment.platform.platform_total
            platform_percentage = self.investment.amount / platform_total
            return platform_percentage*self.percentage
        else:
            return 0

    def __str__(self):
        return self.name.name


class NABInvestment(models.Model):
    """
    Stores the names of NAB Group investment managers. These are used to
    identify investments owned by NAB Group when calculating MLC Wrap admin fee
    """
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name
