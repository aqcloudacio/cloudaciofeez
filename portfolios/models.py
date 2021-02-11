from django.db import models
from django.shortcuts import get_list_or_404

from django.db.models import Sum
from platforms.models import Platform, PlatformNames

from investments.models import AssetAllocation, InvestmentName


class Portfolio(models.Model):
    '''
    There may be a need for a grouping of portfolios. For example,
    if a user had a model portfolio that was used in a MyNorth platform, that
    portfolio may have to be split into multiple parts and the parts applied to
    different fee tiers of myNorth. This is an edge case but not unreasonable.
    Could default to a single portfolio grouping.
    '''

    name = models.CharField(max_length=300)
    platform = models.ForeignKey(Platform,
                                 on_delete=models.CASCADE,
                                 related_name="portfolios",
                                 blank=True, null=True)
    auto_created = models.BooleanField(default=True)
    template = models.BooleanField(default=False)

    # For portfolios that are entered/created by ProductRex
    # For example, if a portfolio manager has us enter their portfolios to share
    # with the user base
    master_template = models.BooleanField(default=False)

    # Note this field is only really required for model portfolios.
    allowed_users = models.ManyToManyField("users.User",
                                           related_name="allowed_portfolios",
                                           blank=True)

    # Used to limit the platforms that a model portfolio is visible to. If
    # blank, the portfolio will be visibile on all platforms. 
    allowed_platforms = models.ManyToManyField(PlatformNames,
                                               related_name="allowed_portfolios",
                                               blank=True)

    # Total value of the model portfolio when entered by user.
    model_value = models.PositiveIntegerField(blank=True, null=True)
    template_id = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('-auto_created',)
        # constraints = [
        #     models.UniqueConstraint(fields=['platform'],
        #                             condition=Q(auto_created=True),
        #                             name='unique_platform_default')
        # ]
    @property
    def total_amount(self):
        if self.investments.exists():
            return self.investments.aggregate(Sum('amount'))["amount__sum"]
        else:
            return 0

    @property
    def total_inv_fees(self):
        if self.investments.exists():
            investments = self.investments.all()
            fees_total = 0
            for investment in investments:
                fees_total += investment.investment_fee_dollar
            return fees_total

    @property
    def total_aa(self):
        if self.investments.assetallocations.exists():
            # NOTE: THIS COULD BE MADE FASTER BY LINKING EACH ASSET ALLOCATION
            # OBJECT TO A PORTFOLIO. THEN ONLY ONE DATABASE CALL WOULD BE REQUIRED.
            # E.G. get_list_or_404(AssetAllocation, portfolio=self)

            # Gets all the investments linked to this portfolio and a list of
            # all the asset allocation names (names only)
            investments = self.investments.all()
            aa_dict = {}

            # Loops through each investment in the portfolio and retrieves a list
            # of asset allocation objects assocated with it.

            for investment in investments:
                aa_objs = get_list_or_404(AssetAllocation, investment=investment)

            # Loops through each aa item an adds it to the dictionary if it does
            # not exist as a key. If it does, the aa amount is added to the
            # existing key.

                for aa_item in aa_objs:
                    name = aa_item.name.name
                    if name in aa_dict:
                        aa_dict[name] += aa_item.aa_dollar
                    else:
                        aa_dict[name] = aa_item.aa_dollar
            return aa_dict

    @property
    def total_aa_perc(self):
        if self.total_aa:
            dict = self.total_aa
            for key, value in dict.items():
                dict[key] = value/self.total_amount
            return dict

    def __str__(self):
        return self.name


class ModelInvestment(models.Model):

    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE,
                                  related_name="model_investments")
    investment_name = models.ForeignKey(InvestmentName,
                                        on_delete=models.CASCADE,
                                        related_name="model_investments")
    percentage = models.DecimalField(max_digits=7,
                                     decimal_places=6,
                                     blank=True, null=True)

    class Meta:
        ordering = ('investment_name',)

    def __str__(self):
        return self.investment_name.name
