from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.exceptions import ObjectDoesNotExist

from investments.models import (Investment, AssetAllocation,
                                AssetAllocationName, InvestmentName)
from portfolios.models import Portfolio
from platforms.models import PlatformFees
from riskprofiles.models import RiskProfileAAName


@receiver(pre_save, sender=Investment)
def pre_save_master(sender, instance, *args, **kwargs):
    apply_investment_template(sender, instance, *args, **kwargs)
    assign_default_portfolio(sender, instance, *args, **kwargs)
    check_fee_group(sender, instance, *args, **kwargs)


@receiver(post_save, sender=Investment)
def post_save_master(sender, instance, *args, **kwargs):
    assign_fee_group(sender, instance, *args, **kwargs)
    check_single_fee_group(sender, instance, *args, **kwargs)
    apply_aa_template(sender, instance, *args, **kwargs)


######
# Pre save signals
######
def apply_investment_template(sender, instance, *args, **kwargs):
    '''
    Searches for an investment of the same name where template = True.
    Once found, the instance is updated with that template's details.
    '''
    if not instance.id and not instance.template:
        if not instance.custom_name and not instance.platform.cloned:
            portfolio = instance.portfolio
            platform = instance.platform
            amount = instance.amount
            investment_template = get_object_or_404(Investment,
                                                    name=instance.name,
                                                    template=True)
            instance.__dict__.update(investment_template.__dict__)
            instance.id = None
            instance.portfolio = portfolio
            instance.amount = amount
            instance.platform = platform
            instance.template = False


def assign_default_portfolio(sender, instance, *args, **kwargs):
    '''
    Assigns the investment to a "Default" portfolio if one has not been set.

    This assignment is fairly arbitrary and used so that investments don't go
    missing.
    '''
    if not instance.portfolio and not instance.template:
        if not instance.platform.cloned:
            default = get_object_or_404(Portfolio,
                                        platform=instance.platform,
                                        auto_created=True)
            instance.portfolio = default

def check_fee_group(sender, instance, *args, **kwargs):
    '''
    Checks an existing investment to see if certain fields have changed
    that might necessitate a fee_group refresh.
    '''
    # Includes investments that have the following fields modified:
    # - Cash
    # - TD
    # - investment_class

    # Skip signal if the fee group has been overridden
    if not instance.override_fee_group:
        # Skip signal if it has no platform_fee_group - this means it was sent
        # here by the platform signal when a platform was reset.
        if instance.platform_fee_group:
            # Skip signal if it's a template investment or does not yet exist (no id)
            if not instance.template and instance.id:
                recheck_fee_group = False
                existing = Investment.objects.get(id=instance.id)
                # These are the fields that are checked to see if they have changed.
                fields = ['cash','TD','investment_class', 'override_fee_group']
                for field in fields:
                    if getattr(instance,field,0) != getattr(existing,field,0):
                        recheck_fee_group = True
                        break
                # Assign fee groups instance does not have one or given fields have changed.
                if recheck_fee_group:
                    # Gets all the fee groups for the instance's platform.
                    fee_groups = get_list_or_404(PlatformFees,
                                                 platform=instance.platform)

                    investment_class_limitations = [list(f.allowed_investment_classes.all()) for f in fee_groups]
                    all_classes = [item for sublist in investment_class_limitations for item in sublist]

                    # If the instance is in one of the limited fee groups
                    if instance.investment_class in all_classes:
                        for group in [g for g in fee_groups if g.allowed_investment_classes.all()]:
                            # Find the fee_group that it belongs to and assign it that group.
                            if instance.investment_class in group.allowed_investment_classes.all():
                                instance.platform_fee_group = group
                                group.investments.add(instance)
                                group.save()
                                break
                    else:
                        group = instance.platform_fee_group
                        group.investments.remove(instance)
                        group.save()
                        instance.platform_fee_group = None


######
# Post save signals
######

