from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models.query_utils import Q

from riskprofiles.api.serializers import (RiskProfileSerializer,
                                          RiskProfileAASerializer,
                                          RiskProfileAANameSerializer,
                                          RiskProfileGroupSerializer)
from riskprofiles.models import (RiskProfile, RiskProfileAAName, RiskProfileAA,
                                 RiskProfileGroup)
from riskprofiles.api.permissions import HasAccessToRP
from django.contrib.auth import get_user_model
from django.db.models import Prefetch


User = get_user_model()

def get_user_AFSL(user):
    if user.AFSL_approved:
        return user.AFSL
    else:
        return None

class RiskProfileGroupViewSet(viewsets.ModelViewSet):
    '''
    Access to Risk Profile Groups that
    - The user is in "allowed_users"
    - The user's AFSL owns (AFSL.risk_profile_group)
    - The user's practice owns (Practice.risk_profile_group)
    - Are the assigned risk_profile_group for the the user's active_practice
    '''
    lookup_field = "id"
    serializer_class = RiskProfileGroupSerializer
    permission_classes = [IsAuthenticated, HasAccessToRP|IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        AFSL = get_user_AFSL(user)
        practices = user.practices.all()
        active_practice = user.active_practice
        # return RiskProfileGroup.objects.all()
        # if user.is_superuser:
        #     return RiskProfileGroup.objects.all().order_by("name")
        # else:
        return RiskProfileGroup.objects.filter(Q(allowed_users__in=[user])
                                               | Q(afsls__in=[AFSL])
                                               | Q(active_practices__in=practices)
                                               | Q(afsls__active_practices__in=[active_practice])
                                                  ).order_by("name")


class RiskProfileViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = RiskProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group = self.kwargs.get("riskprofilegroup_id")
        return RiskProfile.objects.filter(group=group).order_by("id")


class RiskProfileAAViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = RiskProfileAASerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        riskprofile_id = self.kwargs.get("riskprofile_id")
        return RiskProfileAA.objects.filter(riskprofile=riskprofile_id).order_by("name__order")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["riskprofile_id"] = self.kwargs["riskprofile_id"]
        return context


class RiskProfileAANameViewSet(viewsets.ModelViewSet):
    '''
    Access to Risk Profile Names that
    - The user is in "allowed_users"
    - The user's AFSL owns (AFSL.risk_profile_group)
    - The user's practice owns (Practice.risk_profile_group)
    - Is default (belongs to ProductRex, assigned to account on creation)
    '''
    lookup_field = "id"
    serializer_class = RiskProfileAANameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        AFSL = get_user_AFSL(user)
        practices = user.practices.all()
        group = self.kwargs.get("riskprofilegroup_id")
        return RiskProfileAAName.objects.filter(Q(group__allowed_users__in=[user])
                                                | Q(group__afsls__in=[AFSL])
                                                | Q(group__active_practices__in=practices)
                                                | Q(group__default=True),
                                                group=group).order_by("order")

###########
# Helper viewsets
###########


class ActiveAANameViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = RiskProfileAANameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        practices = user.practices.all()
        return RiskProfileAAName.objects.filter(group=user.active_rp).order_by("order")

###########
# Template viewsets
###########

class RiskProfileAANameTemplateViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = RiskProfileAANameSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_queryset(self):
        return RiskProfileAAName.objects.filter(template=True).order_by("order")


class RiskProfileDefaultAANameTemplateViewSet(viewsets.ModelViewSet):
    '''
    Default AA Names that are available to all users.
    '''
    lookup_field = "id"
    serializer_class = RiskProfileAANameSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_queryset(self):
        return RiskProfileAAName.objects.filter(template=True,
                                                group__default=True).order_by("order")


class RiskProfileGroupTemplateViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = RiskProfileGroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return RiskProfileGroup.objects.filter(template=True).order_by("name")
