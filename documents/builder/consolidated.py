from platforms.models import Platform, PlatformFees
from django.shortcuts import get_list_or_404
from django.forms.models import model_to_dict


def get_consolidated_balance(platforms):
    '''
    Gets the consolidated balance for all recommended platform
    '''
    balance = sum([p.platform_total for p in platforms if p.status == "Recommended"])
    for platform in platforms:
        platform.consolidated_balance = balance
        platform.factor = balance / platform.platform_total
    return platforms


def get_factor(platform, fee, factor):
    '''
    Gets the factor which is used to modify the sliding admin fee calculations
    '''
    total = fee.platform_fee_total
    percentage = total / platform.platform_total
    fee_factor = percentage * factor
    return fee_factor


def get_consolidated_data(platforms):
    '''
    Gets the sliding_admin_fee_consolidated for the platform
    '''
    for platform in platforms:
        fees = platform.fees.all()

        factor = platform.factor
        platform.platform_sliding_admin_fee_consolidated = 0

        for fee in fees:
            if fee.platform_fee_total > 0:
                fee.factor = get_factor(platform, fee, factor)
                fee.sliding_admin_fee_consolidated = fee.get_sliding_admin_fee(factor=factor)
                platform.platform_sliding_admin_fee_consolidated += fee.sliding_admin_fee_consolidated

    return platforms
