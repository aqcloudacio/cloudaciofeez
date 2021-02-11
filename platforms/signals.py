from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
import copy
from django.shortcuts import get_object_or_404, get_list_or_404

from platforms.models import (Platform, PlatformFees, PlatformTierThresholds,
                              PlatformTierPercs, PlatformNames)
from portfolios.models import Portfolio
from investments.models import Investment, AssetAllocation


@receiver(pre_save, sender=Platform)
def apply_platform_template(sender, instance, *args, **kwargs):
    '''
    Searches for a platform of the same name where template = True.
    Once found, the instance is updated with that template's details.
    '''
    try:
        if (not instance.id and not instance.template and not instance.edited
            and not instance.cloned):
            scenario_id = instance.scenario
            status = instance.status
            platform_template = get_object_or_404(Platform,
                                                  name=instance.name,
                                                  template=True)
            instance.__dict__.update(platform_template.__dict__)
            instance.id = None
            instance.scenario = scenario_id
            instance.template = False
            instance.status = status
    except Exception as e:
        print(e)

@receiver(pre_save, sender=Platform)
def refresh_platform_template(sender, instance, *args, **kwargs):
    '''
    Refreshes platform data when the user requests it, or when the platform
    name is changed.
    '''
    if instance.refresh:
        scenario_id = instance.scenario
        status = instance.status
        id = instance.id

        if not instance.custom_name or instance.custom_name == "":
            platform_template = get_object_or_404(Platform,
                                                  name=instance.name,
                                                  template=True)
            instance.__dict__.update(platform_template.__dict__)
        else:
            custom_name = instance.custom_name
            empty_platform = Platform(custom_name=custom_name)
            instance.__dict__.update(empty_platform.__dict__)

        instance.id = id
        instance.scenario = scenario_id
        instance.template = False
        instance.status = status
        instance.refresh = True


@receiver(post_save, sender=Platform)
def post_save_master(sender, instance, *args, **kwargs):
    refresh_platform_fee_template(sender, instance, *args, **kwargs)
    create_auto_portfolio(sender, instance, *args, **kwargs)
    apply_platform_fee_template(sender, instance, *args, **kwargs)
    clone_platform_details(sender, instance, *args, **kwargs)
    create_default_fees(sender, instance, *args, **kwargs)


def refresh_platform_fee_template(sender, instance, *args, **kwargs):
    '''
    Duplicates the underlying fees for a newly created non-template platform.
    First finds the fee instances belonging to the template, then loops through
    them, creating new fee objects for the new platform instance.

    For each new fee object, the assocated tier fees model instances are also
    duplicated.

    '''
    if instance.refresh:

        # Break recursion
        instance.refresh = False

        # Sets the fee group to None so the investments aren't deleted when
        # the fee group is..
        investments = instance.investments.all()
        for investment in investments:
            investment.platform_fee_group = None

        # Delete all linked platform fee instances
        PlatformFees.objects.filter(platform=instance).delete()

        # Find the template fee instances and tier structures for the new
        # platform after it has been reset
        if not instance.custom_name:

            # Finds the platformname template for the given instance.
            template_platform_name = get_object_or_404(PlatformNames,
                                                   name=instance.name)

            # If the platform has no fees and copies another platforms (i.e.
            # the fee_owner field is in use), get the instance of that owner
            # platform and use it as a source of data.
            if template_platform_name.fee_owner:
                template_platform_name = template_platform_name.fee_owner

            # IF THE PLATFORM TEMPLATE DOES NOT HAVE FEES IT WILL BUG OUT.
            # EDGE CASE THAT I'M NOT WORRYING ABOUT FOR NOW.
            platform_template_fees = get_list_or_404(PlatformFees,
                                                     platform__name=template_platform_name,
                                                     platform__template=True)
            for fee_object in platform_template_fees:
                new_fee_object = PlatformFees()
                new_id = new_fee_object.id
                new_fee_object.__dict__.update(fee_object.__dict__)
                new_fee_object.platform = instance
                new_fee_object.id = new_id

                try:
                    new_fee_object.save()
                    new_fee_object.allowed_investments.set(fee_object.allowed_investments.all())
                    new_fee_object.save()
                    new_fee_object.allowed_investment_classes.set(fee_object.allowed_investment_classes.all())
                except Exception as e:
                    print(e)

                template_thresholds_list = fee_object.tier_thresholds.all()
                if template_thresholds_list:
                    for threshold_object in template_thresholds_list:
                        new_threshold_object = PlatformTierThresholds()
                        new_threshold_id = new_threshold_object.id
                        new_threshold_object.__dict__.update(threshold_object.__dict__)
                        new_threshold_object.platform_fee_group = new_fee_object
                        new_threshold_object.id = new_threshold_id
                        new_threshold_object.save()

                    template_percs_list = fee_object.tier_percs.all()

                    for perc_object in template_percs_list:
                        new_perc_object = PlatformTierPercs()
                        new_perc_id = new_perc_object.id
                        new_perc_object.__dict__.update(perc_object.__dict__)
                        new_perc_object.platform_fee_group = new_fee_object
                        new_perc_object.id = new_perc_id
                        new_perc_object.save()

        # If platform is swapped to a custom platfrom, save a new blank fee
        # instance.
        else:
            new_fee_object = PlatformFees(platform=instance)
            new_fee_object.save()

        # Trigger the post-save signal for investments to re-set the
        # fee group (the old one will be deleted).
        for investment in investments:
            investment.save()

        # Re-save the entire instance (save  Refresh field)
        instance.save();

