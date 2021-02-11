from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import get_list_or_404, get_object_or_404

from users.models import User
from riskprofiles.models import (RiskProfileAAName, RiskProfile,
                                 RiskProfileGroup, RiskProfileAA)



@receiver(post_save, sender=User)
def post_save_master_user(sender, instance, *args, **kwargs):
    assign_default_rp(sender, instance, *args, **kwargs)


def assign_default_rp(sender, instance, *args, **kwargs):
    '''
    Clones the default risk profile group on user creation.
    '''
    if not instance.risk_profile_groups.all().exists():
        default_rp_group_template = get_object_or_404(RiskProfileGroup,
                                                      template=True,
                                                      default=True)
        new_rp_group = RiskProfileGroup(name=default_rp_group_template.name,
                                        default=True,
                                        template=False)
        new_rp_group.save()
        new_rp_group.allowed_users.set([instance])
        if not instance.active_rp:
            instance.active_rp = new_rp_group
            instance.save()


@receiver(post_save, sender=RiskProfileGroup)
def post_save_master_RP(sender, instance, *args, **kwargs):
    assign_default_profiles(sender, instance, *args, **kwargs)
    assign_default_rp_aa_names(sender, instance, *args, **kwargs)


def assign_default_profiles(sender, instance, *args, **kwargs):
    '''
    Clones the default risk profiles and their AA on user creation.
    '''
    if (instance.default
        and not instance.template
        and not instance.risk_profiles.all().exists()):

        default_rp_templates = get_list_or_404(RiskProfile,
                                               group__template=True,
                                               group__default=True)
        for rp_template in default_rp_templates:
            new_rp = RiskProfile(name=rp_template.name,
                                 group=instance,
                                 order=rp_template.order)
            new_rp.save()

            default_rp_template_aa = get_list_or_404(RiskProfileAA,
                                                     riskprofile=rp_template)
            for rp_template_aa in default_rp_template_aa:
                new_aa = RiskProfileAA(name=rp_template_aa.name,
                                       riskprofile=new_rp,
                                       percentage=rp_template_aa.percentage)
                new_aa.save()


def assign_default_rp_aa_names(sender, instance, *args, **kwargs):
    '''
    Clones the default risk profiles AA names
    '''
    if (not instance.template
        and not instance.rp_aa_names.all().exists()):

        default_rp_aa_names = get_list_or_404(RiskProfileAAName,
                                              group__template=True,
                                              group__default=True)
        for rp_aa_name in default_rp_aa_names:
            new_aa_name = RiskProfileAAName()
            id = new_aa_name.id
            new_aa_name.__dict__.update(rp_aa_name.__dict__)
            new_aa_name.id = id
            new_aa_name.group = instance
            new_aa_name.template = False
            new_aa_name.save()


@receiver(pre_save, sender=RiskProfile)
def add_order_to_rp(sender, instance, *args, **kwargs):
    '''
    Adds order to newly added risk profiles where an order has not been set.
    They are added to the end by default.
    '''

    if not instance.id:
        try:
            all_rps = get_list_or_404(RiskProfile,
                                      group=instance.group)
            instance.order = len(all_rps)+1
        except Exception as e:
            print(e)
            instance.order = 0
