from django.db import models
from django.db.models.query_utils import Q
from django.shortcuts import get_list_or_404
from django.db.models import Sum
from decimal import Decimal

from scenarios.models import Scenario
from investments.models import (Investment, NABInvestment, InvestmentName,
                                InvestmentClass)


class PlatformFamilyGroups(models.Model):
    """
    Model is for sole purpose of storing the family fee link descriptions.
    """
    id = models.AutoField(primary_key=True, editable=False)
    description = models.CharField(max_length=300, unique=True,
                                   blank=True, null=True)

    def __str__(self):
        return self.description


class PlatformNames(models.Model):
    """
    Stores the names of platforms. Used to select platforms for duplication
    and maintain a unique set of names.
    """
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=300, unique=True)
    USI = models.CharField(max_length=20, blank=True, null=True)
    ARSN = models.CharField(max_length=20, blank=True, null=True)
    # If the investments are identical to another platform (e.g. industry super
    # super/pension platforms that shares investments)
    investment_owner = models.ForeignKey('self', null=True, blank=True,
                                         related_name="investment_copiers",
                                         on_delete=models.SET_NULL)
    # If the fees are identical to another platform (e.g. wrap super/pension).
    # The copier will take fees from the owner.
    fee_owner = models.ForeignKey('self', null=True, blank=True,
                                  related_name="fee_copiers",
                                  on_delete=models.SET_NULL)
    # Direct link to the PDS - for internal use only.
    direct_pds_link = models.URLField(blank=True, null=True, max_length=500)

    @property
    def PDS_link(self):
        if self.fee_scrape_settings.exists():
            return self.fee_scrape_settings.all()[0].root
        else:
            return None

    @property
    def linked_investments(self):
        if self.investments.exists():
            return True
        else:
            return False


    def __str__(self):
        return self.name