def apply_platform_fee_template(sender, instance, *args, **kwargs):
    '''
    Duplicates the underlying fees for a newly created non-template platform.
    First finds the fee instances belonging to the template, then loops through
    them, creating new fee objects for the new platform instance.

    For each new fee object, the assocated tier fees model instances are also
    duplicated.

    '''
    try:
        if (not instance.template and not instance.fees.exists()
            and not instance.edited and not instance.cloned):

            # Finds the platformname template for the given instance.
            template_platform_name = get_object_or_404(PlatformNames,
                                                   name=instance.name)

            # If the platform has no fees and copies another platform's (i.e.
            # the fee_owner field is in use), get the instance of that owner
            # platform and use it as a source of data.
            if template_platform_name.fee_owner:
                template_platform_name = template_platform_name.fee_owner

            # IF THE PLATFORM TEMPLATE DOES NOT HAVE FEES IT WILL BUG OUT.
            # EDGE CASE THAT I'M NOT WORRYING ABOUT FOR NOW.
            platform_template_fees = get_list_or_404(PlatformFees,
                                                     platform__name=template_platform_name,
                                                     platform__template=True)

            for fee_object in platform_template_fees:
                new_fee_object = PlatformFees()
                new_id = new_fee_object.id
                new_fee_object.__dict__.update(fee_object.__dict__)
                new_fee_object.platform = instance
                new_fee_object.id = new_id

                try:
                    # Manually sets the allowed investments and investment classes
                    new_fee_object.save()
                    new_fee_object.allowed_investments.set(fee_object.allowed_investments.all())
                    new_fee_object.save()
                    new_fee_object.allowed_investment_classes.set(fee_object.allowed_investment_classes.all())
                except Exception as e:
                    print(e)

                template_thresholds_list = fee_object.tier_thresholds.all()
                if template_thresholds_list:
                    for threshold_object in template_thresholds_list:
                        new_threshold_object = PlatformTierThresholds()
                        new_threshold_id = new_threshold_object.id
                        new_threshold_object.__dict__.update(threshold_object.__dict__)
                        new_threshold_object.platform_fee_group = new_fee_object
                        new_threshold_object.id = new_threshold_id
                        new_threshold_object.save()

                    template_percs_list = fee_object.tier_percs.all()

                    for perc_object in template_percs_list:
                        new_perc_object = PlatformTierPercs()
                        new_perc_id = new_perc_object.id
                        new_perc_object.__dict__.update(perc_object.__dict__)
                        new_perc_object.platform_fee_group = new_fee_object
                        new_perc_object.id = new_perc_id
                        new_perc_object.save()

    except Exception as e:
        print(e)

