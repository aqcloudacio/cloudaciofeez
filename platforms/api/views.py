from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import pagination


from platforms.api.serializers import (PlatformSerializer,
                                       PlatformNameSerializer,
                                       PlatformFeeSerializer,
                                       PlatformTierPercsSerializer,
                                       PlatformTierThresholdsSerializer,
                                       PlatformPortfolioSerializer,
                                       PlatformFamilyGroupsSerializer)
from platforms.models import (Platform, PlatformNames, PlatformFees,
                              PlatformTierPercs, PlatformTierThresholds,
                              PlatformFamilyGroups)
from investments.models import AssetAllocation, Investment, InvestmentName
from portfolios.models import Portfolio
from investments.api.serializers import (AssetAllocationSerializer,
                                         InvestmentSerializer,
                                         InvestmentNameSerializer)
from riskprofiles.models import RiskProfileAAName
from riskprofiles.api.serializers import RiskProfileAANameSerializer
from scenarios.models import Scenario

User = get_user_model()

#### Pagination classes
class PlatformNamePagination(pagination.PageNumberPagination):
       page_size = 1000

class PlatformPagination(pagination.PageNumberPagination):
       page_size = 30

class PlatformFeeGroupPagination(pagination.PageNumberPagination):
       page_size = 200

#### Viewsets

class PlatformViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PlatformPagination

    def get_queryset(self):
        scenario_id = self.kwargs.get("scenario_id")
        return Platform.objects.filter(scenario=scenario_id).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["scenario_id"] = self.kwargs["scenario_id"]
        return context


class PlatformFeeViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = PlatformFeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        platform_id = self.kwargs.get("platform_id")
        return PlatformFees.objects.filter(platform=platform_id).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["platform_id"] = self.kwargs["platform_id"]
        return context


class PlatformNameViewSet(viewsets.ModelViewSet):
    queryset = PlatformNames.objects.all().order_by("name")
    lookup_field = "id"
    serializer_class = PlatformNameSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PlatformNamePagination


class PlatformTierThresholdViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = PlatformTierThresholdsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        platformfee_id = self.kwargs.get("platformfee_id")
        return PlatformTierThresholds.objects.filter(platform_fee_group=platformfee_id).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["platformfee_id"] = self.kwargs["platformfee_id"]
        return context


class PlatformTierPercViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = PlatformTierPercsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        platformfee_id = self.kwargs.get("platformfee_id")
        return PlatformTierPercs.objects.filter(platform_fee_group=platformfee_id).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["platformfee_id"] = self.kwargs["platformfee_id"]
        return context

class PlatformFamilyGroupsViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = PlatformFamilyGroupsSerializer
    permission_classes = [IsAuthenticated]
    queryset = PlatformFamilyGroups.objects.all()
    pagination_class = PlatformFeeGroupPagination

#####################################
# Generic helper views here
#####################################

class PlatformAAViewSet(viewsets.ModelViewSet):
    '''
    Shows all asset allocation for a single platform
    '''
    lookup_field = "id"
    serializer_class = AssetAllocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        platform_id = self.kwargs.get("platform_id")
        return AssetAllocation.objects.filter(investment__platform=platform_id).order_by("investment")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["platform_id"] = self.kwargs["platform_id"]
        return context

class PlatformNameInvestmentNameViewSet(viewsets.ModelViewSet):
    '''
    Shows all investments linked to a platform name (exclusive investments)
    '''
    lookup_field = "id"
    serializer_class = InvestmentNameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        platformname_id = self.kwargs.get("platformname_id")

        platformname = get_object_or_404(PlatformNames,id=platformname_id)

        if platformname.investments.exists():
            return InvestmentName.objects.filter(platform=platformname_id).order_by("name")
        else:
            return InvestmentName.objects.all().order_by("name")


class PlatformInvestmentViewSet(viewsets.ModelViewSet):
    '''
    Shows all investments for a single platform
    '''
    lookup_field = "id"
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        platform_id = self.kwargs.get("platform_id")
        return Investment.objects.filter(platform=platform_id).order_by("name")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["platform_id"] = self.kwargs["platform_id"]
        return context


class PlatformInvestmentAAViewSet(viewsets.ModelViewSet):
    '''
    Shows all asset allocation for a single investment at the platform level
    '''
    lookup_field = "id"
    serializer_class = AssetAllocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        investment_id = self.kwargs.get("investment_id")
        return AssetAllocation.objects.filter(investment=investment_id).order_by("investment")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["investment_id"] = self.kwargs["investment_id"]
        context["platform_id"] = self.kwargs["platform_id"]
        return context


class PlatformPortfolioViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = PlatformPortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        platform_id = self.kwargs.get("platform_id")
        return Portfolio.objects.filter(platform=platform_id).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["platform_id"] = self.kwargs["platform_id"]
        return context


class PlatformAASummaryViewset(viewsets.ModelViewSet):
    '''
    Provides an AA summary for the entire platform.
    '''
    lookup_field = "id"
    serializer_class = RiskProfileAANameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        scenario_id = self.kwargs.get("scenario_id")
        scenario = get_object_or_404(Scenario, id=scenario_id)
        group = scenario.risk_profile.group

        return RiskProfileAAName.objects.filter(group=group).order_by("order")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["platform_id"] = self.kwargs["platform_id"]
        return context

#####################################
# Template views here
#####################################

class PlatformTemplateViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Platform.objects.filter(template=True).order_by("id")


class PlatformFeeTemplateViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = PlatformFeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        platform_id = self.kwargs.get("platformtemplate_id")
        return PlatformFees.objects.filter(platform=platform_id).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["platform_id"] = self.kwargs["platformtemplate_id"]
        return context


class PlatformTierThresholdTemplateViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = PlatformTierThresholdsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        platformfee_id = self.kwargs.get("platformfeetemplate_id")
        return PlatformTierThresholds.objects.filter(platform_fee_group=platformfee_id).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["platformfee_id"] = self.kwargs["platformfeetemplate_id"]
        return context


class PlatformTierPercTemplateViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = PlatformTierPercsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        platformfee_id = self.kwargs.get("platformfeetemplate_id")
        return PlatformTierPercs.objects.filter(platform_fee_group=platformfee_id).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["platformfee_id"] = self.kwargs["platformfeetemplate_id"]
        return context
