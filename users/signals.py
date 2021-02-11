from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model

from users.models import User, Practice, Notification


User = get_user_model()

@receiver(pre_save, sender=Practice)
def add_AFSL(sender, instance, *args, **kwargs):
    '''
    When an AFSL is added to a practice (or changed),
    1. The AFSL's Theme and Risk Profiler are added to the Practice if the
       Practice does not have a Theme/Risk Profiler set.
    2. The AFSL's Model Portfolios are added to the practice.
    '''

    attrs = ["risk_profile_group", "theme", "model_portfolios"]

    if instance.id and instance.AFSL:
        original = get_object_or_404(Practice, id=instance.id)
        if original.AFSL != instance.AFSL:
            # New AFSL added/modded
            instance = set_practice_attrs(instance, attrs)

    elif instance.AFSL:
        # New Practice and has AFSL
        instance = set_practice_attrs(instance, attrs)

    else:
        # New practice, no AFSL
        pass


def set_practice_attrs(instance, attrs):
    for attr in attrs:
        if not getattr(instance, attr):
            # If the practice rpg/theme/model is not set, set it.
            setattr(instance, attr, getattr(instance.AFSL, attr, None))
        elif attr == "model_portfolios":
            # if model_portfolios has entries, add the afsl's model ports to it.
            instance.model_portfolios.add(*instance.AFSL.model_portfolios.all())
        else:
            pass

    return instance

@receiver(post_save, sender=Practice)
def remove_staff(sender, instance, *args, **kwargs):
    '''
    When a user is removed from a practice, this clears their active_practice
    and clears the active_rp if that RP is owned by the remvoed practice.
    '''
    if instance.remove_staff:
        print("STAFF REMOVE METHOD")
        staff_fields = ["practices", "admin_practices", "pending_practices"]
        staff_to_remove = get_object_or_404(User, id=instance.remove_staff)

        for staff_field in staff_fields:
            if getattr(staff_to_remove, staff_field, False):
                getattr(staff_to_remove, staff_field).remove(instance)

        if staff_to_remove.active_practice == instance:
            staff_to_remove.active_practice = None

        if staff_to_remove.active_rp == instance.risk_profile_group:
            staff_to_remove.active_rp = None

        staff_to_remove.save()

        # Resets remove_staff in case the user is readded in future.
        instance.remove_staff = None
        instance.save()


@receiver(pre_save, sender=User)
def user_pre_save_master(sender, instance, *args, **kwargs):
    set_active_rp(sender, instance, *args, **kwargs)
    set_active_theme(sender, instance, *args, **kwargs)

def set_active_rp(sender, instance, *args, **kwargs):
    '''
    Sets the active RiskProfileGroup when an active practice is added to the
    User instance.
    '''
    if instance.active_practice and instance.active_practice.risk_profile_group:
        old = get_object_or_404(User, id=instance.id)
        if instance.active_practice != old.active_practice:
            instance.active_rp = instance.active_practice.risk_profile_group

def set_active_theme(sender, instance, *args, **kwargs):
    '''
    Sets the active theme when an active practice is added to the
    User instance.
    '''
    if instance.active_practice and instance.active_practice.theme:
        old = get_object_or_404(User, id=instance.id)
        if instance.active_practice != old.active_practice:
            instance.active_theme = instance.active_practice.theme

@receiver(post_save, sender=User)
def user_post_save_master(sender, instance, *args, **kwargs):
    check_for_notifications(sender, instance, *args, **kwargs)

def check_for_notifications(sender, instance, created, **kwargs):
    '''
    Checks to see if the user has notifications assigned to them via the
    "to" field rather than "target". If they do, the "to" field is cleared and
    the user instance is assigned to "target".

    This is only for new users - if a user is sent a notification without an
    account, the notification is saved for when they do have an account, then
    assigned via this signal.
    '''
    if created:
        try:
            notifications = get_list_or_404(Notification, to=instance.email)

            for n in notifications:
                n.to = None
                n.target = instance
                n.save()

        except Exception as e:
            print(e)

        created = False