def clone_platform_details(sender, instance, *args, **kwargs):
    '''
    Clones the fees, tiers, investments and asset allocations for platform
    instances (not templates) that have been cloned via the Scenario view.

    '''
    if instance.cloned and not instance.fees.exists():
        try:
            platform_fees = get_list_or_404(PlatformFees,
                                            platform__id=instance.clone_link)
        except Exception as e:
            platform_fees = None
            print(e)

        if platform_fees:
            for fee_object in platform_fees:
                new_fee_object = PlatformFees()
                new_id = new_fee_object.id
                new_fee_object.__dict__.update(fee_object.__dict__)
                new_fee_object.platform = instance
                new_fee_object.id = new_id

                try:
                    new_fee_object.save()
                    new_fee_object.allowed_investments.set(fee_object.allowed_investments.all())
                    new_fee_object.save()
                    new_fee_object.allowed_investment_classes.set(fee_object.allowed_investment_classes.all())
                except Exception as e:
                    print(e)

                template_thresholds_list = fee_object.tier_thresholds.all()
                if template_thresholds_list:
                    for threshold_object in template_thresholds_list:
                        new_threshold_object = PlatformTierThresholds()
                        new_threshold_id = new_threshold_object.id
                        new_threshold_object.__dict__.update(threshold_object.__dict__)
                        new_threshold_object.platform_fee_group = new_fee_object
                        new_threshold_object.id = new_threshold_id
                        new_threshold_object.save()

                    template_percs_list = fee_object.tier_percs.all()

                    for perc_object in template_percs_list:
                        new_perc_object = PlatformTierPercs()
                        new_perc_id = new_perc_object.id
                        new_perc_object.__dict__.update(perc_object.__dict__)
                        new_perc_object.platform_fee_group = new_fee_object
                        new_perc_object.id = new_perc_id
                        new_perc_object.save()

                if fee_object.investments.exists():
                    investment_list = fee_object.investments.all()
                    for investment in investment_list:
                        new_investment = Investment()
                        new_investment_id = new_investment.id
                        new_investment.__dict__.update(investment.__dict__)
                        new_investment.id = new_investment_id
                        new_investment.platform = instance
                        new_investment.platform_fee_group = new_fee_object
                        new_portfolio = get_object_or_404(Portfolio,
                                                          platform__id=instance.id,
                                                          template=False,
                                                          auto_created=True)
                        new_investment.portfolio = new_portfolio
                        new_investment.save()

                        aa_list = investment.asset_allocations.all()
                        if aa_list:
                            for aa_object in aa_list:
                                new_aa_object = AssetAllocation()
                                new_aa_id = new_aa_object.id
                                new_aa_object.__dict__.update(aa_object.__dict__)
                                new_aa_object.investment = new_investment
                                new_aa_object.id = new_aa_id
                                new_aa_object.save()

        instance.cloned = False
        instance.save()

def create_auto_portfolio(sender, instance, *args, **kwargs):
    '''
    Automatically creates a default portfolio for each platform.
    '''
    try:
        if not instance.portfolios.exists():
            new_portfolio = Portfolio(id=None,
                                      name="Default",
                                      platform=instance,
                                      template=False,
                                      auto_created=True)
            new_portfolio.save()
    except Exception as e:
        print(e)


def create_default_fees(sender, instance, *args, **kwargs):
    '''
    Automatically creates a default fee group for custom platforms. Group is
    empty but helps avoid other bugs.
    '''
    try:
        if (not instance.fees.exists() and instance.edited
            and not instance.template and not instance.cloned):
            new_fees = PlatformFees(id=None,
                                    description="Fee Structure",
                                    platform=instance)
            new_fees.save()
    except Exception as e:
        print(e)


@receiver(post_save, sender=PlatformNames)
def create_platform(sender, instance, *args, **kwargs):
    '''
    Creates an empty platform template each time a new platformname is created.
    This is so there is always a platfrom template for a platformname (unless
    it is manually deleted).
    '''
    if not instance.platforms.exists():
        new_platform = Platform(name=instance,
                                template=True)
        new_platform.save()