def assign_fee_group(sender, instance, *args, **kwargs):
    '''
    Assigns a fee group for a given investment.

    This can be based on a fee group allowed_investment limitation, or
    allowed_investment_classes limitation. Priority is given to
    investment_classes as these trump actual names.

    The investment code (ASX, APIR, or OTHER) must be in
    platform_fee_group.allowed_investments OR
    platform_fee_group.allowed_investments must be blank.
    '''

    # Skip signal if the fee group has been overridden
    if not instance.override_fee_group:
        # Skip signal if it's a template investment.
        if not instance.template:
            if not instance.platform_fee_group:
                # Gets all the fee groups for the instance's platform.
                fee_groups = get_list_or_404(PlatformFees,
                                             platform=instance.platform)

                investment_class_limitations = [list(f.allowed_investment_classes.all()) for f in fee_groups]
                all_classes = [item for sublist in investment_class_limitations for item in sublist]

                # If the instance is in one of the limited fee groups
                if instance.investment_class in all_classes:
                    for group in [g for g in fee_groups if g.allowed_investment_classes.all()]:
                        # Find the fee_group that it belongs to and assign it that group.
                        if instance.investment_class in group.allowed_investment_classes.all():
                            print(775)
                            instance.platform_fee_group = group
                            break

                # If the investment does not belong to a limited fee group.
                else:
                    # Removes fee groups that are limited to an inv class (already dealth witH)
                    fee_groups = [g for g in fee_groups if not g.allowed_investment_classes.all()]
                    # IF the investment is cash or TD, assign to the first fee_group
                    # (sorted by "order" field)
                    if instance.cash or instance.TD:
                        instance.platform_fee_group = fee_groups[0]
                    else:
                        #Iterate fee groups that do NOT have investment class limitation
                        for group in fee_groups:
                            allowed_investments = group.allowed_investments.all()
                            # If the investment_name is in the group's allowed_investments
                            if instance.name in allowed_investments:
                                instance.platform_fee_group = group
                                break
                            # # If there are no allowed_investments (the fee_group is open
                            # # to all)
                            # elif not allowed_investments:
                            #     instance.platform_fee_group = group
                            #     break
                            # catchall to assign to the last fee group (all invs must have
                            # a fee group).
                            else:
                                instance.platform_fee_group = fee_groups[-1]
                                break
                instance.save()


def check_single_fee_group(sender, instance, *args, **kwargs):
    '''
    Checks if the platform has a single fee group.

    If it does, compiles a set of all fee groups currently in use
    (i.e. an investment has been assigned to them under that platform) and
    assigns ALL investments under that platform to the highest "order" group
    (i.e. the most expensive).
    '''
    if (not instance.template and instance.platform.single_fee_group
        and not instance.platform.cloned):
        all_fee_groups = get_list_or_404(PlatformFees,
                                         platform=instance.platform,
                                         investments__isnull=False)
        max_order = max(group.fee_group_order for group in all_fee_groups)
        highest_rank_group = get_object_or_404(PlatformFees,
                                               fee_group_order=max_order,
                                               platform=instance.platform)
        instance.platform_fee_group = highest_rank_group
        investments = get_list_or_404(Investment,
                                      platform=instance.platform)
        for investment in investments:
            if investment.platform_fee_group != highest_rank_group:
                investment.platform_fee_group = highest_rank_group
                print(44)
                investment.save()



def apply_aa_template(sender, instance, *args, **kwargs):
    '''
    Adds the underlying aa for a newly created non-template investments.
    First finds the aa instances belonging to the template, then loops through
    them, creating new aa objects for the new investment instance.
    '''
    if not instance.template and not instance.asset_allocations.exists():
        if not instance.custom_name and not instance.platform.cloned:
            try:
                investment_template_aa = get_list_or_404(AssetAllocation,
                                                         investment__name=instance.name,
                                                         investment__template=True)
                for aa_object in investment_template_aa:
                    new_aa_object = AssetAllocation()
                    new_id = new_aa_object.id
                    new_aa_object.__dict__.update(aa_object.__dict__)
                    new_aa_object.investment = instance
                    new_aa_object.id = new_id

                    new_aa_object.save()

            except Exception:
                pass

##################
### Pre-save signals - AA
##################
@receiver(pre_save, sender=AssetAllocation)
def link_rpaa_to_aa(sender, instance, *args, **kwargs):
    '''
    This is primarily used for custom investments. Links the user's risk
    profile asset allocation "name" (the uneditable template name) to an
    AssetAllocationName of the same name.

    Templated RiskProfileAAName's will always have a AssetAllocationName that
    exactly matches.

    NT NOTE: ENFORCE THIS VIA A SIGNAL ON RISKPROFILEENAME TEMPLATE INSTANTIATION
    '''
    if instance.rp_name_id:
        rp_name = get_object_or_404(RiskProfileAAName,
                                    id=instance.rp_name_id.id)
        aaname = get_object_or_404(AssetAllocationName,
                                   name=rp_name.name)
        instance.name = aaname


@receiver(post_save, sender=InvestmentName)
def create_investment(sender, instance, *args, **kwargs):
    if not instance.investments.exists():
        new_investment = Investment(name=instance,
                                    template=True)
        new_investment.save()
