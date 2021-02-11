from django.db import models
from django.db.models.query_utils import Q


class RiskProfileGroup(models.Model):
    '''
    This is a top-level grouping for risk profiles. It contains all risk
    profiles for a group, as well as a link to all the applicable
    RiskProfileAANames for that group.

    A user can have multiple RiskProfileGroups if they wish (for example,
    outsourced paraplanners).

    RiskProfileGroups are linked to allowed_users or
    AFSLs for easy sharing of child resources (names, profiles).

    NOTE: Currently there can only be one allowed_user (the "owner").

    Name is defaulted to either the user's name or AFSL + "Risk Profiles".

    The "Default" Risk Profile is open to all

    A user can only have one risk profile group active at any one time.
    '''
    name = models.CharField(max_length=200)
    allowed_users = models.ManyToManyField('users.User',
                                           related_name="risk_profile_groups",
                                           blank=True)

    default = models.BooleanField(default=False)
    template = models.BooleanField(default=False)

    @property
    def unique_name(self):
        if self.allowed_users:
            return (f'{self.name} ({self.allowed_users.all()[0].email})')

    def __str__(self):
        return self.name


class RiskProfileAAName(models.Model):
    '''
    Name of the asset allocation classes (Aus eqs, Int eqs, etc.)
    These are set to a "standard" set by default but can be modded by user.

    Each user is created their own set based off our default upon account
    creation. The custom_name is defaulted to the "name" via a signal
    but this field can be changed at a later date (users are encouraged to).

    Note that the "name" field can not be changed by the user - this is a link
    to the original template rp_aa_name which is linked to individual
    investment AA names.

    Some names may be "inactive" by default. That is, the user can use them,
    and they will be mapped to managed fund data, but we do not endorse them.

    Custom_names can be custom to the user (allowed_users), limited to an AFSL
    (FK in AFSL model) or open to all/default (group_default = True)


    '''
    name = models.CharField(max_length=200)
    custom_name = models.CharField(max_length=200, blank=True, null=True)
    group = models.ForeignKey(RiskProfileGroup,
                              on_delete=models.CASCADE,
                              related_name="rp_aa_names",
                              blank=True, null=True)
    template = models.BooleanField(default=False)
    # The order which these names appear in charts/tables
    order = models.PositiveIntegerField(default=0)

    TYPE_CHOICES = [
        ('Defensive', "Defensive asset"),
        ('Growth', "Growth asset"),
        ('Alternative', "Alternative asset"),
    ]
    asset_type = models.CharField(max_length=100,
                                  choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class RiskProfile(models.Model):
    '''
    The risk profile name, macro data and order.

    Ordering is from most defensive (0) to most aggressive (-1)
    '''
    name = models.CharField(max_length=200)
    group = models.ForeignKey(RiskProfileGroup,
                              on_delete=models.CASCADE,
                              related_name="risk_profiles",
                              blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class RiskProfileAA(models.Model):
    '''
    The actual risk asset allocations. Multiple of these for each risk profile.
    '''
    name = models.ForeignKey(RiskProfileAAName,
                             on_delete=models.CASCADE,
                             related_name="allocations")
    riskprofile = models.ForeignKey(RiskProfile,
                                    on_delete=models.CASCADE,
                                    related_name="allocations")
    percentage = models.DecimalField(max_digits=7,
                                     decimal_places=6,
                                     default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'riskprofile'],
                                    name='unique_name')
        ]


    def __str__(self):
        return self.name.name