class Platform(models.Model):

    id = models.AutoField(editable=False, primary_key=True)
    scenario = models.ForeignKey(Scenario,
                                 on_delete=models.CASCADE,
                                 related_name="platforms",
                                 blank=True, null=True)
    edited = models.BooleanField(default=False)
    template = models.BooleanField(default=False)

    name = models.ForeignKey(PlatformNames,
                             on_delete=models.CASCADE,
                             related_name="platforms",
                             blank=True, null=True)
    custom_name = models.CharField(max_length=100,
                                   null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)

    cloned = models.BooleanField(default=False)
    clone_link = models.PositiveIntegerField(null=True, blank=True)

    # Used to refresh platform data only. Will always be false in DB
    refresh = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ("Current", "Current"),
        ("Recommended", "Recommended"),
        ("Alternative", "Alternative"),
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES,
                              blank=True, null=True)

    TYPE_CHOICES = [
        ('Accumulation', "Superannuation - Accumulation"),
        ('Pension', "Superannuation - Pension"),
        ('Defined Benefit', "Superannuation - Defined Benefit"),
        ('Investment', "Investment"),
        ('SMSF - Accumulation', "Self Managed Super Fund - Accumulation"),
        ('SMSF - Pension', "Self Managed Super Fund - Pension"),
    ]
    platform_type = models.CharField(max_length=100,
                                     choices=TYPE_CHOICES,
                                     blank=True, null=True)
    notes = models.CharField(max_length=400, blank=True)

    #  PDS Fields
    PDS_date = models.DateField(blank=True, null=True)
    PDS_version = models.CharField(max_length=50, blank=True)

    #  Other fields for scrape
    AA_link = models.URLField(blank=True, null=True)
    ICR_link = models.URLField(blank=True, null=True)
    ###
    # Do I want to allow direct download of PDSs that do not have a URL link?
    ###
    create_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    last_checked = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True)

    # Platform-level fees.
    platform_adviser_fee = models.DecimalField(max_digits=7,
                                      decimal_places=2,
                                      null=True, default=0)
    platform_adviser_fee_percentage = models.DecimalField(max_digits=7,
                                                 decimal_places=6,
                                                 null=True, default=0)
    cash_fee = models.DecimalField(max_digits=7,
                                   decimal_places=6,
                                   blank=True, null=True)
    switch_fee = models.DecimalField(max_digits=6,
                                     decimal_places=2,
                                     default=0,
                                     blank=True, null=True)
    #  If a platform has multiple fee structures, but only one fixed admin fee
    #  will be charged, shared_admin_fee should = True
    shared_admin_fee = models.BooleanField(default=True)

    # If there is "splitting" of platform fee groupings. That is, can you have
    # multiple fee groupings for one account.
    single_fee_group = models.BooleanField(default=True)

    # Fee linking details.
    ALLOWED_LINKS = [
        ("None", "No fee linking"),
        ("Personal", "Links to own accounts only"),
        ("Family", "Links to own direct family only")
    ]
    allowed_fee_link = models.CharField(max_length=20,
                                        choices=ALLOWED_LINKS,
                                        default="None")
    manual_linking_adjustment = models.PositiveIntegerField(default=0)
    # maximum_linked_accounts = models.PositiveIntegerField(default=0)
    LINK_TYPES = [
        ("None", "No change in admin fee"),
        ("Combined", "Admin fee calculated on combined balance"),
        ("Reduction", "Admin fee reduced by fixed amount")
    ]
    fee_link_type = models.CharField(max_length=20,
                                     choices=LINK_TYPES,
                                     default="None")

    #  For "Reduction" type fee links only.
    # Note that this is the amount to take off the admin fee %, not the
    # amount that the admin fee is reduced.
    # So if the reduction is 0.1% on a total fee of 1%, the value should be
    # 0.1%, NOT 10%.
    admin_fee_linking_reduction = models.DecimalField(max_digits=7,
                                                      decimal_places=6,
                                                      blank=True,
                                                      null=True)

    # Fee-linked platforms
    fee_link_group = models.ForeignKey(PlatformFamilyGroups,
                                       on_delete=models.CASCADE,
                                       related_name="platforms",
                                       null=True, blank=True)

    # Fee modifiers
    # The fixed admin fee is not charged for balances above this level
    admin_fee_cutoff = models.DecimalField(max_digits=9,
                                           decimal_places=2,
                                           blank=True, null=True)
    white_label_admin_fee = models.BooleanField(default=False)
    # The maximum ORR Levy payable
    ORR_levy_cap = models.DecimalField(max_digits=6,
                                       decimal_places=2,
                                       blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'],
                                    condition=Q(template=True),
                                    name='unique_platform_template')
        ]

    @property
    def platform_total(self):
        portfolios = self.portfolios.all()
        platform_total = 0
        for portfolio in [p for p in portfolios if p.total_amount is not None]:
            platform_total += portfolio.total_amount
        return platform_total

    @property
    def platform_modified_total(self):
        '''
        Sum of the platform fee group's modified totals. This is the sum of
        all investments less excluded investments (if applicable), for example,
        cash and Term Deposits.
        Used to get the total linked platform balances.
        '''
        return sum(fee.modified_total for fee in self.fees.all()
                  if fee.modified_total is not None)

    @property
    def platform_total_fees(self):
        try:
            if self.active_fee_groups:
                platform_total_fees = 0
                for fee_group in self.active_fee_groups:
                    platform_total_fees += fee_group.platform_fee_total_fees
                return platform_total_fees + self.total_adviser_fees
            else:
                return 0
        except Exception as e:
            print(e)

    @property
    def platform_total_fees_ex_adviser(self):
        return self.platform_total_fees - self.total_adviser_fees

    @property
    def platform_investments_string(self):
        if self.investments.exists():
            investments = [str(investment) for investment in self.investments.all()]
            return ", ".join(investments)
        else:
            return None

    @property
    def platform_cur_value(self):
            invs = list(self.investments.all()) + self.full_selldowns
            return sum(inv.cur_value for inv in invs)

    @property
    def platform_transaction(self):
            invs = list(self.investments.all()) + self.full_selldowns
            return sum(inv.transaction for inv in invs)

    @property
    def platform_rec_value(self):
            invs = list(self.investments.all()) + self.full_selldowns
            return sum(inv.rec_value for inv in invs)

    def get_source_platforms(self):
        '''
        Returns platforms that have the same account number and a status of
        "current". They are the "starting position" for rebalances.
        '''
        if self.account_number:
            try:
                source_platforms = get_list_or_404(Platform,
                                                ~Q(id=self.id),
                                                account_number=self.account_number,
                                                status="Current")
                return source_platforms

            except Exception:
                return None


    def as_dict(self):
        return dict((f.name, getattr(self, f.name)) for f in self._meta.fields)

    def get_destination_platforms(self):
        '''
        Returns whether there are platforms that have the same account number
        and a status NOT == "current".
        That is, whether this platform is being rebalanced.
        '''
        if self.account_number:
            try:
                destination_platforms = get_list_or_404(Platform,
                                                ~Q(id=self.id),
                                                ~Q(status="Current"),
                                                account_number=self.account_number)
                return destination_platforms

            except Exception as e:
                pass
                # print(e)

    def get_source_investments(self, platforms):
        '''
        Returns platforms that have the same account number and a status of
        "current". They are the "starting position" for rebalances.
        '''
        try:
            source_investments = []
            for platform in platforms:
                source_investments.extend(get_list_or_404(Investment,
                                                          platform=platform,
                                                          cash=False))
            return source_investments

        except Exception as e:
            pass
            # print(e)

    def build_rebalance_tuples(self, source_investments, destination_investments):

        sells = []
        buys = []
        holds = []

        for src_inv in source_investments:
            for dest_inv in destination_investments:

                if src_inv.name == dest_inv.name:
                    tx = dest_inv.amount - src_inv.amount

                    # If new > current, add item to buys
                    if dest_inv.amount > src_inv.amount:
                        buys.append((dest_inv,tx))
                        destination_investments.remove(dest_inv)
                        break

                    # If new > current, add item to sells
                    elif dest_inv.amount < src_inv.amount:
                        sells.append((dest_inv,tx))
                        destination_investments.remove(dest_inv)
                        break

                    # Else add item to holds
                    else:
                        holds.append((dest_inv,tx))
                        destination_investments.remove(dest_inv)
                        break

            # If item does not match any condition, it must not exis
            # and therefore must have been sold.
            else:
                sells.append((src_inv, -src_inv.amount))

        # Any investments remaining in this list must be new, so are
        # added to the buys list.
        for inv in destination_investments:
            buys.append((inv, inv.amount))

        return buys, sells, holds


    def investment_transactions(self, type):
        '''

        '''
        investments = list(self.investments.all())
        investments = [i for i in investments if i.amount]

        sells = []
        buys = []
        holds = []

        if self.status != "Current":
            source_platforms = self.get_source_platforms()
            # If platform is alternate or recommended, check if it is linked
            # to a "current" platform (i.e. is a rebalance).
            if source_platforms:
                source_investments = self.get_source_investments(source_platforms)

                # If it is, and there are investments, find the buys/sells/holds
                if source_investments:
                    buys, sells, holds = self.build_rebalance_tuples(source_investments, investments)

            else:
                # If it is not linked to a "current" platform (i.e. it is new)
                # then add all investments to the "buys"
                for inv in investments:
                    buys.append((inv, inv.amount))

        else:
            # If it is a current platform, check if there is a "destination"
            # platform, that is, it is being rebalanced.
            destination_platforms = self.get_destination_platforms()

            if not destination_platforms:
                # If there is no destination platform, add all investments
                # to the sells list
                for inv in investments:
                    sells.append((inv, -inv.amount))

        if type == "buys":
            return buys
        elif type == "sells":
            return sells
        elif type == "changes":
            return sells+buys
        elif type == "holds":
            return holds


    def investment_buys(self):
        return self.investment_transactions("buys")

    def investment_sells(self):
        return self.investment_transactions("sells")

    def investment_holds(self):
        return self.investment_transactions("holds")

    def investment_changes(self):
        return self.investment_transactions("changes")


    @property
    def full_selldowns(self):

        source_platforms = self.get_source_platforms()

        if source_platforms:
            source_investments = self.get_source_investments(source_platforms)

            if source_investments:
                for inv in self.investments.all():
                    for src_inv in source_investments:
                        if src_inv.name.id == inv.name.id:
                            source_investments.pop(source_investments.index(src_inv))
                            break
            return source_investments

        else:
            return []

    @property
    def switch_fees_total(self):
        if self.switch_fee:
            changes = self.investment_changes()
            if changes:
                num_changes = len(changes)
                return num_changes*self.switch_fee
            else:
                return 0
        else:
            return 0

    @property
    def buy_sell_spread_total(self):
        buy_spread_total = 0
        sell_spread_total = 0
        buys = self.investment_buys()
        sells = self.investment_sells()

        if buys:
            print(buys)
            buy_spread_total = sum([(tx * inv.buy_spread) for inv,tx in buys])

        if sells:
            sell_spread_total = sum([abs(tx * inv.sell_spread) for inv,tx in sells])

        return buy_spread_total + sell_spread_total

    @property
    def linked_platforms(self):
        result = []
        if self.fee_link_group:
            try:
                links = get_list_or_404(Platform,
                                        ~Q(id=self.id),
                                        fee_link_group=self.fee_link_group,
                                        scenario=self.scenario,
                                        status=self.status)
                for link in links:
                    result.append((str(link), (link.platform_total + link.manual_linking_adjustment)))

                if self.manual_linking_adjustment > 0:
                    result.append(("Manual Adjustment", self.manual_linking_adjustment))

                return result

            except Exception as e:
                pass
                # print(e)
        else:
            return None

    @property
    def platform_adviser_fee_percentage_calculated(self):
        if self.platform_adviser_fee_percentage:
            return self.platform_adviser_fee_percentage*self.platform_total
        else:
            return 0

    @property
    def total_adviser_fees(self):
        if self.platform_adviser_fee or self.platform_adviser_fee_percentage_calculated:
            return self.platform_adviser_fee + self.platform_adviser_fee_percentage_calculated
        else:
            return 0

    # @property
    # def consolidated_balance(self):
    #     return sum(p.platform_total for p in self.scenario.platforms.all())


    '''
    These properties are aggregations from platform fee groupings.
    Calculated here for ease of reference.

    NOTE: The naming syntax for these properties is:
    "'platform_' + <name of platform_fee field>". This must be used for dynamic
    report production.
    '''
    @property
    def active_fee_groups(self):
        '''
        Returns a list of linked fee groups that have value > 0
        '''
        if self.fees.exists():
            return [f for f in self.fees.all() if f.platform_fee_total > 0]
        else:
            return None

    def sum_fee_prop(self, prop):
        '''
        Utility function used to sum fields from active fee groups (fee groups
        with total val > 0)
        '''
        if self.active_fee_groups:
            return sum(getattr(fee,prop) for fee in self.active_fee_groups
                       if getattr(fee,prop) is not None)
        else:
            return 0

    @property
    def platform_sliding_admin_fee(self):
        return self.sum_fee_prop('sliding_admin_fee')

    @property
    def platform_admin_fee_dollar_calculated(self):
        '''
        If shared admin fee is true, the largest flat admin fee will be used
        If not, all flat admin fees will be summed.
        '''
        fee = 0
        if self.shared_admin_fee:
            fee_list = [fee.admin_fee_dollar_calculated for fee in self.active_fee_groups
                        if fee.admin_fee_dollar_calculated is not None]
            if fee_list:
                fee = max(fee_list)
        else:
            fee = self.sum_fee_prop('admin_fee_dollar_calculated')

        return self.apply_admin_fee_cutoff(fee)

    def apply_admin_fee_cutoff(self, fee):
        '''
        Applied at the platform level (may have multiple fee structures)
        '''
        if self.admin_fee_cutoff is not None:
            if self.platform_total < self.admin_fee_cutoff:
                return fee
            else:
                return 0
        else:
            return fee

    @property
    def platform_admin_fee_percentage_calculated(self):
        return self.sum_fee_prop('admin_fee_percentage_calculated')

    @property
    def platform_expense_recovery_dollar(self):
        return self.sum_fee_prop('expense_recovery_dollar')

    @property
    def platform_expense_recovery_percentage_calculated(self):
        return self.sum_fee_prop('expense_recovery_percentage_calculated')

    @property
    def platform_ORR_levy_calculated(self):
        '''
        Sums the total ORR levy for the underlying fee platforms. Once summed,
        the ORR cap is reapplied in case there are multiple fee levels with
        the same max ORR payable (max ORR only charged once per platform)
        '''
        if self.active_fee_groups:
            ORR = sum(f.ORR_levy_calculated for f in self.active_fee_groups
                      if f.ORR_levy_calculated is not None)

            ORR_levy_cap = self.ORR_levy_cap

            if ORR_levy_cap:
                return min(ORR, ORR_levy_cap)
            else:
                return ORR
        else:
            return 0

    @property
    def platform_fund_accounting_fee_dollar(self):
        return self.sum_fee_prop('fund_accounting_fee_dollar')

    @property
    def platform_fund_accounting_fee_percentage_calculated(self):
        return self.sum_fee_prop('fund_accounting_fee_percentage_calculated')

    @property
    def platform_trustee_fee_calculated(self):
        return self.sum_fee_prop('trustee_fee_calculated')

    @property
    def platform_issuer_fee_calculated(self):
        return self.sum_fee_prop('issuer_fee_calculated')

    @property
    def platform_sma_admin_fee(self):
        return self.sum_fee_prop('sma_admin_fee')

    @property
    def platform_investment_fee(self):
        return self.sum_fee_prop('investment_fee')

    @property
    def platform_low_balance_refund(self):
        return self.sum_fee_prop('low_balance_refund')

    @property
    def ongoing_display_list(self):
        '''
        These fields are used in document generatation.
        Position 0 is the exact name of the platform_fee field to total.
        Position 1 is the default friendly name.
        '''
        return [
            ("investment_fee", "Investment Fee"),
            ("sliding_admin_fee", "Sliding Admin Fee"),
            ("admin_fee_dollar_calculated", "Admin Fee (Flat)"),
            ("admin_fee_percentage_calculated", "Admin Fee (Floating)"),
            ("expense_recovery_dollar", "Expense Recovery Fee (Flat)"),
            ("expense_recovery_percentage_calculated", "Expense Recovery Fee (Floating)"),
            ("ORR_levy_calculated", "ORR Levy"),
            ("fund_accounting_fee_dollar", "Fund Accounting Fee (Flat)"),
            ("fund_accounting_fee_percentage_calculated", "Fund Accounting Fee (Floating)"),
            ("trustee_fee_calculated", "Trustee Fee"),
            ("issuer_fee_calculated", "Issuer Fee"),
            ("sma_admin_fee", "SMA Admin Fee"),
            ("low_balance_refund", "Low Balance Refund"),
        ]

    @property
    def adviser_fee_list(self):
        '''
        These fields are used in document generatation.
        Position 0 is the exact name of the adviser fee field to total.
        Position 1 is the default friendly name.
        '''
        return [
            ("adviser_fee", "Adviser Fee (Flat)"),
            ("adviser_fee_percentage_calculated", "Adviser Fee (Floating)"),
        ]

    @property
    def str_name(self):
        '''
        Pretty printed name (same as __str__) for frontend
        '''
        if self.custom_name:
            return self.custom_name
        elif self.name:
            return self.name.name
        else:
            return ''


    def __str__(self):
        if self.name:
            return self.name.name
        elif self.custom_name:
            return self.custom_name
        else:
            return ''


