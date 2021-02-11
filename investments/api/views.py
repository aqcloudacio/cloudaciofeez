from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import pagination

from investments.api.serializers import (InvestmentSerializer,
                                         InvestmentClassSerializer,
                                         AssetAllocationNameSerializer,
                                         AssetAllocationSerializer,
                                         InvestmentNameSerializer,
                                         NABInvestmentSerializer,
                                         InvestmentTemplateSerializer,
                                         AssetAllocationTemplateSerializer)
from investments.models import (Investment, InvestmentClass, AssetAllocation,
                                AssetAllocationName, InvestmentName,
                                NABInvestment)
from riskprofiles.api.serializers import RiskProfileAANameSerializer
from scenarios.models import Scenario
from riskprofiles.models import RiskProfileAAName

#### Pagination classes
class InvestmentNamePagination(pagination.PageNumberPagination):
       page_size = 1000

#### Viewsets

class InvestmentViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        portfolio_id = self.kwargs.get("portfolio_id")
        return Investment.objects.filter(portfolio=portfolio_id).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["portfolio_id"] = self.kwargs["portfolio_id"]
        return context


class InvestmentClassViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = InvestmentClassSerializer
    permission_classes = [IsAuthenticated]
    queryset = InvestmentClass.objects.all().order_by("name")


class InvestmentNameViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = InvestmentNameSerializer
    permission_classes = [IsAuthenticated]
    queryset = InvestmentName.objects.all().order_by("platform")
    pagination_class = InvestmentNamePagination

class UnlinkedInvestmentNameViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = InvestmentNameSerializer
    permission_classes = [IsAuthenticated]
    queryset = InvestmentName.objects.filter(platform=None).order_by("name")
    pagination_class = InvestmentNamePagination

class AssetAllocationViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = AssetAllocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        investment_id = self.kwargs.get("investment_id")
        return AssetAllocation.objects.filter(investment=investment_id).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["investment_id"] = self.kwargs["investment_id"]
        context["user"] = self.request.user
        return context


class AssetAllocationNameViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = AssetAllocationNameSerializer
    permission_classes = [IsAuthenticated]
    queryset = AssetAllocationName.objects.all().order_by("name")


class UnlinkedAssetAllocationNameViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = AssetAllocationNameSerializer
    permission_classes = [IsAuthenticated]
    queryset = AssetAllocationName.objects.filter(rp_aaname_link=None).all().order_by("name")


class NABInvestmentViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = NABInvestmentSerializer
    permission_classes = [IsAuthenticated]
    queryset = NABInvestment.objects.all().order_by("name")

#######
# Helper views
#######

class InvestmentAASummaryViewset(viewsets.ModelViewSet):
    '''
    Provides an AA summary for the investment, based off the risk_profile in use
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
        context["investment_id"] = self.kwargs["investment_id"]
        return context

############
# Template views
############


class InvestmentTemplateViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Investment.objects.filter(template=True).order_by("id")

class AssetAllocationTemplateViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = AssetAllocationTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        investment_id = self.kwargs.get("investmenttemplate_id")
        return AssetAllocation.objects.filter(investment=investment_id).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["investment_id"] = self.kwargs["investmenttemplate_id"]
        return context