class PlatformFees(models.Model):
    """
    This table stores "fixed" style fees and associated info. Can have multiple
    fee structures for each platform.

    When the fees for a Platform are shown, the PlatformFee instances linked
    to that Platform should be aggregated.
    """
    id = models.AutoField(primary_key=True, editable=False)
    edited = models.BooleanField(default=False)
    platform = models.ForeignKey(Platform,
                                 on_delete=models.CASCADE,
                                 related_name="fees")

    # Name of the fee structure as defined by platform provider.
    description = models.CharField(max_length=100)

    # The "order" of the fee grouping under the platform.
    # Most restrictive (usually cheapest) should be lowest, "full" menus should
    # be highest. Defaulted to 0, as most platforms only have one fee group.
    fee_group_order = models.IntegerField(default=0)

    # If platform fee is limited to a particular AFSL.
    AFSL_limitation = models.ForeignKey("users.AFSL",
                                        on_delete=models.SET_NULL,
                                        related_name="platform_fees",
                                        blank=True, null=True)

    # Type of percentage-based admin fee structure.
    STRUCTURE_CHOICES = [
        ('Flat percentange', "Flat percentage admin fee"),
        ('Tiered', "Tiered admin fee"),
        ('Tiered per asset', "Tiered admin fee per asset"),
        ('Staggered', "Staggered admin fee"),
        ('MLC Wrap', "MLC Wrap custom admin fee")
    ]
    admin_fee_structure = models.CharField(max_length=100,
                                           choices=STRUCTURE_CHOICES,
                                           blank=True)

    # "Fixed" style fees
    # Note that these should be ANNUALISED
    admin_fee_dollar = models.DecimalField(max_digits=6,
                                           decimal_places=2,
                                           default=0, null=True)
    admin_fee_percentage = models.DecimalField(max_digits=7,
                                               decimal_places=6,
                                               default=0, null=True)
    admin_fee_rebate = models.DecimalField(max_digits=7,
                                           decimal_places=6,
                                           default=0)
    expense_recovery_dollar = models.DecimalField(max_digits=6,
                                                  decimal_places=2,
                                                  default=0, null=True)
    expense_recovery_percentage = models.DecimalField(max_digits=7,
                                                      decimal_places=6,
                                                      default=0, null=True)
    ORR_levy = models.DecimalField(max_digits=7,
                                   decimal_places=6,
                                   default=0)
    fund_accounting_fee_dollar = models.DecimalField(max_digits=6,
                                                     decimal_places=2,
                                                     default=0, null=True)
    fund_accounting_fee_percentage = models.DecimalField(max_digits=7,
                                                         decimal_places=6,
                                                         default=0, null=True)
    trustee_fee = models.DecimalField(max_digits=7,
                                      decimal_places=6,
                                      default=0, null=True)
    issuer_fee = models.DecimalField(max_digits=7,
                                     decimal_places=6,
                                     default=0, null=True)
    sma_admin_fee = models.DecimalField(max_digits=6,
                                        decimal_places=2,
                                        default=0, null=True)



    # Additional fund information used in fee calculations
    minimum_admin_fee = models.DecimalField(max_digits=6,
                                            decimal_places=2,
                                            default=0)
    maximum_admin_fee = models.DecimalField(max_digits=8,
                                            decimal_places=2,
                                            default=0, null=True)
    minimum_total_fee = models.DecimalField(max_digits=6,
                                            decimal_places=2,
                                            default=0)
    maximum_total_fee = models.DecimalField(max_digits=8,
                                            decimal_places=2,
                                            default=0, null=True)

    # Fee exclusions for administration fee
    FEE_EXCLUSIONS = [
        ("Cash", "Cash only excluded"),
        ("TD", "Term deposits only excluded"),
        ("Cash and TD", "Cash and TDs excluded"),
    ]
    admin_fee_exclusions = models.CharField(max_length=50,
                                            choices=FEE_EXCLUSIONS,
                                            blank=True)

    # Optional list of investments that are allowed on the fee structure.
    # May not be widely used but MUST be used for platforms that have varying
    # fee structures depending on the investment (e.g. MyNorth)
    # This is actually a better way of handling MLC Wrap too. May change
    # MLC Wrap calculations in the future.
    # NOTE this must be an APIR, ASX, or "OTHER" code.

    #note - assigned in the investment model signals on instantiation.
    allowed_investments = models.ManyToManyField(InvestmentName,
                                                 related_name="fee_structures",
                                                 blank=True)

    # Optional list of investment classes that MUST belong to the instance.
    # E.g. Asgard eWrap Investment listed securities
    allowed_investment_classes = models.ManyToManyField(InvestmentClass,
                                                        related_name="fee_groups",
                                                        blank=True)


    class Meta:
        ordering = ('fee_group_order',)

    @property
    def platform_fee_total(self):
        investments = self.investments.filter(platform_fee_group=self)
        platform_fee_total = 0
        for investment in investments:
            if investment.amount:
                platform_fee_total += investment.amount
        return platform_fee_total

    @property
    def ongoing_display_list(self):
        return self.platform.ongoing_display_list


    @property
    def platform_fee_total_fees(self):
        if self.platform_fee_total > 0:
            ongoing_display_list = self.ongoing_display_list
            total_fee_val = 0
            for (property, friendly) in ongoing_display_list:
                value = getattr(self,property)
                try:
                    if value:
                        total_fee_val += value
                except Exception as e:
                    pass
                    print(e)
            return total_fee_val
        else:
            return 0

    @property
    def investment_fee(self):
        '''
        Returns the sum of the investment fees for all investments in this fee
        group.
        '''
        investments = self.investments.all()

        return sum(i.investment_fee_dollar for i in investments)


    @property
    def low_balance_refund(self):
        '''
        Returns the low balance refund if applicable to this fee group.
        '''
        # Test if platform fee group falls under threshold
        if ((self.platform_fee_total < 6000) and (self.platform_fee_total > 0)
            and (self.platform.platform_type != 'Investment')):

            # Yes, this is a dupe of the platform_fee_total_fees prop,
            # because if I call that prop from this one, it is recursive
            ongoing_display_list = [x for x in self.ongoing_display_list if x != (("low_balance_refund", "Low Balance Refund"))]

            total_fee_val = 0
            for (property, friendly) in ongoing_display_list:
                value = getattr(self,property)
                try:
                    if value:
                        total_fee_val += value
                except Exception as e:
                    pass
                    # print(e)

            # Test if fees are greater than 3%
            if (total_fee_val / self.platform_fee_total) > 0.03:
                max_fee = self.platform_fee_total * Decimal(0.03)
                # Return diference as refund
                return -(total_fee_val - max_fee)
            else:
                return 0
        else:
            return 0

    @property
    def admin_fee_dollar_calculated(self):
        '''
        Returns the dollar value of the flat admin fee and applies the cutoff
        (set at platform level).
        '''
        admin_fee_cutoff = self.platform.admin_fee_cutoff
        fee = self.admin_fee_dollar

        if admin_fee_cutoff:
            if admin_fee_cutoff > self.platform_fee_total:
                return fee
            else:
                return 0
        else:
            return fee


    @property
    def ORR_levy_calculated(self):
        '''
        Returns the dollar value of the ORR levy and applies the cap (set at
        platform level).

        NOTE. Does not account for there being multiple ORR levies (if
        shared_admin_fee = False). This is however handled at the platform
        level (the cap is applied to the sum of ORR levies, so is correct for
        documents.
        '''
        ORR_levy_amount = self.ORR_levy * self.platform_fee_total
        ORR_levy_cap = self.platform.ORR_levy_cap

        if ORR_levy_cap:
            return min(ORR_levy_amount, ORR_levy_cap)
        else:
            return ORR_levy_amount


    '''
    # These are all percentage-based fees converted to dollar values.
    # These are aggregated at the platform level for top-level overview.
    '''
    @property
    def admin_fee_percentage_calculated(self):
        # Subtracts percentage-based fee rebated from percentage fee.
        if self.admin_fee_percentage is not None:
            return ((self.admin_fee_percentage-self.admin_fee_rebate)
                    * self.platform_fee_total)

    @property
    def expense_recovery_percentage_calculated(self):
        if self.expense_recovery_percentage is not None:
            return self.expense_recovery_percentage*self.platform_fee_total

    @property
    def fund_accounting_fee_percentage_calculated(self):
        if self.fund_accounting_fee_percentage is not None:
            return self.fund_accounting_fee_percentage*self.platform_fee_total

    @property
    def trustee_fee_calculated(self):
        if self.trustee_fee is not None:
            return self.trustee_fee*self.platform_fee_total

    @property
    def issuer_fee_calculated(self):
        if self.issuer_fee is not None:
            return self.issuer_fee*self.platform_fee_total

    '''
    Creates sliding fees based on the applicable fee structure.
    '''
    @property
    def sliding_admin_fee(self):
        return self.get_sliding_admin_fee()

    def get_sliding_admin_fee(self, **kwargs):
        if self.admin_fee_structure and self.platform_fee_total != 0:
            fee = 0
            if self.has_thresholds():
                if self.admin_fee_structure == "Tiered":
                    fee = self.calculate_tiered_fee()
                elif self.admin_fee_structure == "Staggered":
                    fee = self.calculate_staggered_fee()
                elif self.admin_fee_structure == "Tiered per asset":
                    fee = self.calculate_tpa_fee()
                elif self.admin_fee_structure == "MLC Wrap":
                    tiered = self.calculate_tiered_fee()
                    fee = self.calculate_MLC_fee(tiered)
            else:
                return 0
            if fee:
                #Applies min or max admin fees to the calculated fee
                fee = self.apply_min_or_max(fee)

                #Applies fixed (%) fee reduction if applicable
                if self.linking_discount:
                    fee = self.apply_linking_discount(fee)

                return fee
            else:
                return 0

        else:
            return 0

    def has_thresholds(self):
        return self.tier_thresholds.exists() and self.tier_percs.exists()

    def apply_min_or_max(self, fee):
        '''
        Reduces or increases the fee passed as an argument to the min or max
        admin fee as listed in the fee instance.
        '''
        # Doesn't apply min/max to rebates.
        if fee < 0:
            return fee
        elif self.maximum_admin_fee > 0:
            return min(max(fee, self.minimum_admin_fee), self.maximum_admin_fee)
        elif self.minimum_admin_fee is not None:
            return max(fee, self.minimum_admin_fee)
        else:
            return fee

    def calculate_tiered_fee(self):
        '''
        Retrieves list of thresholds and percentages linked to the platform fee
        group. Then calculates the tiered fee based on those values and the
        total value of the platform.
        '''
        # This will bug out if there are no thresholds or percentages and the
        # fee structure is set to tiered/staggered/etc. Needs to be fixed
        try:
            thresholds = get_list_or_404(PlatformTierThresholds,
                                         platform_fee_group=self)
            percentages = get_list_or_404(PlatformTierPercs,
                                          platform_fee_group=self)

            tiered_fee = 0
            tiered_fee_percentage = 0
            remainder = 0
            modified_total = self.modified_total
            adjusted_linked_total = self.apply_linking_adjustment(modified_total)

            for threshold, percentage in zip(thresholds, percentages):
                upper_threshold = threshold.threshold
                lower_threshold = threshold.lower_threshold
                percentage = percentage.percentage

                # If the platform total (or adjusted total) is lower than
                # the current iterated threshold
                if upper_threshold <= adjusted_linked_total:
                    # Find the amount between the thresholds. This is used
                    # to calculate the fee on that bracket.
                    amt_between_thresholds = upper_threshold - lower_threshold
                    tiered_fee += amt_between_thresholds * percentage
                # If the platform total is higher than the threshold, a
                # remainder needs to be found and the percentaged based on that
                else:
                    remainder = adjusted_linked_total - lower_threshold
                    tiered_fee += remainder * percentage
                    break

            else:
                return 0

            # Gets the percentage of tiered_fee using the adjusted total
            tiered_fee_percentage = tiered_fee / adjusted_linked_total

            # Multiplies this adjusted percentage by the actual platform total
            # to get the fee for this platform.
            tiered_fee = tiered_fee_percentage * modified_total
            return tiered_fee

        except Exception as e:
            print(e)

    def calculate_staggered_fee(self):
        '''
        Staggered fees are based on the total account balance * applicable fee
        tier.
        '''
        try:
            thresholds = get_list_or_404(PlatformTierThresholds,
                                         platform_fee_group=self)
            percentages = get_list_or_404(PlatformTierPercs,
                                          platform_fee_group=self)
        except Exception as e:
            print(e)

        staggered_fee = 0
        staggered_fee_percentage = 0
        modified_total = self.modified_total
        adjusted_linked_total = self.apply_linking_adjustment(modified_total)

        for threshold, percentage in zip(thresholds, percentages):
            threshold = threshold.threshold
            percentage = percentage.percentage
            # If the threshold is greater than the total.
            # Thresholds are iterated from smallest to largest, so will break
            # at the lowest match.
            if threshold >= adjusted_linked_total:
                staggered_fee = adjusted_linked_total * percentage
                break

        # Gets the percentage of staggered_fee using the adjusted total
        staggered_fee_percentage = staggered_fee / adjusted_linked_total

        # Multiplies this adjusted percentage by the actual platform total
        # to get the fee for this platform.
        staggered_fee = staggered_fee_percentage * modified_total

        return staggered_fee

    def calculate_tpa_fee(self):
        '''
        TPA or "tiered per asset" fees are basically the same as tiered fees
        except the tier is applied to each individual investment balance.
        '''
        # NOTE: there are no "TPA" platforms that currently offer fee linking,
        # so it has not been coded.
        # This will need to be updated if this changes
        try:
            thresholds = get_list_or_404(PlatformTierThresholds,
                                         platform_fee_group=self)
            percentages = get_list_or_404(PlatformTierPercs,
                                          platform_fee_group=self)
            investments = get_list_or_404(Investment,
                                          platform_fee_group=self)
        except Exception as e:
            print(e)

        tpa_fee = 0

        for investment in investments:
            tiered_fee = 0
            for threshold, percentage in zip(thresholds, percentages):
                upper_threshold = threshold.threshold
                lower_threshold = threshold.lower_threshold
                percentage = percentage.percentage
                # If the platform total (or adjusted total) is lower than
                # the current iterated threshold
                if upper_threshold <= investment.amount:
                    # Find the amount between the thresholds. This is used
                    # to calculate the fee on that bracket.
                    amt_between_thresholds = upper_threshold - lower_threshold
                    tiered_fee += amt_between_thresholds * percentage
                else:
                    # If the platform total is higher than the threshold, a
                    # remainder needs to be found and the percentaged based on
                    # that
                    remainder = investment.amount - lower_threshold
                    tiered_fee += remainder * percentage
                    break

            tpa_fee += tiered_fee

        return tpa_fee

    def calculate_MLC_fee(self, tiered_fee):
        '''
        MLC fees are similar to tiered fees - the base part of the fee uses the
        tiered fee calculation. On top of this, they charge an additional fee
        for listed investments and investments not managed by MLC.
        These amounts (0.15% and 0.10% respectively, are hard coded below.)
        '''
        investments = get_list_or_404(Investment,
                                      platform_fee_group=self)
        NAB_managers = NABInvestment.objects.all()
        listed_investments_total = 0
        NAB_investments_total = 0
        for investment in investments:
            if investment.investment_class.listed:
                listed_investments_total += investment.amount
            for NAB_manager in NAB_managers:
                if NAB_manager.name not in investment.name.name:
                    NAB_investments_total += investment.amount
        listed_fee = int(listed_investments_total) * 0.0015
        NAB_fee = int(NAB_investments_total) * 0.0010
        total_fee = listed_fee + NAB_fee + int(tiered_fee)
        return total_fee

    @property
    def modified_total(self):
        return self.get_modified_total()

    def get_modified_total(self):
        '''
        This is used to reduce the platform total balance if the platform
        excludes cash, TD or both when calculating the sliding admin fee.
        Functions create a filtered queryset based on the platform preference
        then aggregate that queryset to provide a total amount.
        '''
        reduction_amount = 0
        try:
            if self.admin_fee_exclusions == "Cash and TD":
                reduction_amount = Investment.objects.filter(Q(cash=True)
                                                             | Q(TD=True),
                                                             platform_fee_group=self).aggregate(Sum('amount'))["amount__sum"]
            elif self.admin_fee_exclusions == "Cash":
                reduction_amount = Investment.objects.filter(cash=True,
                                                             platform_fee_group=self).aggregate(Sum('amount'))["amount__sum"]
            elif self.admin_fee_exclusions == "TD":
                reduction_amount = Investment.objects.filter(TD=True,
                                                             platform_fee_group=self).aggregate(Sum('amount'))["amount__sum"]
            else:
                pass
        except Exception as e:
            print(e)
            pass

        amount_before_reduction = self.platform_fee_total

        if reduction_amount:
            return (amount_before_reduction - reduction_amount)
        else:
            return amount_before_reduction

    def apply_linking_discount(self, fee):
        '''
        Reduces the fee by the discount amount
        '''
        discount = self.linking_discount
        return fee - (fee * discount)

    @property
    def linking_discount(self):
        '''
        If a fixed fee-link reduction applies, return it, else return false.
        '''
        if self.platform.fee_link_type == "Reduction":
            platforms = self.get_linked_platforms

            if (platforms) or (self.platform.manual_linking_adjustment > 0):
                return self.platform.admin_fee_linking_reduction

        else:
            return False

    def get_linked_platforms(self):
        '''
        Returns a list of platforms that are in the same fee link group,
        with the same scenario and have the same status. Does NOT return the
        instance itself (would duplicate its balance).
        '''
        try:
            linked = get_list_or_404(Platform,
                                     ~Q(id=self.platform.id),
                                     fee_link_group=self.platform.fee_link_group,
                                     scenario=self.platform.scenario,
                                     status=self.platform.status)
            return linked
        except Exception:
            return None

    def get_linked_balances(self, platforms):
        '''
        Iterates linked platforms and returns the sum of their modified
        balances as well as the manual linking adjustments
        '''
        total = 0
        for platform in platforms:
            total += platform.platform_modified_total
            total += platform.manual_linking_adjustment

        return total

    def apply_linking_adjustment(self, self_modifed_balance):
        '''
        Returns the total adjusted platform balance so that sliding fees can
        be modified for the purpose of fee linking. Only for "Combined"
        style fee reductions.

        Note that the total adjusted platform balance is the sum of:
         - Self modified balance  (ex cash/td if specified)
         - Linked platforms total modified balance
         - Self manual adjustment
        '''
        linked_balances = 0
        if self.platform.fee_link_group:
            # Gets the platforms that are linked to this one through a shared
            # fee_link_group, status and scenario.
            platforms = self.get_linked_platforms()

            # Will not try to retrieve balances for platforms that have no
            # links for this instance.
            # For platforms where their balances are combined to modify the tiered
            # or staggered admin fees.
            if platforms and (self.platform.fee_link_type == "Combined"):
                linked_balances = self.get_linked_balances(platforms)

                if self.platform.single_fee_group:
                    adjusted = (self_modifed_balance
                                + self.platform.manual_linking_adjustment
                                + linked_balances)
                    return adjusted
                else:
                    # DOES NOT WORK WHEN SINGLE FEE GROUP IS FALSE. DON"T KNOW
                    # WHERE TO ASSIGN THE MANUAL ADJUSTMENT. THIS IS AN EDGE
                    # CASEFOR NOW AND MAY NOT EVER EXIST.
                    return self_modifed_balance

            else:
                return self_modifed_balance
        else:
            return self_modifed_balance

    def __str__(self):
        return self.description


class PlatformTierThresholds(models.Model):
    """
    Upper limit for each fee tier
    """

    platform_fee_group = models.ForeignKey(PlatformFees,
                                           on_delete=models.CASCADE,
                                           related_name="tier_thresholds")
    threshold = models.DecimalField(max_digits=7, decimal_places=0, default=0)


    class Meta:
        ordering = ['threshold']

    @property
    def lower_threshold(self):
        try:
            threshold_list = self.platform_fee_group.tier_thresholds.all()
            idx = (*threshold_list,).index(self)
            if idx == 0:
                return 0
            else:
                return threshold_list[idx-1].threshold
        except Exception as e:
            print(e)
            return 0

    @property
    def upper_threshold(self):
        return self.threshold

    def __str__(self):
        return str(self.threshold)


class PlatformTierPercs(models.Model):
    """
    Applicable percentage for each fee tier
    """
    platform_fee_group = models.ForeignKey(PlatformFees,
                                           on_delete=models.CASCADE,
                                           related_name="tier_percs")
    percentage = models.DecimalField(max_digits=7, decimal_places=6, default=0)

    class Meta:
        ordering = ['-percentage']

    def __str__(self):
        return str(self.percentage)
